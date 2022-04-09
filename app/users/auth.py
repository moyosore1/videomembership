import datetime


from jose import jwt, ExpiredSignatureError

from .models import User


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
    return jwt.encode(data, secret_key, algorithm=algo)


def verify_user(token):
    data = None
    try:
        data = jwt.decode(token, secret_key, algorithms=[algo])
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if 'user_id' not in data:
        return None
    return data
