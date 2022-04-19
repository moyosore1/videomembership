from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse


from app.shortcuts import redirect, render
from app.users.decorators import login_required
from app import utils

from .schemas import VideoSchema

router = APIRouter(
    prefix="/videos"
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, 'videos/create.html', {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post(request: Request, url: str = Form(...)):
    raw_data = {
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
    return render(request, 'videos/list.html', {})


