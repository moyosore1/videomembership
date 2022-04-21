from starlette.exceptions import HTTPException as StarletteHTTPException

from app.main import main_app
from app.shortcuts import redirect, render, is_htmx
from app.users.exceptions import LoginRequiredException


@main_app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "error.html"
    context = {"status_code":status_code}
    return render(request, template_name, context)


@main_app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exc):
    response = redirect(f"/login?next={request.url}", remove_session=True)
    if is_htmx(request):
        response.status_code = 200
        response.headers["HX-Redirect"] = "/login"
    return response
