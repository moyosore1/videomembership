from distutils.command.config import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


from app.config import get_settings

settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


# like django!
def render(request, template_name, context={}, status_code: int = 200):
    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    return response
    # return templates.TemplateResponse(template_name, ctx, status_code=status_code)
