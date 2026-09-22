"""RED: compound DB must load, normalize, rank."""
import os
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "compounds.csv")


def test_compounds_csv_exists():
    assert os.path.exists(DATA), "compounds.csv missing"


def test_compounds_schema():
    df = pd.read_csv(DATA)
    required = {"compound", "median_lifespan_pct", "sex", "assay",
                "dose", "strain", "source_doi", "evidence_grade"}
    assert required.issubset(set(df.columns)), f"bad cols: {list(df.columns)}"


def test_compounds_count():
    df = pd.read_csv(DATA)
    assert len(df) >= 50, f"need >=50 rows, got {len(df)}"


def test_top_hit_luteolin():
    from src.compounds import load_compounds, rank_compounds
    df = load_compounds(DATA)
    ranked = rank_compounds(df)
    assert "luteolin" in ranked["compound"].str.lower().values
    row = ranked[ranked["compound"].str.lower() == "luteolin"].iloc[0]
    assert row["median_lifespan_pct"] >= 10.0
