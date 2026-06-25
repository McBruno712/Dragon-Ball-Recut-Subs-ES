import re

_TAG_RE = re.compile(r"\{[^}]*\}")

_CJK_RANGES = (
    (0x3040, 0x30FF),
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
)

_ROMAJI_KEYWORDS = (
    "tsukamo",
    "doragon booru",
    "doragon bōru",
    "kamehameha",
    "kame hame ha",
    "kame hame",
    "goku",
    "gohan",
    "vegeta",
    "piccolo",
    "frieza",
    "nappa",
    "raditz",
    "kakarrot",
    "senzu",
    "shenron",
)


def _strip_tags(text: str) -> str:
    return _TAG_RE.sub("", text or "")


def _has_japanese_char(text: str) -> bool:
    for ch in text:
        cp = ord(ch)
        for lo, hi in _CJK_RANGES:
            if lo <= cp <= hi:
                return True
    return False


def _has_romaji_keyword(text: str) -> bool:
    lowered = text.lower()
    return any(kw in lowered for kw in _ROMAJI_KEYWORDS)


def is_japanese(text: str) -> bool:
    stripped = _strip_tags(text)
    return _has_japanese_char(stripped) or _has_romaji_keyword(stripped)
