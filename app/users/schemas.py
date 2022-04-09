from pydantic import (BaseModel,
                      EmailStr,
                      SecretStr,
                      validator,
                      root_validator)

from .models import User
from . import auth


class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password2: SecretStr

    @validator("email")
    def validate_email(cls, v, values, **kwargs):
        qs = User.objects.filter(email=v)
        if qs.count() != 0:
            raise ValueError("Email is not available.")
        return v

    @validator("password2")
    def validate_passwords(cls, v, values, **kwargs):
        password = values.get('password')
        password2 = v
        if password != password2:
            raise ValueError("Passwords do not match.")
        return v


class UserSignInSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: str = None

    @root_validator
    def validate_user(cls, values):
        error_msg = "Invalid credentials"
        email = values.get("email") or None
        password = values.get("password") or None

        if email is None or password is None:
            raise ValueError(error_msg)
        password = password.get_secret_value()

        user = auth.authenticate(email, password)
        print(user)
        if user is None:
            raise ValueError(error_msg)
        token = auth.login(user)
        return {"session_id": token}
