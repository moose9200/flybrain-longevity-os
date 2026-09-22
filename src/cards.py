"""Share cards: SVG (stdlib) + PNG (Pillow)."""
from xml.sax.saxutils import escape

SITE = "https://flybrain-longevity-os-production.up.railway.app/"
WIDTH = 1200
HEIGHT = 630
BG = "#0B1020"


def _text(value) -> str:
    return escape(str(value), {'"': "&quot;"})


def score_card_svg(compound_or_stack, score, verdict) -> str:
    """Return 1200x630 SVG share card (dark bg, no external assets)."""
    label = _text(compound_or_stack)
    score_s = _text(score)
    verdict_s = _text(verdict)
    site_s = _text(SITE)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>'
        f'<rect x="24" y="24" width="{WIDTH - 48}" height="{HEIGHT - 48}" fill="none" '
        f'stroke="#334155" stroke-width="2"/>'
        f'<text x="80" y="150" font-family="sans-serif" font-size="44" fill="#E2E8F0">{label}</text>'
        f'<text x="80" y="360" font-family="sans-serif" font-size="160" '
        f'font-weight="bold" fill="#FFFFFF">{score_s}</text>'
        f'<text x="80" y="450" font-family="sans-serif" font-size="56" fill="#93C5FD">{verdict_s}</text>'
        f'<text x="80" y="550" font-family="sans-serif" font-size="28" fill="#94A3B8">{site_s}</text>'
        f"</svg>"
    )


def score_card_png(compound_or_stack, score, verdict) -> bytes:
    """Return 1200x630 PNG share card bytes (requires Pillow)."""
    from io import BytesIO

    from PIL import Image, ImageDraw

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([24, 24, WIDTH - 24, HEIGHT - 24], outline=(51, 65, 85), width=2)
    draw.text((80, 90), str(compound_or_stack), fill=(226, 232, 240))
    draw.text((80, 200), str(score), fill=(255, 255, 255))
    draw.text((80, 330), str(verdict), fill=(147, 197, 253))
    draw.text((80, 550), SITE, fill=(148, 163, 184))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
