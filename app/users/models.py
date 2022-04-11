import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from app.config import get_settings

from . import validators, security

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

    def set_password(self, password, commit=False):
        hashed_password = security.generate_hash(password)
        self.password = hashed_password
        if commit:
            self.save()
        return True

    def verify_password(self, password):
        hashed_password = self.password
        verified = False
        verified, _ = security.verify_hash(hashed_password, password)
        return verified

    @staticmethod
    def create_user(email, password=None):
        qs = User.objects.filter(email=email)
        if qs.count() != 0:
            raise Exception("Email already taken.")

        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise Exception("Invalid email!")

        user = User(email=email)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def check_exists(user_id):
        qs = User.objects.filter(user_id=user_id).allow_filtering()
        return qs.count() != 0

    @staticmethod
    def by_user_id(user_id=None):
        if user_id is None:
            return None
        qs = User.objects.filter(user_id=user_id).allow_filtering()
        if qs.count() != 1:
            return None
        return qs.first()