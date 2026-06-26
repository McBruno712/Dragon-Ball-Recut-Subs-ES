from pathlib import Path
import pysubs2

REF = Path(__file__).resolve().parent.parent / "reference" / "E01.ES.ass"


def test_e01_reference_loads():
    subs = pysubs2.load(str(REF), format_="ass")
    assert len(subs.events) > 0


def test_e01_reference_has_no_untranslated_markers():
    text = REF.read_text(encoding="utf-8")
    assert "[[LLM_TODO]]" not in text


def test_e01_reference_uses_arial():
    subs = pysubs2.load(str(REF), format_="ass")
    for name, style in subs.styles.items():
        assert style.fontname != "Avenir Black", f"Style {name} still uses Avenir Black"
