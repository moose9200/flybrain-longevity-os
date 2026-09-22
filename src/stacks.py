"""Viral stack-checker engine (FlyBrain Longevity OS)."""
import base64
import binascii
import os

from src.compounds import load_compounds
from src.scoring import add_scores

_BASE = os.path.dirname(__file__)
_DATA = os.path.join(_BASE, "..", "data", "compounds.csv")


def _load_known() -> set[str]:
    """Lowercased compound names from the bundled CSV (empty set if missing)."""
    try:
        import pandas as pd

        df = pd.read_csv(_DATA)
        return {str(n).strip().lower() for n in df["compound"].tolist()}
    except (OSError, ValueError, KeyError):
        return set()


KNOWN: set[str] = _load_known()


def _scored_lookup() -> dict:
    """Lowercased name -> (canonical name, score, grade, circuit tags)."""
    try:
        scored = add_scores(load_compounds(_DATA))
    except (OSError, ValueError, KeyError):
        return {}
    lookup = {}
    for _, row in scored.iterrows():
        key = str(row["compound"]).strip().lower()
        lookup[key] = (
            str(row["compound"]),
            float(row["healthspan_score"]),
            str(row["evidence_grade"]),
            str(row.get("circuit_tags", "")).strip(),
        )
    return lookup


def check_stack(items: list[str]) -> dict:
    """Score a user-picked stack of compound names (case-insensitive)."""
    lookup = _scored_lookup()
    scored = []
    unknown = []
    for raw in items:
        key = str(raw).strip().lower()
        if not key:
            continue
        if key in lookup:
            name, score, grade, _tags = lookup[key]
            scored.append(
                {"compound": name, "healthspan_score": score, "grade": grade}
            )
        else:
            unknown.append(raw)
    scored.sort(key=lambda e: e["healthspan_score"], reverse=True)
    stack_score = sum(e["healthspan_score"] for e in scored) / len(scored) if scored else 0.0
    if not scored:
        verdict = "empty"
    elif stack_score < 5:
        verdict = "weak"
    elif stack_score < 10:
        verdict = "promising"
    else:
        verdict = "strong"
    by_tags: dict[str, list[str]] = {}
    for entry in scored:
        tags = lookup[entry["compound"].strip().lower()][3]
        by_tags.setdefault(tags, []).append(entry["compound"])
    redundancies = [sorted(group) for group in by_tags.values() if len(group) > 1]
    redundancies.sort()
    return {
        "scored": scored,
        "unknown": unknown,
        "stack_score": stack_score,
        "verdict": verdict,
        "redundancies": redundancies,
    }


def share_encode(items: list[str]) -> str:
    """Encode a stack as a URL-safe string (lowercased, comma-joined)."""
    joined = ",".join(str(n).strip().lower() for n in items if str(n).strip())
    return base64.urlsafe_b64encode(joined.encode("utf-8")).decode("ascii")


def share_decode(s: str) -> list[str]:
    """Decode a share string back to names; [] on invalid input."""
    if not isinstance(s, str) or not s.strip():
        return []
    try:
        padded = s.strip() + "=" * (-len(s.strip()) % 4)
        raw = base64.b64decode(padded, altchars=b"-_", validate=True)
        text = raw.decode("utf-8")
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return []
    return [n.strip().lower() for n in text.split(",") if n.strip()]
