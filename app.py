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
from src.stacks import check_stack, share_encode, share_decode
from src.seo import compound_slug, compound_page, share_card
from src.viral import referral_code, referral_link, record_share, leaderboard, challenge_text
from src.cards import score_card_svg, score_card_png
from src.analytics import log_visit, visit_stats
from src.promo import make_code, redeem, REWARDS
import datetime

BASE = os.path.dirname(__file__)
COMPOUNDS = os.path.join(BASE, "data", "compounds.csv")
CIRCUITS = os.path.join(BASE, "data", "circuits.json")
STORE = os.path.join(BASE, "data", "shares.json")
SITE = "https://flybrain-longevity-os-production.up.railway.app/"

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

params = st.query_params
_visit_src = "stack" if params.get("stack") else ("compound" if params.get("compound") else ("ref" if params.get("ref") else "direct"))
try:
    log_visit(os.path.join(BASE, "data", "visits.json"), _visit_src, params.get("ref", ""))
except Exception:
    pass
tab1, tab2, tab3 = st.tabs(["Screener", "Stack Checker", "Challenge"])
with tab1:
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
    deep = params.get("compound", "")
    names = sorted(df["compound"].tolist())
    default_choice = deep if deep in names else names[0]
    choice = st.selectbox("Compound", names,
                          index=names.index(default_choice))
    row = df[df["compound"] == choice].iloc[0]
    st.markdown(compound_page(row.to_dict()))
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

with tab2:
    st.subheader("Stack Checker — score your supplement stack")
    prefill = share_decode(params.get("stack", "")) if params.get("stack") else []
    raw = st.text_area("One compound per line",
                       value="\n".join(prefill) if prefill else "luteolin\nresveratrol")
    items = [l.strip() for l in raw.splitlines() if l.strip()]
    if st.button("Score my stack"):
        res = check_stack(items)
        st.metric("Stack score", res["stack_score"])
        st.write(f"Verdict: **{res['verdict']}**")
        if res["scored"]:
            st.dataframe(pd.DataFrame(res["scored"]))
        if res["unknown"]:
            st.warning(f"Not in DB (ignored): {', '.join(res['unknown'])}")
        if res["redundancies"]:
            st.info(f"Overlap groups: {res['redundancies']}")
        code = share_encode([s["compound"] for s in res["scored"]]) if res["scored"] else ""
        if code:
            st.code(f"{SITE}?stack={code}", language="text")
            st.caption(share_card(res["stack_score"], res["verdict"],
                                  len(res["scored"])))
            title = f"My stack ({len(res['scored'])} compounds)"
            try:
                st.download_button("Download share card (PNG)",
                                   score_card_png(title, res["stack_score"],
                                                  res["verdict"]),
                                   file_name="flybrain_stack.png",
                                   mime="image/png")
            except Exception:
                st.code(score_card_svg(title, res["stack_score"],
                                       res["verdict"]), language="xml")
            handle = st.text_input("Handle for leaderboard", key="lb_handle")
            if st.button("Post to leaderboard") and handle.strip():
                record_share(STORE, referral_code(handle.strip()),
                             res["stack_score"])
                st.success(f"Posted! Your link: {referral_link(referral_code(handle.strip()))}")

with tab3:
    st.subheader("Weekly Challenge")
    week = datetime.date.today().strftime("%Y-W%V")
    st.write(challenge_text(week))
    st.subheader("Leaderboard")
    board = leaderboard(STORE)
    if board:
        st.dataframe(pd.DataFrame(board))
    else:
        st.caption("Empty — first entry takes the crown.")
    st.subheader("Rewards")
    st.caption(f"Top 3: {REWARDS['leaderboard_top3']}. First share: {REWARDS['first_share']}. 5 referrals: {REWARDS['refer_5']}.")
    rhandle = st.text_input("Handle for promo code", key="promo_handle")
    if st.button("Get my launch code") and rhandle.strip():
        st.code(make_code(rhandle.strip(), "launch"), language="text")
    pcode = st.text_input("Redeem code", key="promo_redeem")
    if st.button("Redeem") and pcode.strip() and rhandle.strip():
        out = redeem(os.path.join(BASE, "data", "redemptions.json"),
                     pcode.strip(), rhandle.strip())
        if out["ok"]:
            st.success(f"Reward: {out['reward']}")
        else:
            st.error("Invalid or already redeemed.")
    try:
        stats = visit_stats(os.path.join(BASE, "data", "visits.json"))
        st.caption(f"{stats['total']} visits tracked. Sources: {stats['by_source']}")
    except Exception:
        pass
