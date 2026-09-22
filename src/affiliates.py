"""Affiliate slots — generic, env-configured, ASA-disclosed. No network."""
import os

AFFILIATE_PROGRAMS = [
    {
        "name": "Supplement Retailer A",
        "url_env_var": "AFFILIATE_URL_RETAILER_A",
        "disclosure": "Links may earn commission at no extra cost to you.",
    },
    {
        "name": "Lab Supplier B",
        "url_env_var": "AFFILIATE_URL_LAB_B",
        "disclosure": "Links may earn commission at no extra cost to you.",
    },
    {
        "name": "Wellness Marketplace C",
        "url_env_var": "AFFILIATE_URL_MARKETPLACE_C",
        "disclosure": "Links may earn commission at no extra cost to you.",
    },
]


def disclosure_banner() -> str:
    """UK ASA-compliant affiliate disclosure, one paragraph."""
    return (
        "Disclosure: some links on this page are affiliate links, which means "
        "FlyBrain Longevity OS may earn a commission if you buy through them at "
        "no extra cost to you; this does not affect our rankings, which are based "
        "solely on Drosophila lifespan, climbing and stress data."
    )


def get_affiliate_urls() -> dict:
    """Resolve affiliate URLs from env vars. No defaults, no network."""
    return {p["name"]: os.getenv(p["url_env_var"], "") for p in AFFILIATE_PROGRAMS}


def attach_links(compound: dict) -> tuple:
    """Pure: return (unchanged compound copy, disclosure flag). No network."""
    return dict(compound), True
