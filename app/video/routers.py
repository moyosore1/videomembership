from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse


from app.shortcuts import redirect, render, get_object_or_404
from app.users.decorators import login_required
from app import utils

from .schemas import VideoSchema
from .models import Video

router = APIRouter(
    prefix="/videos"
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, 'videos/create.html', {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post(request: Request, title: str =Form(...),  url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, VideoSchema)
    context = {
        "data":data,
        "errors":errors,
        "url": url
    }
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
    redirect_path = data.get('path') or "/videos/create"
    return redirect(redirect_path)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    qs = Video.objects.all().limit(100)
    context = {
        "videos": qs
    }
    return render(request, 'videos/list.html', context)


@router.get("/detail/{host_id}", response_class=HTMLResponse)
def video_detail_view(request: Request, host_id: str):
    video = get_object_or_404(Video, host_id=host_id)
    context = {
        "host_id": host_id,
        "video":video
    }
    return render(request, 'videos/list.html', context)


