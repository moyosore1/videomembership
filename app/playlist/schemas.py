import uuid


from pydantic import (BaseModel,
                      validator,
                      root_validator)

from .models import Playlist
from app.video.models import Video
from app.video.extractors import extract_video_id
from app.users.exceptions import InvalidUserIdException


class PlaylistSchema(BaseModel):
    user_id: uuid.UUID
    title: str


class PlaylistVideoAddSchema(BaseModel):
    url: str
    user_id: uuid.UUID
    playlist_id: uuid.UUID
    title: str

    @validator("url")
    def validate_url(cls, v, values, **kwargs):
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError("Not a valid URL")
        return v

    @validator("playlist_id")
    def validate_playlist_id(cls, v, values, **kwargs):
        q = Playlist.objects.filter(db_id=v)
        if q.count() == 0:
            raise ValueError(f"{v} is not a valid Playlist.")
        return v


    @root_validator
    def validate_data(cls, values):
        url = values.get("url")
        title = values.get("title")
        user_id = values.get("user_id")
        playlist_id = values.get("playlist_id")
        extra_data = {}
        if title is not None:
            extra_data['title'] = title

        video = None
        if url is None:
            raise ValueError("A valid url is required.")
        try:
            video, created = Video.get_or_create(url, user_id=user_id, **extra_data)
        except:
            raise ValueError("There is a problem, please try again")

        if not isinstance(video, Video):
            raise ValueError("There is a problem, please try again")
        if playlist_id:
            playlist_obj = Playlist.objects.get(db_id=playlist_id)
            playlist_obj.add_host_ids(host_ids=[video.host_id])
            playlist_obj.save()

        return video.as_data()
