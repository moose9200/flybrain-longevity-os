"""FlyBrain Longevity OS — Streamlit app (zero-cost deploy)."""
import os
import streamlit as st
import pandas as pd

from src.compounds import load_compounds, rank_compounds
from src.circuits import load_circuits, sex_aware_circuits
from src.scoring import add_scores
from src.reports import build_report_row

BASE = os.path.dirname(__file__)
COMPOUNDS = os.path.join(BASE, "data", "compounds.csv")
CIRCUITS = os.path.join(BASE, "data", "circuits.json")

st.set_page_config(page_title="FlyBrain Longevity OS", layout="wide")
st.title("FlyBrain Longevity OS — Drosophila Healthspan Screener")
st.caption("Male CNS v1.0 (Janelia, CC-BY) + Female FAFB v783 (FlyWire). Software-only v0. No wet-lab claims.")

df = add_scores(load_compounds(COMPOUNDS))
circuits = sex_aware_circuits(load_circuits(CIRCUITS))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Compound leaderboard")
    grade = st.selectbox("Evidence grade", ["All", "A", "B", "C"])
    view = df if grade == "All" else df[df["evidence_grade"] == grade]
    view = view.sort_values("healthspan_score", ascending=False)
    st.dataframe(view[["compound", "median_lifespan_pct", "sex",
                       "healthspan_score", "evidence_grade"]].head(50))
with col2:
    st.subheader("Brain-circuit mapper")
    for c in circuits:
        with st.expander(c["name"]):
            st.write(c["description"])
            st.code(c["query_example"], language="python")
            st.caption(f"Dataset: {c['neuprint_dataset']} | {c['sex_dimorphism_flag']}")

st.subheader("Consumer report")
choice = st.selectbox("Compound", sorted(df["compound"].tolist()))
row = df[df["compound"] == choice].iloc[0]
st.markdown(build_report_row(row["compound"], row["healthspan_score"],
                             row["circuit_tags"], row["evidence_grade"]))
st.download_button("Download ranked CSV",
                   df.to_csv(index=False), "flybrain_ranked.csv")
