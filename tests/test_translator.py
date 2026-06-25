from dbsubs_lat.translator import is_japanese


def test_is_japanese_detects_kana():
    assert is_japanese("Tsukamo ze! Doragon Booru") is True


def test_is_japanese_detects_kanji():
    assert is_japanese("悟空か?") is True


def test_is_japanese_rejects_pure_ascii():
    assert is_japanese("Let's go grab them up! The Dragon Balls!") is False


def test_is_japanese_handles_ass_override_tags():
    assert is_japanese("{\\i1}Tsukamo ze! Doragon Booru{\\i0}") is True
    assert is_japanese("{\\fad(300,0)}Kame...Hame...HA!") is False
