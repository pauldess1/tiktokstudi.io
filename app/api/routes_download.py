from fastapi import APIRouter
from pydantic import BaseModel
from services.downloader import download

router = APIRouter()

class DownloadRequest(BaseModel):
    url: str

@router.post("/")
def download_video(request: DownloadRequest):
    video_path = download(request.url)
    return {"status": "ok", "path": video_path}