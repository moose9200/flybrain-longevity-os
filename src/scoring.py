"""Healthspan scoring: lifespan + functional bonus + circuit overlap."""
import pandas as pd


def healthspan_score(lifespan_pct: float, climbing: bool = False,
                     stress: bool = False, circuit_overlap: int = 0) -> float:
    if lifespan_pct == 0 and not climbing and not stress and circuit_overlap == 0:
        return 0.0
    score = float(lifespan_pct)
    if climbing:
        score += 2.0
    if stress:
        score += 1.5
    score += 1.0 * int(circuit_overlap)
    return round(score, 2)


def add_scores(df: pd.DataFrame, circuit_hits: dict | None = None) -> pd.DataFrame:
    circuit_hits = circuit_hits or {}
    out = df.copy()
    scores = []
    for _, r in out.iterrows():
        key = str(r["compound"]).lower()
        overlap = circuit_hits.get(key, len(str(r.get("circuit_tags", "")).split(";")))
        scores.append(healthspan_score(
            float(r["median_lifespan_pct"]),
            bool(r["climbing_improved"]),
            bool(r["stress_resistance"]),
            int(overlap),
        ))
    out["healthspan_score"] = scores
    return out
