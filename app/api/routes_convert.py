from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.converter import convert_to_tiktok

router = APIRouter()

class ConvertRequest(BaseModel):
    clip_path: str
    method: str = "crop"

@router.post("/")
def convert_clip(req: ConvertRequest):
    """
    Convertit un clip en format TikTok vertical.
    """
    try:
        tiktok_path = convert_to_tiktok(input_path=req.clip_path, method=req.method)
        if tiktok_path is None:
            raise HTTPException(status_code=500, detail="Conversion TikTok échouée")
        return {"status": "success", "tiktok_path": tiktok_path}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {e}")
