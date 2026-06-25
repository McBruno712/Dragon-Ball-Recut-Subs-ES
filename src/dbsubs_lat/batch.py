"""Orchestrate mark+place phases for a pilot or a range of episodes."""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pysubs2

from .extractor import extract_subtitle, find_subtitle_stream_index, ExtractionError
from .translator import is_japanese, split_long_line
from .validator import validate, ValidationError


_EP_RE = re.compile(r"\.E(\d{2,3})\.")


def _episode_number(mkv: Path) -> str:
    m = _EP_RE.search(mkv.name)
    if not m:
        raise ValueError(f"Could not extract episode number from {mkv.name}")
    return m.group(1)


def _log(report: list[str], line: str) -> None:
    print(line)
    report.append(line)


def _process_one(
    mkv: Path,
    glossary: dict[str, str],
    videos_dir: Path,
    log_dir: Path,
) -> Path:
    ep = _episode_number(mkv)
    report: list[str] = []
    _log(report, f"=== {mkv.name} ===")

    sidx = find_subtitle_stream_index(mkv, language="eng", codec_name="ass")
    _log(report, f"subtitle stream index: {sidx}")
    with tempfile.TemporaryDirectory() as tmpd:
        tmp = Path(tmpd) / f"E{ep}.ass"
        extract_subtitle(mkv, stream_index=sidx, dest=tmp)
        original = pysubs2.load(str(tmp), format_="ass")

        translated = pysubs2.SSAFile()
        translated.info = original.info
        translated.styles = original.styles.copy()
        translated.fonts_opaque = original.fonts_opaque
        translated.graphics_opaque = original.graphics_opaque

        for name, style in translated.styles.items():
            if style.fontname == "Avenir Black":
                style.fontname = "Arial"
        _log(report, f"styles rewritten: {len(translated.styles)}")

        n_jap = n_eng = n_split = 0
        for ev in original.events:
            new_ev = pysubs2.SSAEvent(
                start=ev.start, end=ev.end, text=ev.text,
                style=ev.style, name=ev.name, marginl=ev.marginl,
                marginr=ev.marginr, marginv=ev.marginv, effect=ev.effect,
                layer=ev.layer,
            )
            if is_japanese(ev.text):
                n_jap += 1
            else:
                n_eng += 1
                replaced = ev.text
                for en, es in glossary.items():
                    replaced = re.sub(
                        rf"(?<![A-Za-z0-9_]){re.escape(en)}(?![A-Za-z0-9_])",
                        es, replaced,
                    )
                if len(replaced) > 42:
                    replaced = split_long_line(replaced, max_chars=42)
                    n_split += 1
                replaced = f"[[LLM_TODO]] {replaced}"
                new_ev.text = replaced
            translated.events.append(new_ev)

        validate(original, translated)
        _log(report, "validation: OK")

        out_path = videos_dir / f"{mkv.stem}.ES.ass"
        translated.save(str(out_path), format_="ass")
        _log(report, f"wrote: {out_path.name}")

    _log(report, f"japanese preserved: {n_jap}")
    _log(report, f"english lines marked for LLM: {n_eng}")
    _log(report, f"lines needing length split: {n_split}")
    _log(report, "")
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"E{ep}.txt").write_text("\n".join(report), encoding="utf-8")
    return out_path


def run_pilot(ep: str, videos_dir: Path, glossary: dict[str, str], log_dir: Path) -> int:
    ep = ep.upper()
    if not ep.startswith("E"):
        print("--pilot must look like E01, E02, ...", file=sys.stderr)
        return 2
    candidates = sorted(videos_dir.glob(f"*.Recut.{ep}.v2.*.mkv"))
    if not candidates:
        print(f"No mkv found for {ep} in {videos_dir}", file=sys.stderr)
        return 1
    rc = 0
    for mkv in candidates:
        try:
            _process_one(mkv, glossary, videos_dir, log_dir)
        except (ExtractionError, ValidationError) as e:
            print(f"FAILED {mkv.name}: {e}", file=sys.stderr)
            rc = 1
    return rc


def run_batch(batch: str, videos_dir: Path, glossary: dict[str, str], log_dir: Path) -> int:
    m = re.match(r"^E(\d{2,3})-E(\d{2,3})$", batch)
    if not m:
        print("--batch must look like E02-E21", file=sys.stderr)
        return 2
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo > hi:
        print("--batch range is empty", file=sys.stderr)
        return 2
    rc = 0
    for ep_num in range(lo, hi + 1):
        ep = f"E{ep_num:02d}"
        out_marker = videos_dir / f"*.Recut.{ep}.v2.*.ES.ass"
        if any(videos_dir.glob(out_marker.name)):
            print(f"SKIP {ep}: .ES.ass already exists")
            continue
        candidates = sorted(videos_dir.glob(f"*.Recut.{ep}.v2.*.mkv"))
        if not candidates:
            print(f"SKIP {ep}: no mkv found")
            continue
        for mkv in candidates:
            try:
                _process_one(mkv, glossary, videos_dir, log_dir)
            except (ExtractionError, ValidationError) as e:
                print(f"FAILED {mkv.name}: {e}", file=sys.stderr)
                rc = 1
    return rc
