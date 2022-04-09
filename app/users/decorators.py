from functools import wraps  # keeps doc string

from fastapi import Request, HTTPException

from .auth import verify_user
from .exceptions import LoginRequiredException


def login_required(func):

    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        session_id = request.cookies.get("session_id")
        user_session = verify_user(session_id)
        if user_session is None:
            raise LoginRequiredException(status_code=400)
        return func(request, *args, **kwargs)

    return wrapper
