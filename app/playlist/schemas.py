import uuid


from pydantic import (BaseModel)


from .models import Playlist


class PlaylistSchema(BaseModel):
    user_id: uuid.UUID
    title: str

   