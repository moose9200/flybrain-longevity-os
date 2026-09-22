"""RED: viral stack-checker engine (FlyBrain Longevity OS)."""
import os

import pytest

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "compounds.csv")


def test_known_compound_scored():
    from src.stacks import check_stack
    out = check_stack(["luteolin"])
    assert len(out["scored"]) == 1
    entry = out["scored"][0]
    assert entry["compound"] == "luteolin"
    assert entry["healthspan_score"] == 16.6
    assert entry["grade"] == "A"
    assert out["unknown"] == []


def test_unknown_flagged():
    from src.stacks import check_stack
    out = check_stack(["luteolin", "not-a-real-compound-xyz"])
    assert out["unknown"] == ["not-a-real-compound-xyz"]
    assert [e["compound"] for e in out["scored"]] == ["luteolin"]


def test_empty_stack_verdict():
    from src.stacks import check_stack
    out = check_stack([])
    assert out["scored"] == []
    assert out["stack_score"] == 0.0
    assert out["verdict"] == "empty"
    assert out["redundancies"] == []


def test_weak_verdict():
    from src.stacks import check_stack
    out = check_stack(["azd8055"])
    assert out["stack_score"] < 5
    assert out["verdict"] == "weak"


def test_promising_verdict():
    from src.stacks import check_stack
    out = check_stack(["rapamycin-brewer-female"])
    assert 5 <= out["stack_score"] < 10
    assert out["verdict"] == "promising"


def test_strong_verdict():
    from src.stacks import check_stack
    out = check_stack(["luteolin"])
    assert out["stack_score"] >= 10
    assert out["verdict"] == "strong"


def test_scored_sorted_desc():
    from src.stacks import check_stack
    out = check_stack(["hmb", "luteolin"])
    scores = [e["healthspan_score"] for e in out["scored"]]
    assert scores == sorted(scores, reverse=True)
    assert out["scored"][0]["compound"] == "luteolin"


def test_stack_score_is_mean():
    from src.stacks import check_stack
    out = check_stack(["luteolin", "hmb"])
    mean = sum(e["healthspan_score"] for e in out["scored"]) / 2
    assert out["stack_score"] == pytest.approx(mean)


def test_redundancy_grouping():
    from src.stacks import check_stack
    out = check_stack(["hmb", "hmb-male"])
    assert len(out["redundancies"]) == 1
    assert sorted(out["redundancies"][0]) == ["hmb", "hmb-male"]


def test_no_redundancy_single():
    from src.stacks import check_stack
    out = check_stack(["luteolin"])
    assert out["redundancies"] == []


def test_share_roundtrip():
    from src.stacks import share_encode, share_decode
    items = ["Luteolin", "HMB"]
    assert share_decode(share_encode(items)) == ["luteolin", "hmb"]


def test_share_invalid_decode():
    from src.stacks import share_decode
    assert share_decode("!!!not-base64!!!") == []
    assert share_decode("") == []


def test_case_insensitive_matching():
    from src.stacks import check_stack
    out = check_stack(["LUTEOLIN", "Hmb"])
    assert out["unknown"] == []
    assert sorted(e["compound"] for e in out["scored"]) == ["hmb", "luteolin"]
