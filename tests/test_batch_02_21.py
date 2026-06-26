"""Lock in approved ES translations for batch E02-E21."""
from pathlib import Path
import pysubs2
import pytest

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / "reference"

BATCH = list(range(2, 12))  # E02 to E11 (first half of batch 1)


@pytest.mark.parametrize("ep_num", BATCH)
def test_reference_loads(ep_num: int):
    path = REF_DIR / f"E{ep_num:02d}.ES.ass"
    assert path.exists(), f"Missing reference: {path}"
    subs = pysubs2.load(str(path), format_="ass")
    assert len(subs.events) > 0


@pytest.mark.parametrize("ep_num", BATCH)
def test_reference_has_no_untranslated_markers(ep_num: int):
    path = REF_DIR / f"E{ep_num:02d}.ES.ass"
    text = path.read_text(encoding="utf-8")
    assert "[[LLM_TODO]]" not in text


@pytest.mark.parametrize("ep_num", BATCH)
def test_reference_uses_arial(ep_num: int):
    path = REF_DIR / f"E{ep_num:02d}.ES.ass"
    subs = pysubs2.load(str(path), format_="ass")
    for name, style in subs.styles.items():
        assert style.fontname != "Avenir Black", (
            f"E{ep_num:02d} style {name} still uses Avenir Black"
        )
