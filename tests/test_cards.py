"""RED: share cards — SVG (stdlib) + PNG (Pillow)."""
import xml.etree.ElementTree as ET

from src.cards import score_card_svg

SITE = "https://flybrain-longevity-os-production.up.railway.app/"


def test_svg_contains_score_verdict_url():
    svg = score_card_svg("luteolin", 15.6, "promising")
    assert "15.6" in svg
    assert "promising" in svg
    assert SITE in svg
    assert "luteolin" in svg


def test_svg_dimensions_dark_bg_no_external():
    svg = score_card_svg("my stack", 9.0, "weak")
    assert "1200" in svg and "630" in svg
    lowered = svg.lower()
    assert "#0b1020" in lowered or "#111827" in lowered or "#000" in lowered
    for token in ("<image", "xlink:href", "@import", "url(http"):
        assert token not in lowered, f"external asset token: {token}"
    assert "<svg" in lowered and "</svg>" in lowered
    ET.fromstring(svg)


def test_svg_no_emoji_ascii():
    svg = score_card_svg("luteolin", 15.6, "strong")
    assert svg.isascii(), f"non-ascii in svg: {svg[:200]!r}"
    for ch in ["\U0001F600", "\U0001F680", "\U0001F389", "\U0001F525", "\U0001F4AA", "\u2764", "\u2B50"]:
        assert ch not in svg


def test_svg_deterministic():
    a = score_card_svg("luteolin", 15.6, "promising")
    b = score_card_svg("luteolin", 15.6, "promising")
    assert a == b


def test_png_valid_signature_dimensions():
    try:
        from src.cards import score_card_png
    except ImportError:
        import pytest
        pytest.skip("Pillow missing — PNG not offered")
        return
    blob = score_card_png("luteolin", 15.6, "promising")
    assert isinstance(blob, (bytes, bytearray))
    assert bytes(blob)[:8] == b"\x89PNG\r\n\x1a\n"
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(bytes(blob)))
    assert img.size == (1200, 630)
