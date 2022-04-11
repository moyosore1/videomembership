from pydantic import (BaseModel,
                      EmailStr,
                      SecretStr,
                      validator,
                      root_validator)


from app.users.exceptions import InvalidUserIdException
from .exceptions import InvalidURLException, VideoAlreadyAddedException
from .extractors import extract_video_id
from .models import Video

class VideoSchema(BaseModel):
    url: str
    user_id : str

    @validator("url")
    def validate_url(cls, v, values, **kwargs):
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError("Not a valid URL")
        return v


    @root_validator
    def validate_data(cls, values):
        url = values.get("url")
        user_id = values.get("user_id")
        video = None
        try:
            video = Video.add_video(url, user_id=user_id)
        except InvalidURLException:
            raise ValueError("Not a valid URL")
        except VideoAlreadyAddedException:
            raise ValueError("You have already added said video")
        except InvalidUserIdException:
            raise ValueError("Invalid user.")
        except:
            raise ValueError("There is a problem, please try again")
        
        if video is None:
            raise ValueError("There is a problem, please try again")
        
        if not isinstance(video, Video):
            raise ValueError("There is a problem, please try again")
        return video.as_data()