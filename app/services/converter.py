import os
import uuid
import subprocess

def convert_to_tiktok(input_path, output_path=None, method='pad'):
    """
    Convertit une vidéo au format vertical TikTok (1080x1920).
    method : 'pad' (bandes noires), 'crop' (centré), 'scale' (juste redimension).
    """
    if output_path is None:
        os.makedirs("./clips", exist_ok=True)
        output_path = f"./clips/tiktok_{uuid.uuid4()}.mp4"

    # Sélection du filtre vidéo selon le mode
    if method == 'pad':
        # conserve ratio → complète avec bandes
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"
        )
    elif method == 'crop':
        # zoom jusqu’à 1920px de haut puis crop en 1080
        vf = "scale=-1:1920,crop=1080:1920,setsar=1"
    elif method == 'scale':
        # full stretch vertical
        vf = "scale=1080:-1,setsar=1"
    else:
        raise ValueError("method doit être 'pad', 'crop' ou 'scale'")

    cmd = [
        'ffmpeg',
        '-y',
        '-i', input_path,
        '-vf', vf,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'veryfast',
        '-movflags', '+faststart',  # important pour TikTok/Reels
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"📱 Vidéo format TikTok ({method}) : {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la conversion TikTok : {e}")
        return None
