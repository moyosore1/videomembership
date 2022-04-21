import pathlib
from typing import Optional


from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table
from starlette.middleware.authentication import AuthenticationMiddleware


from . import config, db
from .utils import valid_schema_data_or_error
from .shortcuts import render, redirect
from .handlers import *  # noqa

from .playlist.routers import router as playlist_router
from .users.models import User
from .users.schemas import UserSignupSchema, UserSignInSchema
from .users.decorators import login_required
from .users.backends import JWTCookieBackend
from .video.models import Video
from .video.routers import router as video_router
from .watch.models import WatchEvent
from .watch.routers import router as watch_router

BASE_DIR = pathlib.Path(__file__).resolve().parent

# settings = config.get_settings()

main_app = FastAPI()
main_app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
main_app.include_router(video_router)
main_app.include_router(watch_router)
main_app.include_router(playlist_router)

DB_SESSION = None


@main_app.on_event("startup")
def on_startup():
    # called when FastAPI starts
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)


@main_app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, 'account/dashboard.html', {}, status_code=200)
    context = {
        'abc': "moyosore"
    }
    return render(request, "home.html", context)


@main_app.get("/login", response_class=HTMLResponse)
# @requires(['anon'])
def login_get_view(request: Request):
    
    return render(request, "auth/login.html", {})


@main_app.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect("/login")
    return render(request, "auth/login.html", {})


@main_app.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/login", remove_session=True)

@main_app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...), next:Optional[str]="/"):
    # need python-multipart to handle form data.

    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = valid_schema_data_or_error(raw_data, UserSignInSchema)
    context = {
        "data": data,
        "errors": errors
    }
    if len(errors) > 0:
        return render(request,  "auth/register.html", context, status_code=400)
    if "http://127.0.0.1" not in next:
        next = "/"
    return redirect(next, cookies=data)


@main_app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/register.html", {})


@main_app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    # need python-multipart to handle form data.
    raw_data = {
        "email": email,
        "password": password,
        "password2": password2
    }
    data, errors = valid_schema_data_or_error(raw_data, UserSignupSchema)
    if len(errors) > 0:
        return render(request,  "auth/register.html", {"data": data, "errors": errors}, status_code=400)
    return redirect("/login")


@main_app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):

    context = {}
    return render(request, "account/profile.html", context)


@main_app.get("/users")
def users_list():
    queryset = User.objects.all().limit(10)
    return list(queryset)



