import datetime


from jose import jwt, ExpiredSignatureError

from .models import User
from app import config

settings = config.get_settings()


def authenticate(email, password):
    # if email wasn't the first primary key, it'd have to be
    # User.objects.allow_filtering().get(email=email)
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        user = None
    if not user.verify_password(password):
        return None
    return user


def login(user, expires=30):

    data = {
        "user_id": f"{user.user_id}",
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
    }
    return jwt.encode(data, settings.secret_key, algorithm=settings.jwt_algorithm)


def verify_user(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key,
                          algorithms=[settings.jwt_algorithm])
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if 'user_id' not in data:
        return None
    return data
