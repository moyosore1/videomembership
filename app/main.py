from fastapi import FastAPI
from . import config

main_app = FastAPI()
# settings = config.get_settings()


@main_app.get("/")
def homepage():
    # will be json data
    return {"hello": "world"}
