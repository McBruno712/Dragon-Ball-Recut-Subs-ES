import json
from pathlib import Path
import pytest
from dbsubs_lat.translator import is_japanese, translate_text, load_glossary


def test_is_japanese_detects_kana():
    assert is_japanese("Tsukamo ze! Doragon Booru") is True


def test_is_japanese_detects_kanji():
    assert is_japanese("悟空か?") is True


def test_is_japanese_rejects_pure_ascii():
    assert is_japanese("Let's go grab them up! The Dragon Balls!") is False


def test_is_japanese_handles_ass_override_tags():
    assert is_japanese("{\\i1}Tsukamo ze! Doragon Booru{\\i0}") is True
    assert is_japanese("{\\fad(300,0)}Kame...Hame...HA!") is False


@pytest.fixture
def glossary_path(tmp_path: Path) -> Path:
    data = {
        "Goku": "Gokú",
        "Krillin": "Krilin",
        "Dragon Balls": "Esferas del Dragón",
        "Kamehameha": "Kamehameha",
    }
    p = tmp_path / "glosario.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_load_glossary_reads_json(glossary_path: Path):
    g = load_glossary(glossary_path)
    assert g["Goku"] == "Gokú"
    assert g["Krillin"] == "Krilin"


def test_translate_text_replaces_known_terms(glossary_path: Path):
    g = load_glossary(glossary_path)
    out = translate_text("Are you really Son Goku?", g)
    assert "Gokú" in out


def test_translate_text_handles_phrase_terms(glossary_path: Path):
    g = load_glossary(glossary_path)
    out = translate_text("We need the Dragon Balls!", g)
    assert "Esferas del Dragón" in out


def test_translate_text_preserves_known_casing(glossary_path: Path):
    g = load_glossary(glossary_path)
    out = translate_text("Kamehameha!", g)
    assert "Kamehameha" in out


def test_translate_text_empty_returns_empty(glossary_path: Path):
    g = load_glossary(glossary_path)
    assert translate_text("", g) == ""


from dbsubs_lat.translator import split_long_line


def test_split_long_line_short_passes_through():
    assert split_long_line("Hola mundo", max_chars=42) == "Hola mundo"


def test_split_long_line_splits_on_space():
    long_text = (
        "Esta es una línea muy larga que necesita ser dividida en dos renglones "
        "para que entre bien en pantalla"
    )
    out = split_long_line(long_text, max_chars=42)
    assert "\n" in out
    for piece in out.split("\n"):
        assert len(piece) <= 42


def test_split_long_line_handles_no_spaces():
    out = split_long_line("abcdefghij" * 6, max_chars=20)
    assert "\n" in out
    for piece in out.split("\n"):
        assert len(piece) <= 20


def test_split_long_line_handles_ass_tags():
    out = split_long_line(
        "{\\i1}Esta es una línea italizada bastante larga para dividir correctamente{\\i0}",
        max_chars=30,
    )
    assert "\n" in out
