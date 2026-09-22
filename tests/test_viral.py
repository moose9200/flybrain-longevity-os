"""RED: viral-loop engine — referral codes, links, shares, leaderboard, challenge."""
import string

from src import viral as v


def test_referral_code_deterministic():
    assert v.referral_code("Hemant") == v.referral_code("Hemant")
    assert v.referral_code("Hemant") == v.referral_code("hemant")


def test_referral_code_8char_alnum_lowercase():
    code = v.referral_code("Tash")
    assert len(code) == 8
    assert code == code.lower()
    assert all(c in string.ascii_lowercase + string.digits for c in code)
    assert v.referral_code("Sean") != v.referral_code("Harry")


def test_referral_link_format():
    code = "abcd1234"
    link = v.referral_link(code)
    assert link == f"https://flybrain-longevity-os-production.up.railway.app/?ref={code}"
    custom = v.referral_link(code, base_url="https://example.co.uk/")
    assert custom == f"https://example.co.uk/?ref={code}"


def test_record_share_leaderboard_roundtrip(tmp_path):
    store = str(tmp_path / "shares.json")
    v.record_share(store, "aaaabbbb", 12.5)
    v.record_share(store, "ccccdddd", 20.0)
    lb = v.leaderboard(store)
    assert len(lb) == 2
    assert lb[0]["code"] == "ccccdddd"
    assert lb[0]["score"] == 20.0


def test_leaderboard_best_per_code_dedupe(tmp_path):
    store = str(tmp_path / "shares.json")
    v.record_share(store, "aaaabbbb", 10.0)
    v.record_share(store, "aaaabbbb", 30.0)
    v.record_share(store, "aaaabbbb", 20.0)
    lb = v.leaderboard(store)
    assert len(lb) == 1
    assert lb[0]["score"] == 30.0


def test_leaderboard_sorted_desc_and_top_n(tmp_path):
    store = str(tmp_path / "nested" / "shares.json")
    for i in range(5):
        v.record_share(store, f"code000{i}", float(i))
    lb = v.leaderboard(store, top_n=3)
    assert len(lb) == 3
    scores = [e["score"] for e in lb]
    assert scores == sorted(scores, reverse=True)
    assert scores[0] == 4.0


def test_record_share_tolerates_corrupt_file(tmp_path):
    store = tmp_path / "shares.json"
    store.write_text("not valid json {{{")
    v.record_share(str(store), "eeefffff", 7.5)
    lb = v.leaderboard(str(store))
    assert len(lb) == 1
    assert lb[0] == {"code": "eeefffff", "score": 7.5} or (
        lb[0]["code"] == "eeefffff" and lb[0]["score"] == 7.5
    )


def test_challenge_text_contains_week_label():
    text = v.challenge_text("Week 12")
    assert "Week 12" in text
    assert "Beat last week's top stack" in text
    lowered = text.lower()
    assert "optimise" in lowered or "optimize" not in lowered
    assert "emoji" not in lowered
    for ch in ["😀", "🚀", "🎉", "🔥", "💪"]:
        assert ch not in text
