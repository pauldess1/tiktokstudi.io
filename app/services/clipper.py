import os
import uuid
import subprocess

def extract_clip(video_path, start_sec, duration_sec, output_path=None):
    """
    Extrait un clip d'une vidéo avec ffmpeg (rapide et robuste).
    """
    if output_path is None:
        os.makedirs("./clips", exist_ok=True)
        output_path = f"./clips/{uuid.uuid4()}.mp4"

    cmd = [
        'ffmpeg',
        '-y',                     # overwrite
        '-ss', str(start_sec),    # start
        '-i', video_path,         # input
        '-t', str(duration_sec),  # duration
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'veryfast',    # faster for server workloads
        '-movflags', '+faststart', # optimisation streaming
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🎬 Clip extrait : {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return None
