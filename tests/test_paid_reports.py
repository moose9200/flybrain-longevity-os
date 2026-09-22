"""RED: paid dossiers gate exact scores by plan (no IO, no network)."""
import pytest

from src.paid_reports import build_dossier, dossier_filename


def test_free_teaser_hides_exact_score():
    out = build_dossier("luteolin", 15.1, "dopamine_reward;insulin_mtor", "A", "free")
    assert "15.1" not in out
    assert "15,1" not in out


def test_free_teaser_shows_band_and_cta():
    out = build_dossier("luteolin", 15.1, "dopamine_reward;insulin_mtor", "A", "free")
    assert "quartile" in out.lower()
    assert "upgrade" in out.lower()


def test_researcher_shows_exact_score():
    out = build_dossier("luteolin", 15.1, "dopamine_reward;insulin_mtor", "A", "researcher")
    assert "15.1" in out
    assert "dopamine_reward" in out
    assert "insulin_mtor" in out


def test_researcher_has_grade_methods_ccby():
    out = build_dossier("luteolin", 15.1, "dopamine_reward", "A", "researcher")
    assert "A" in out
    assert "CC-BY" in out
    assert "method" in out.lower()


def test_brand_includes_claim_support_dois():
    doi = "10.3389/fnut.2026.1909085"
    out = build_dossier("luteolin", 15.1, "dopamine_reward", "A", "brand", source_dois=[doi])
    assert "claim-support" in out.lower() or "claim support" in out.lower()
    assert doi in out


def test_unknown_plan_raises():
    with pytest.raises(ValueError):
        build_dossier("luteolin", 15.1, "dopamine_reward", "A", "enterprise")


def test_filename_safe():
    name = dossier_filename("Luteolin 50uM/Oregon-R", "researcher")
    assert " " not in name
    assert "/" not in name
    assert "\\" not in name
    assert name.endswith(".md")
    assert "luteolin" in name.lower()
    assert "researcher" in name.lower()


def test_disclaimer_present_all_outputs():
    for plan, kwargs in [
        ("free", {}),
        ("researcher", {}),
        ("brand", {"source_dois": ["10.3389/fnut.2026.1909085"]}),
    ]:
        out = build_dossier("luteolin", 15.1, "dopamine_reward", "A", plan, **kwargs)
        assert "UNVERIFIED" in out
