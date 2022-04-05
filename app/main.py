from fastapi import FastAPI

from cassandra.cqlengine.management import sync_table


from . import config, db
from .users.models import User

main_app = FastAPI()
DB_SESSION = None
# settings = config.get_settings()


@main_app.on_event("startup")
def on_startup():
    # called when FastAPI starts
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@main_app.get("/")
def homepage():
    # will be json data
    return {"hello": "world"}

@main_app.get("/users")
def users_list():
    queryset = User.objects.all().limit(10)
    return list(queryset)

