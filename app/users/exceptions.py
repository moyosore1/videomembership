from curses.ascii import HT
from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    pass


class InvalidUserIdException(HTTPException):
    """
        Invalid user id
    """


class UserHasAccountException(Exception):
    pass

class InvalidEmailException(Exception):
    pass
