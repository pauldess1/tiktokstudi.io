from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.pipeline import full_pipeline

router = APIRouter()

class FullPipelineRequest(BaseModel):
    url: str
    start: float
    duration: float
    method: str = "pad"

@router.post("/")
def process_full(req: FullPipelineRequest):
    """
    Pipeline complète : download → clip → convert TikTok
    """
    tiktok_path, error = full_pipeline(req.url, req.start, req.duration, req.method)
    if error:
        raise HTTPException(status_code=500, detail=error)

    return {
        "status": "success",
        "tiktok_path": tiktok_path
    }
