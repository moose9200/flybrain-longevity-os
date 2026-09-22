"""RED: SEO + share-card engine (pure, zero-dep)."""
import re

from src.seo import compound_slug, compound_page, share_card, sitemap_entries

SITE = "https://flybrain-longevity-os-production.up.railway.app/"


def _row(**kw):
    base = {
        "compound": "Luteolin",
        "healthspan_score": 15.6,
        "median_lifespan_pct": 11.6,
        "evidence_grade": "A",
        "circuit_tags": "dopamine_reward;insulin_mtor",
        "dose": "50uM",
        "strain": "Oregon-R",
        "sex": "female",
        "source_doi": "10.3389/fnut.2026.1909085",
    }
    base.update(kw)
    return base


def test_slug_lower_hyphen():
    assert compound_slug("Luteolin 50uM!") == "luteolin-50um"


def test_slug_safe_chars():
    s = compound_slug("HMB-Male (10mg/mL) @ yw")
    assert re.fullmatch(r"[a-z0-9-]+", s), f"unsafe slug: {s}"
    assert " " not in s and "/" not in s


def test_page_contains_score_and_grade():
    page = compound_page(_row())
    assert "15.6" in page
    assert "A" in page


def test_page_contains_disclaimer_sources_canonical():
    page = compound_page(_row())
    assert "UNVERIFIED" in page
    assert "Janelia Male CNS v1.0" in page
    assert "FlyWire FAFB v783" in page
    assert "https://flybrain-longevity-os-production.up.railway.app/?compound=luteolin" in page


def test_page_h1_and_circuit_dose_strain_sex():
    page = compound_page(_row())
    assert page.startswith("# Luteolin longevity evidence")
    assert "dopamine_reward" in page
    assert "50uM" in page and "Oregon-R" in page and "female" in page


def test_share_card_length_url_contents():
    card = share_card(15.6, "promising", 3)
    assert len(card) <= 240, f"too long: {len(card)}"
    assert SITE in card
    assert "15.6" in card and "promising" in card


def test_share_card_no_emojis():
    card = share_card(9.0, "early", 5)
    assert card.isascii(), f"non-ascii in card: {card!r}"


def test_sitemap_count_and_entries():
    urls = sitemap_entries(["luteolin", "HMB Male"], "https://example.com")
    assert len(urls) == 2 + 2
    assert "https://example.com/" in urls
    assert "https://example.com/stack-checker" in urls
    assert "https://example.com/?compound=luteolin" in urls
    assert "https://example.com/?compound=hmb-male" in urls


def test_unknown_grade_handled():
    page = compound_page(_row(evidence_grade="Z"))
    assert "Z" in page
    assert "Unknown" in page or "unknown" in page or "early evidence" in page
