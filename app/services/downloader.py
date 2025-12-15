import os
import uuid
import yt_dlp


def download(url: str):
    """
    Télécharge une vidéo YouTube dans la meilleure qualité MP4 possible.
    """
    os.makedirs("./videos", exist_ok=True)

    output_path = f"./videos/{uuid.uuid4()}.mp4"

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "quiet": True,
        "noprogress": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✅ Téléchargement réussi : {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        return None
