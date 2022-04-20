from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse


from app.shortcuts import redirect, render, get_object_or_404
from app.users.decorators import login_required
from app import utils
from app.watch.models import WatchEvent

from .schemas import PlaylistSchema
from .models import Playlist

router = APIRouter(
    prefix="/playlists"
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def playlist_create_view(request: Request):
    return render(request, 'playlists/create.html', {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def playlist_create_post(request: Request, title: str = Form(...)):
    raw_data = {
        "title": title,
        "user_id": request.user.username
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, PlaylistSchema)
    context = {
        "data": data,
        "errors": errors
    }
    if len(errors) > 0:
        return render(request, "playlists/create.html", context, status_code=400)
    obj = Playlist.objects.create(**data)
    redirect_path = obj.path or "/playlists/create"
    return redirect(redirect_path)


@router.get("/", response_class=HTMLResponse)
def playlist_list_view(request: Request):
    qs = Playlist.objects.all().limit(100)
    context = {
        "playlists": qs
    }
    return render(request, 'playlists/list.html', context)


@router.get("/detail/{db_id}", response_class=HTMLResponse)
def playlist_detail_view(request: Request, db_id: str):
    playlist = get_object_or_404(Playlist, db_id=db_id)
    
    if request.user.is_authenticated:
        user_id = request.user.username
        
    context = {
        "playlist": playlist,
        "videos": playlist.get_videos(),
    }
    return render(request, 'playlists/list.html', context)
