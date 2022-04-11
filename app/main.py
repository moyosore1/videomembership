import json
import pathlib

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires

from . import config, db
from .utils import valid_schema_data_or_error
from .shortcuts import render, redirect
from .handlers import * # noqa
from .users.models import User
from .users.schemas import UserSignupSchema, UserSignInSchema
from .users.decorators import login_required
from .users.backends import JWTCookieBackend


BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
# settings = config.get_settings()

main_app = FastAPI()
main_app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
DB_SESSION = None


@main_app.on_event("startup")
def on_startup():
    # called when FastAPI starts
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


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
    session_id = request.cookies.get("session_id") or None
    return render(request, "auth/login.html", {"logged_in": session_id is not None})


@main_app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...)):
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
    return redirect("/", cookies=data)


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
