from importlib.resources import path
import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from app.config import get_settings
from app.users.models import User
from app.users.exceptions import InvalidUserIdException

from .extractors import extract_video_id
from .exceptions import InvalidURLException, VideoAlreadyAddedException

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video (host={self.host_id})"

    def as_data(self):
        return {f"{self.host_service}_id":self.host_id, "path":self.path}

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidURLException("Invalid url")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIdException("Invalid user id.")
        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video has been added by you")
        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)


    @property
    def get_path(self):
        return f"/videos/{self.host_id}"