import json
import pathlib

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from cassandra.cqlengine.management import sync_table


from .utils import valid_schema_data_or_error
from .shortcuts import render
from . import config, db
from .users.models import User
from .users.schemas import UserSignupSchema, UserSignInSchema

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
# settings = config.get_settings()

main_app = FastAPI()
DB_SESSION = None


@main_app.on_event("startup")
def on_startup():
    # called when FastAPI starts
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@main_app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        'abc': "moyosore"
    }
    return render(request, "home.html", context)


@main_app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return render(request, "auth/login.html", {"request": request})


@main_app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...)):
    # need python-multipart to handle form data.
    raw_data = {
        "email": email,
        "password": password
    }
    data, errors = valid_schema_data_or_error(raw_data, UserSignInSchema)
    return render(request, "auth/login.html", {"data": data, "errors": errors})


@main_app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render("auth/register.html", {})


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
    return render(request, "auth/register.html", {"data": data, "errors": errors})


@main_app.get("/users")
def users_list():
    queryset = User.objects.all().limit(10)
    return list(queryset)
