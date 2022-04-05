import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from app.config import get_settings

from . import validators

settings = get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User (email={self.email})"

    @staticmethod
    def create_user(email, password=None):
        qs = User.objects.filter(email=email)
        if qs.count() != 0:
            raise Exception("Email already taken.")

        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise Exception("Invalid email!")

        user = User(email=email)
        user.password = password
        user.save()
        return user
