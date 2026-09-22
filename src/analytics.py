"""Visit analytics: stdlib only, JSON list store."""
import json
import os
import time


def _load_entries(store_path) -> list:
    try:
        with open(store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def log_visit(store_path, source, ref) -> None:
    """Append {"ts", "source", "ref"} to JSON list; tolerate corrupt file."""
    parent = os.path.dirname(os.path.abspath(str(store_path)))
    if parent:
        os.makedirs(parent, exist_ok=True)
    entries = _load_entries(str(store_path))
    entries.append(
        {
            "ts": time.time(),
            "source": str(source or ""),
            "ref": str(ref or ""),
        }
    )
    with open(str(store_path), "w", encoding="utf-8") as f:
        json.dump(entries, f)


def visit_stats(store_path) -> dict:
    """Return {"total", "by_source", "by_ref"}; tolerate missing/corrupt file."""
    entries = _load_entries(str(store_path))
    by_source: dict = {}
    by_ref: dict = {}
    total = 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        total += 1
        s = str(e.get("source", "") or "")
        r = str(e.get("ref", "") or "")
        by_source[s] = by_source.get(s, 0) + 1
        by_ref[r] = by_ref.get(r, 0) + 1
    return {"total": total, "by_source": by_source, "by_ref": by_ref}
