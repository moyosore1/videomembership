from ast import For
import pathlib

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table


from . import config, db
from .users.models import User

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
# settings = config.get_settings()

main_app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
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
        'request': request,
        'abc': "moyosore"
    }
    return templates.TemplateResponse("home.html", context)


@main_app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@main_app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...)):
    # need python-multipart to handle form data.
    print(email, password)
    return templates.TemplateResponse("auth/login.html", {"request": request})


@main_app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@main_app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request, email: str = Form(...), password: str = Form(...), password2: str = Form(...)):
    # need python-multipart to handle form data.
    print(email, password)
    return templates.TemplateResponse("auth/login.html", {"request": request})


@main_app.get("/users")
def users_list():
    queryset = User.objects.all().limit(10)
    return list(queryset)
