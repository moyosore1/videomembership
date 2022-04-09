from curses.ascii import HT
from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    pass
