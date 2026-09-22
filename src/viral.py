"""Viral-loop engine: referrals, shares, leaderboard, weekly challenge."""
import hashlib
import json
import os
import time


def referral_code(handle: str) -> str:
    norm = handle.strip().lower()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:8]


def referral_link(code: str, base_url: str = "https://flybrain-longevity-os-production.up.railway.app/") -> str:
    return f"{base_url}?ref={code}"


def _load_entries(store_path) -> list:
    try:
        with open(store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def record_share(store_path, code, stack_score) -> None:
    parent = os.path.dirname(os.path.abspath(str(store_path)))
    if parent:
        os.makedirs(parent, exist_ok=True)
    entries = _load_entries(str(store_path))
    entries.append({"code": code, "score": float(stack_score), "ts": time.time()})
    with open(str(store_path), "w", encoding="utf-8") as f:
        json.dump(entries, f)


def leaderboard(store_path, top_n: int = 10) -> list:
    entries = _load_entries(str(store_path))
    best: dict = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        code = e.get("code")
        score = e.get("score")
        if code is None or score is None:
            continue
        try:
            score = float(score)
        except (TypeError, ValueError):
            continue
        if code not in best or score > best[code]:
            best[code] = score
    ranked = [{"code": c, "score": s} for c, s in best.items()]
    ranked.sort(key=lambda d: d["score"], reverse=True)
    return ranked[:top_n]


def challenge_text(week_label: str) -> str:
    return (
        f"{week_label} challenge: Beat last week's top stack. "
        "Rules: (1) Log one stack daily. (2) Share your referral link. "
        "(3) Top score wins. Optimise your stack — start now!"
    )
