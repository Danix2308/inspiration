"""Fetch a reel/video's metadata + local transcript, print COMPACT JSON (keeps tokens low).
Usage: python -P fetch_reel.py <url>
Needs: yt-dlp, ffmpeg, faster-whisper (all local, free).
"""
import json, os, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
url = sys.argv[1]
out = {"url": url}

try:
    meta = json.loads(subprocess.run(
        ["yt-dlp", "--skip-download", "--dump-json", "--no-warnings", url],
        capture_output=True, text=True, encoding="utf-8", timeout=90).stdout)
    d = meta.get("upload_date") or ""
    cap = (meta.get("description") or "").strip()
    first = next((l.strip() for l in cap.splitlines() if l.strip() and not l.strip().startswith("#")), "")
    yt_title = meta.get("title") or ""
    out.update({
        # Reels have no real title: use the caption's first line (the visible headline)
        "title": first[:120] or (yt_title if not yt_title.startswith("Video by") else None),
        "handle": meta.get("channel") or meta.get("uploader_id"),
        "posted": f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else None,
        "creator": meta.get("uploader") or meta.get("channel"),
        "duration_s": meta.get("duration"),
        "views": meta.get("view_count"),
        "likes": meta.get("like_count"),
        "caption": (meta.get("description") or "")[:800],
    })
except Exception as e:
    out["meta_error"] = str(e)[:200]

try:
    tmp = tempfile.mkdtemp()
    subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "--no-warnings", "-q",
                    "-o", os.path.join(tmp, "a.%(ext)s"), url], timeout=180, check=True)
    # Decode with ffmpeg: faster-whisper's own decoder breaks on newer PyAV (metadata_errors)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(tmp, "a.mp3"),
                          "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, timeout=120, check=True).stdout
    import numpy as np
    from faster_whisper import WhisperModel
    segs, _ = WhisperModel("base", device="cpu", compute_type="int8").transcribe(
        np.frombuffer(pcm, np.float32).copy())
    out["transcript"] = " ".join(s.text.strip() for s in segs)[:3000]
except Exception as e:
    out["transcript_error"] = str(e)[:200]

print(json.dumps(out, ensure_ascii=False))
