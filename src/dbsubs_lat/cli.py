from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .batch import run_batch, run_pilot
from .translator import load_glossary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Translate DB Recut English ASS subs to ES-LAT")
    p.add_argument("--videos-dir", required=True, type=Path)
    p.add_argument("--pilot", default=None, help="e.g. E01 (pilot mode, single episode)")
    p.add_argument("--batch", default=None, help="e.g. E02-E21 (batch range)")
    p.add_argument(
        "--glossary", type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "data" / "glosario_latino.json",
    )
    p.add_argument("--log-dir", type=Path, default=Path("logs"))
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.pilot and not args.batch:
        print("Specify --pilot E## or --batch E##-E##", file=sys.stderr)
        return 2

    glossary = load_glossary(args.glossary)

    if args.pilot:
        return run_pilot(args.pilot, args.videos_dir, glossary, args.log_dir)

    return run_batch(args.batch, args.videos_dir, glossary, args.log_dir)


if __name__ == "__main__":
    raise SystemExit(main())
