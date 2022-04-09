from starlette.exceptions import HTTPException

from app.main import main_app
from app.shortcuts import render

@main_app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "error.html"
    context = {"status_code":status_code}
    return render(request, template_name, context)