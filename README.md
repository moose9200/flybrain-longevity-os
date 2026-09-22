# FlyBrain Longevity OS
Live: https://flybrain-longevity-os-production.up.railway.app/
Software-only Drosophila healthspan screener. Zero budget.
Leverages Janelia Male CNS v1.0 (CC-BY, 166k neurons) + FlyWire Female FAFB v783 (139k neurons).

## Run
pip install -r requirements.txt
pytest tests/ -v
streamlit run app.py

## Data
- `data/compounds.csv`: 50 compounds, lifespan + climbing + stress, grades A (fetched) / C (validate)
- `data/circuits.json`: 6 circuits (5 unisex + 1 dimorphic excluded by default), all `male-cns:v1.0`

## Connectome access
- Interactive: https://neuprint.janelia.org/ dataset male-cns:v1.0
- Code: `pip install neuprint-python`, token from neuPrint account, see circuit query_examples
- Bulk: gs://flyem-male-cns/v1.0/... (use API; large feathers not bundled)
- Female: https://codex.flywire.ai/

## Pricing
- Free £0: top-10 leaderboard, 1 teaser report/mo
- Researcher £19/mo: full 51-compound CSV, unlimited dossiers, circuit queries
- Brand £299/report: screening dossier + claim-support pack
- Checkout via Stripe Payment Links (env vars, nothing hardcoded). Affiliate links disclosed in-app.

## License / attribution
Male CNS CC-BY. Cite Berg et al Cell 2026 + Dorkenwald et al Nature 2024.
Human translation UNVERIFIED. No medical claims.
