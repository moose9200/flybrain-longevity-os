"""RED: billing entitlements + Stripe checkout links (no network)."""
import os

from src.billing import PLANS, checkout_url, entitlements, has_access


def test_free_flags():
    ent = entitlements("free")
    assert ent["leaderboard_top_10"] is True
    assert ent["full_csv"] is False
    assert ent["unlimited_reports"] is False
    assert ent["reports_per_month"] == 1


def test_researcher_flags():
    ent = entitlements("researcher")
    assert ent["full_csv"] is True
    assert ent["unlimited_reports"] is True
    assert ent["circuit_queries"] is True


def test_brand_flags():
    ent = entitlements("brand")
    assert ent["screening_dossier"] is True
    assert ent["claim_support_pack"] is True


def test_checkout_url_empty_without_env(monkeypatch):
    for plan in ("free", "researcher", "brand"):
        monkeypatch.delenv(f"STRIPE_LINK_{plan.upper()}", raising=False)
    assert checkout_url("researcher") == ""
    assert checkout_url("brand") == ""


def test_checkout_url_uses_env_when_set(monkeypatch):
    monkeypatch.setenv("STRIPE_LINK_RESEARCHER", "https://buy.stripe.com/test_researcher")
    assert checkout_url("researcher") == "https://buy.stripe.com/test_researcher"
    monkeypatch.setenv("STRIPE_LINK_BRAND", "https://buy.stripe.com/test_brand")
    assert checkout_url("brand", base_url="https://example.com") == "https://buy.stripe.com/test_brand"


def test_has_access_true_cases():
    assert has_access("researcher", "full_csv") is True
    assert has_access("brand", "screening_dossier") is True
    assert has_access("free", "leaderboard_top_10") is True


def test_has_access_false_cases():
    assert has_access("free", "full_csv") is False
    assert has_access("free", "screening_dossier") is False
    assert has_access("researcher", "screening_dossier") is False
    assert has_access("unknown_plan", "full_csv") is False
    assert has_access("free", "unknown_feature") is False


def test_plans_gbp_prices():
    assert PLANS["researcher"]["price_gbp"] == 19
    assert PLANS["brand"]["price_gbp"] == 299
    assert PLANS["free"]["price_gbp"] == 0
