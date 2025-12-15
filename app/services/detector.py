import subprocess
import librosa
import numpy as np

def smooth_signal(signal, window=5):
    return np.convolve(signal, np.ones(window)/window, mode='same')

def extract_audio(video_path, audio_path="./temp/audio.wav"):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path


def compute_energy(audio_path, frame_duration=0.5):
    y, sr = librosa.load(audio_path, sr=16000)
    frame_len = int(frame_duration * sr)
    energies = []

    for i in range(0, len(y), frame_len):
        frame = y[i:i+frame_len]
        if len(frame) == 0:
            continue
        rms = np.sqrt(np.mean(frame**2))
        energies.append(rms)

    return np.array(energies)

def detect_energy_peaks(energies, k=3):
    median = np.median(energies)
    mad = np.median(np.abs(energies - median)) + 1e-6
    threshold = median + k * mad

    return [i for i, e in enumerate(energies) if e > threshold]

def cluster_indices(indices, max_gap=3):
    clusters = []
    current = []

    for i in indices:
        if not current or i - current[-1] <= max_gap:
            current.append(i)
        else:
            clusters.append(current)
            current = [i]

    if current:
        clusters.append(current)

    return [cluster[len(cluster)//2] for cluster in clusters]

def detect_pause_then_peak(energies, pause_ratio=0.6, spike_ratio=1.4):
    mean = np.mean(energies)
    moments = []

    for i in range(1, len(energies)):
        if energies[i-1] < mean * pause_ratio and energies[i] > mean * spike_ratio:
            moments.append(i)

    return moments

def frames_to_timestamps(frames, frame_duration=0.5):
    return [round(f * frame_duration, 2) for f in frames]

def format_timestamp(seconds: float):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def detect_highlights(video_path):
    audio_path = extract_audio(video_path)
    
    energies = compute_energy(audio_path)

    # Smooth
    smooth = smooth_signal(energies, window=5)

    # Peaks (MAD-based)
    peaks = detect_energy_peaks(smooth, k=3)

    # Pause → spike
    pauses = detect_pause_then_peak(smooth)

    # Combine + cluster (SUPER IMPORTANT)
    combined = sorted(list(set(peaks + pauses)))
    centers = cluster_indices(combined, max_gap=4)

    timestamps = frames_to_timestamps(centers)

    return timestamps

