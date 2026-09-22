"""RED: visit analytics — stdlib only, JSON list store."""
import json

from src.analytics import log_visit, visit_stats


def test_log_round_trip_tmp_path(tmp_path):
    store = str(tmp_path / "visits.json")
    log_visit(store, "stack-checker", "abcd1234")
    with open(store, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list) and len(data) == 1
    entry = data[0]
    assert entry["source"] == "stack-checker"
    assert entry["ref"] == "abcd1234"
    assert "ts" in entry


def test_corrupt_tolerated_on_log(tmp_path):
    store = tmp_path / "visits.json"
    store.write_text("not valid json {{{", encoding="utf-8")
    log_visit(str(store), "screener", "ref1")
    with open(store, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["source"] == "screener"


def test_corrupt_tolerated_on_stats(tmp_path):
    store = tmp_path / "visits.json"
    store.write_text("{{{ corrupt", encoding="utf-8")
    stats = visit_stats(str(store))
    assert stats == {"total": 0, "by_source": {}, "by_ref": {}}


def test_stats_grouping_by_source(tmp_path):
    store = str(tmp_path / "visits.json")
    log_visit(store, "screener", "r1")
    log_visit(store, "screener", "r2")
    log_visit(store, "stack-checker", "r1")
    stats = visit_stats(store)
    assert stats["total"] == 3
    assert stats["by_source"] == {"screener": 2, "stack-checker": 1}


def test_ref_counting(tmp_path):
    store = str(tmp_path / "visits.json")
    log_visit(store, "a", "code1")
    log_visit(store, "b", "code1")
    log_visit(store, "a", "code2")
    stats = visit_stats(store)
    assert stats["by_ref"] == {"code1": 2, "code2": 1}


def test_missing_file_stats_zero(tmp_path):
    stats = visit_stats(str(tmp_path / "nope.json"))
    assert stats["total"] == 0
    assert stats["by_source"] == {} and stats["by_ref"] == {}
