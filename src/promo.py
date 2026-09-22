"""Promo codes + referral rewards (stdlib only, no network)."""
import hashlib
import json
import os

REWARDS = {
    "leaderboard_top3": "researcher 1 month",
    "first_share": "profile badge",
    "refer_5": "researcher 1 month",
}

CAMPAIGNS = ["launch", "refer_5", "top3"]

_CAMPAIGN_REWARD = {
    "launch": REWARDS["first_share"],
    "refer_5": REWARDS["refer_5"],
    "top3": REWARDS["leaderboard_top3"],
}


def make_code(handle: str, campaign: str) -> str:
    norm_handle = str(handle).strip().lower()
    norm_campaign = str(campaign).strip().lower()
    raw = f"{norm_handle}:{norm_campaign}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:10]


def _load_redemptions(store_path) -> list:
    try:
        with open(str(store_path), "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def redeem(store_path_or_none, code: str, handle: str) -> dict:
    code = str(code)
    norm_handle = str(handle).strip().lower()
    matched = None
    for campaign in CAMPAIGNS:
        if code == make_code(norm_handle, campaign):
            matched = campaign
            break
    if matched is None:
        return {"ok": False, "reward": ""}
    reward = _CAMPAIGN_REWARD[matched]
    if store_path_or_none is None:
        return {"ok": True, "reward": reward}
    store_path = str(store_path_or_none)
    entries = _load_redemptions(store_path)
    for e in entries:
        if not isinstance(e, dict):
            continue
        if e.get("code") == code and str(e.get("handle", "")).strip().lower() == norm_handle:
            return {"ok": False, "reward": "", "reason": "duplicate"}
    parent = os.path.dirname(os.path.abspath(store_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    entries.append({"code": code, "handle": norm_handle, "campaign": matched, "reward": reward})
    with open(store_path, "w", encoding="utf-8") as f:
        json.dump(entries, f)
    return {"ok": True, "reward": reward}
