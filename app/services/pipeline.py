from services.downloader import download
from services.clipper import extract_clip
from services.converter import convert_to_tiktok

def full_pipeline(url: str, start: float, duration: float, method: str = "pad"):
    """
    Pipeline complète : download → clip → convert to TikTok
    """
    video_path = download(url)
    if video_path is None:
        return None, "Erreur lors du téléchargement"

    clip_path = extract_clip(video_path, start, duration)
    if clip_path is None:
        return None, "Erreur lors de l'extraction du clip"

    tiktok_path = convert_to_tiktok(clip_path, method=method)
    if tiktok_path is None:
        return None, "Erreur lors de la conversion TikTok"

    return tiktok_path, None
