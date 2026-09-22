"""RED: promo codes + referral rewards (stdlib only)."""
import string

from src import promo as p


def test_make_code_deterministic():
    assert p.make_code("Hemant", "launch") == p.make_code("Hemant", "launch")
    assert p.make_code("Hemant", "launch") == p.make_code("hemant", "launch")


def test_make_code_10char_alnum():
    code = p.make_code("Tash", "launch")
    assert len(code) == 10
    assert all(c in string.ascii_letters + string.digits for c in code)


def test_make_code_diff_campaign_diff_code():
    assert p.make_code("Hemant", "launch") != p.make_code("Hemant", "refer_5")
    assert p.make_code("Hemant", "top3") != p.make_code("Sean", "top3")


def test_unknown_campaign_false():
    res = p.redeem(None, "ZZZZZZZZZZ", "Hemant")
    assert res["ok"] is False


def test_valid_redeem_true_no_store():
    code = p.make_code("Hemant", "launch")
    res = p.redeem(None, code, "Hemant")
    assert res["ok"] is True
    assert isinstance(res["reward"], str) and res["reward"] != ""


def test_valid_redeem_all_campaigns_no_store():
    for campaign in ["launch", "refer_5", "top3"]:
        code = p.make_code("Taya", campaign)
        res = p.redeem(None, code, "Taya")
        assert res["ok"] is True, campaign
        assert res["reward"] != ""


def test_duplicate_rejected(tmp_path):
    store = str(tmp_path / "promo.json")
    code = p.make_code("Sean", "refer_5")
    first = p.redeem(store, code, "Sean")
    assert first["ok"] is True
    second = p.redeem(store, code, "Sean")
    assert second["ok"] is False
    assert second.get("reason") == "duplicate"


def test_no_store_mode_no_duplicate_tracking():
    code = p.make_code("Harry", "top3")
    assert p.redeem(None, code, "Harry")["ok"] is True
    assert p.redeem(None, code, "Harry")["ok"] is True


def test_rewards_text_non_empty():
    assert set(p.REWARDS) == {"leaderboard_top3", "first_share", "refer_5"}
    for key, val in p.REWARDS.items():
        assert isinstance(val, str) and val.strip() != "", key
