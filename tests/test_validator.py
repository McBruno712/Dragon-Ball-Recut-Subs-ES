import pysubs2
import pytest
from dbsubs_lat.validator import validate, ValidationError


def _make_subs(text_pairs: list[tuple[str, str, str]]) -> pysubs2.SSAFile:
    subs = pysubs2.SSAFile()
    for start, end, text in text_pairs:
        ev = pysubs2.SSAEvent(start=int(start), end=int(end), text=text)
        subs.events.append(ev)
    return subs


def test_validate_passes_when_only_text_differs():
    original = _make_subs([("0", "1000", "Hello"), ("2000", "3000", "Bye")])
    translated = _make_subs([("0", "1000", "Hola"), ("2000", "3000", "Adiós")])
    validate(original, translated)


def test_validate_fails_on_count_mismatch():
    original = _make_subs([("0", "1000", "Hello")])
    translated = _make_subs([])
    with pytest.raises(ValidationError):
        validate(original, translated)


def test_validate_fails_on_timestamp_mismatch():
    original = _make_subs([("0", "1000", "Hello")])
    translated = _make_subs([("0", "2000", "Hola")])
    with pytest.raises(ValidationError):
        validate(original, translated)
