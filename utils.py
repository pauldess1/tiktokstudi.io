import yt_dlp
import os

def telecharger_youtube_mp4(url_youtube, chemin_sortie='./videos'):
    """
    Télécharge une vidéo YouTube dans la meilleure qualité MP4 possible.
    """
    if not os.path.exists(chemin_sortie):
        os.makedirs(chemin_sortie)
        
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
        'recode-video': 'mp4',
        'outtmpl': os.path.join(chemin_sortie, '%(id)s.%(ext)s'),
        'quiet': True,
        'noprogress': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_youtube, download=True)
            chemin_fichier_telecharge = ydl.prepare_filename(info)
            print(f"✅ Téléchargement réussi : {chemin_fichier_telecharge}")
            return chemin_fichier_telecharge

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de l'URL : {url_youtube}")
        print(f"Détails de l'erreur : {e}")
        return None