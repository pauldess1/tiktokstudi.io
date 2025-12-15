from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.routes_download import router as download_router
from api.routes_clip import router as clip_router
from api.routes_convert import router as convert_router
from api.routes_full import router as full_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def landing(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {"request": request}
    )

app.include_router(download_router, prefix="/download")
app.include_router(clip_router, prefix="/clip")
app.include_router(convert_router, prefix="/convert")
app.include_router(full_router, prefix="/full")