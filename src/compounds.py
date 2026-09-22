"""Compound DB: load, rank, filter."""
import pandas as pd


def load_compounds(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["climbing_improved"] = df["climbing_improved"].astype(str).str.lower().isin(["true", "1"])
    df["stress_resistance"] = df["stress_resistance"].astype(str).str.lower().isin(["true", "1"])
    return df


def rank_compounds(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["sort_key"] = out["median_lifespan_pct"].fillna(0)
    return out.sort_values("sort_key", ascending=False).drop(columns=["sort_key"])
