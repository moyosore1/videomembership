from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse


from app.shortcuts import redirect, render, get_object_or_404
from app.users.decorators import login_required
from app import utils
from app.watch.models import WatchEvent

from .schemas import VideoSchema
from .models import Video

router = APIRouter(
    prefix="/videos"
)



def is_htmx(request:Request):
    return request.headers.get("hx-request") == 'true'

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request, is_htmx=Depends(is_htmx)):
    
    if is_htmx:
        return render(request, "videos/htmx/create.html")
    return render(request, 'videos/create.html', {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post(request: Request, is_htmx=Depends(is_htmx), title: str = Form(...),  url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, VideoSchema)
    redirect_path = data.get('path') or "/videos/create"
    if is_htmx:
        if len(errors) > 0:
            return render(request, "videos/htmx/create.html", context)
        context = {"path":redirect_path, "title":data.get('title')}
        return render(request, "videos/htmx/link.html", context)
    context = {
        "data":data,
        "errors":errors,
        "url": url
    }
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
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
    start_time = 0
    if request.user.is_authenticated:
        user_id = request.user.username
        start_time = WatchEvent.get_resume_time(host_id, user_id)
    context = {
        "host_id": host_id,
        "start_time": start_time,
        "video":video
    }
    return render(request, 'videos/list.html', context)


