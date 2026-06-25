import json
import subprocess
from pathlib import Path


class ExtractionError(RuntimeError):
    pass


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise ExtractionError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
        )
    return proc.stdout


def find_subtitle_stream_index(mkv: Path, language: str, codec_name: str) -> int:
    if not Path(mkv).exists():
        raise ExtractionError(f"File not found: {mkv}")
    out = _run([
        "ffprobe", "-v", "error",
        "-select_streams", "s",
        "-show_entries", "stream=index,codec_type,codec_name:stream_tags=language",
        "-of", "json",
        str(mkv),
    ])
    data = json.loads(out)
    for s in data.get("streams", []):
        if s.get("codec_type") != "subtitle":
            continue
        if s.get("codec_name") != codec_name:
            continue
        lang = s.get("tags", {}).get("language", "")
        if lang == language:
            return int(s["index"])
    raise ExtractionError(
        f"No {codec_name} subtitle with language={language!r} in {mkv}"
    )


def extract_subtitle(mkv: Path, stream_index: int, dest: Path) -> Path:
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    _run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(mkv),
        "-map", f"0:{stream_index}",
        "-c", "copy",
        str(dest),
    ])
    if not dest.exists() or dest.stat().st_size == 0:
        raise ExtractionError(f"Extraction produced empty file: {dest}")
    return dest
