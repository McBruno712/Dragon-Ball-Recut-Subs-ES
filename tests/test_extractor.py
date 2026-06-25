from pathlib import Path
import pytest
from dbsubs_lat.extractor import (
    find_subtitle_stream_index,
    extract_subtitle,
    ExtractionError,
)


SAMPLE_DIR = Path("/home/mcbruno712/Videos/Películas/Dragon Ball Recut (Complete) v2")
E01 = SAMPLE_DIR / "Dragon.Ball.Recut.E01.v2.Bulma.and.Son.Goku.mkv"


@pytest.mark.skipif(not E01.exists(), reason="E01 source mkv not present")
def test_find_subtitle_stream_index_finds_eng_ass():
    idx = find_subtitle_stream_index(E01, language="eng", codec_name="ass")
    assert idx == 3


@pytest.mark.skipif(not E01.exists(), reason="E01 source mkv not present")
def test_extract_subtitle_writes_ass(tmp_path: Path):
    out = extract_subtitle(E01, stream_index=3, dest=tmp_path / "E01.ass")
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "[Events]" in text
    assert "Dialogue:" in text


def test_find_subtitle_stream_index_raises_for_missing_file(tmp_path: Path):
    with pytest.raises(ExtractionError):
        find_subtitle_stream_index(tmp_path / "nope.mkv", language="eng", codec_name="ass")
