"""Billing plans + entitlements + Stripe Payment Links (zero-dep, no network)."""
import os

PLANS = {
    "free": {
        "name": "Free",
        "price_gbp": 0,
        "interval": "forever",
        "description": "Leaderboard top 10 and 1 report per month. Behaviour summaries optimised for curiosity.",
    },
    "researcher": {
        "name": "Researcher",
        "price_gbp": 19,
        "interval": "month",
        "description": "Full 51-compound CSV, unlimited reports and circuit queries. Optimised for research behaviour.",
    },
    "brand": {
        "name": "Brand",
        "price_gbp": 299,
        "interval": "report",
        "description": "Screening dossier plus claim-support pack. Organised evidence summaries with optimised behaviour notes.",
    },
}

_ENTITLEMENTS = {
    "free": {
        "leaderboard_top_10": True,
        "full_csv": False,
        "unlimited_reports": False,
        "circuit_queries": False,
        "screening_dossier": False,
        "claim_support_pack": False,
        "reports_per_month": 1,
    },
    "researcher": {
        "leaderboard_top_10": True,
        "full_csv": True,
        "unlimited_reports": True,
        "circuit_queries": True,
        "screening_dossier": False,
        "claim_support_pack": False,
        "reports_per_month": 0,
    },
    "brand": {
        "leaderboard_top_10": True,
        "full_csv": False,
        "unlimited_reports": False,
        "circuit_queries": False,
        "screening_dossier": True,
        "claim_support_pack": True,
        "reports_per_month": 1,
    },
}


def entitlements(plan: str) -> dict:
    return dict(_ENTITLEMENTS.get(str(plan).lower(), {}))


def checkout_url(plan: str, base_url: str = "") -> str:
    _ = base_url
    key = f"STRIPE_LINK_{str(plan).upper()}"
    return os.getenv(key, "") or ""


def has_access(plan: str, feature: str) -> bool:
    return bool(entitlements(plan).get(feature, False))
