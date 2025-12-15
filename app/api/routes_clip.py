from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.clipper import extract_clip

router = APIRouter()

class ClipRequest(BaseModel):
    video_path: str
    start: float
    duration: float


@router.post("/")
def create_clip(req: ClipRequest):
    """
    Extrait un clip depuis une vidéo déjà téléchargée.
    """
    output = extract_clip(
        video_path=req.video_path,
        start_sec=req.start,
        duration_sec=req.duration
    )

    if output is None:
        raise HTTPException(status_code=500, detail="Clip extraction failed.")

    return {
        "status": "success",
        "clip_path": output
    }
