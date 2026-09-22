"""RED: healthspan scoring must combine lifespan + function + circuit bonus."""
from src.scoring import healthspan_score


def test_score_basic():
    s = healthspan_score(lifespan_pct=11.6, climbing=True,
                         stress=False, circuit_overlap=2)
    assert s > 11.6, "circuit bonus missing"
    assert s < 100


def test_score_no_effect():
    s = healthspan_score(lifespan_pct=0.0, climbing=False,
                         stress=False, circuit_overlap=0)
    assert s == 0.0


def test_score_negative_capped():
    s = healthspan_score(lifespan_pct=-51.3, climbing=False,
                         stress=False, circuit_overlap=0)
    assert s == -51.3


def test_rank_end_to_end():
    from src.compounds import load_compounds
    from src.scoring import add_scores
    import os
    data = os.path.join(os.path.dirname(__file__), "..", "data", "compounds.csv")
    df = load_compounds(data)
    scored = add_scores(df, circuit_hits={"luteolin": 2})
    assert "healthspan_score" in scored.columns
    top = scored.sort_values("healthspan_score", ascending=False).iloc[0]
    assert top["healthspan_score"] > 0
