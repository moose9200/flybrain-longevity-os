"""FlyBrain Longevity OS — Streamlit app (zero-cost deploy)."""
import os
import streamlit as st
import pandas as pd

from src.compounds import load_compounds, rank_compounds
from src.circuits import load_circuits, sex_aware_circuits
from src.scoring import add_scores
from src.reports import build_report_row
from src.billing import PLANS, entitlements, checkout_url, has_access
from src.paid_reports import build_dossier, dossier_filename
from src.affiliates import disclosure_banner

BASE = os.path.dirname(__file__)
COMPOUNDS = os.path.join(BASE, "data", "compounds.csv")
CIRCUITS = os.path.join(BASE, "data", "circuits.json")

st.set_page_config(page_title="FlyBrain Longevity OS", layout="wide")
st.title("FlyBrain Longevity OS — Drosophila Healthspan Screener")
st.caption("Male CNS v1.0 (Janelia, CC-BY) + Female FAFB v783 (FlyWire). Software-only v0. No wet-lab claims.")

df = add_scores(load_compounds(COMPOUNDS))
circuits = sex_aware_circuits(load_circuits(CIRCUITS))

st.sidebar.header("Plan")
plan = st.sidebar.selectbox("Your tier", ["free", "researcher", "brand"],
                            format_func=lambda p: f"{PLANS[p]['name']} — £{PLANS[p]['price_gbp']}/{PLANS[p]['interval']}")
st.sidebar.caption(PLANS[plan]["description"])
link = checkout_url(plan)
if link and plan != "free":
    st.sidebar.link_button(f"Upgrade to {PLANS[plan]['name']}", link)
elif plan != "free":
    st.sidebar.caption("Checkout link unset — set STRIPE_LINK env var.")
st.sidebar.divider()
st.sidebar.header("Pricing")
for key, p in PLANS.items():
    st.sidebar.write(f"**{p['name']}** — £{p['price_gbp']}/{p['interval']}")
st.caption(disclosure_banner())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Compound leaderboard")
    grade = st.selectbox("Evidence grade", ["All", "A", "B", "C"])
    view = df if grade == "All" else df[df["evidence_grade"] == grade]
    view = view.sort_values("healthspan_score", ascending=False)
    if not has_access(plan, "full_csv"):
        view = view.head(10)
        st.caption("Free tier shows top 10. Researcher unlocks all 51.")
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
                   df.to_csv(index=False), "flybrain_ranked.csv",
                   disabled=not has_access(plan, "full_csv"))
if not has_access(plan, "full_csv"):
    st.caption("CSV download needs Researcher tier.")

st.subheader("Screening dossier (paid tiers)")
dchoice = st.selectbox("Dossier compound", sorted(df["compound"].tolist()),
                       key="dossier_pick")
drow = df[df["compound"] == dchoice].iloc[0]
dois = [drow["source_doi"]] if drow["source_doi"] else []
dossier = build_dossier(drow["compound"], float(drow["healthspan_score"]),
                        drow["circuit_tags"], drow["evidence_grade"],
                        plan if plan in ("researcher", "brand") else "free",
                        source_dois=dois)
st.markdown(dossier)
if has_access(plan, "screening_dossier") or has_access(plan, "unlimited_reports"):
    st.download_button("Download dossier",
                       dossier, dossier_filename(drow["compound"], plan))
