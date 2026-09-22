"""RED: affiliates — ASA disclosure + pure link attach, no network, env URLs."""
import copy

from src import affiliates


def test_disclosure_non_empty_mentions_affiliate():
    banner = affiliates.disclosure_banner()
    assert isinstance(banner, str)
    assert banner.strip() != ""
    assert "affiliate" in banner.lower()


def test_attach_links_pure_returns_unchanged_plus_flag():
    compound = {"compound": "luteolin", "median_lifespan_pct": 11.6}
    snapshot = copy.deepcopy(compound)
    result = affiliates.attach_links(compound)
    # contract: (compound_copy, disclosure_flag)
    assert isinstance(result, tuple) and len(result) == 2
    out_compound, disclosure = result
    assert out_compound == snapshot
    assert compound == snapshot  # input not mutated
    assert out_compound is not compound
    assert disclosure is True


def test_env_override_via_monkeypatch(monkeypatch):
    prog = affiliates.AFFILIATE_PROGRAMS[0]
    env_var = prog["url_env_var"]
    monkeypatch.setenv(env_var, "https://example.com/aff?tag=test123")
    urls = affiliates.get_affiliate_urls()
    assert urls[prog["name"]] == "https://example.com/aff?tag=test123"
    monkeypatch.delenv(env_var, raising=False)
    urls_empty = affiliates.get_affiliate_urls()
    assert urls_empty[prog["name"]] == ""


def test_programs_list_has_three_entries():
    assert isinstance(affiliates.AFFILIATE_PROGRAMS, list)
    assert len(affiliates.AFFILIATE_PROGRAMS) >= 3


def test_programs_entries_have_required_fields():
    for prog in affiliates.AFFILIATE_PROGRAMS:
        assert prog["name"]
        assert prog["url_env_var"]
        assert prog["disclosure"]
