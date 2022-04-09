from pydantic import BaseModel, EmailStr, SecretStr, validator

from .models import User


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
        print(v)
        password2 = v
        if password != password2:
            raise ValueError("Passwords do not match.")
        return v
