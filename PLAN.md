# FlyBrain Longevity OS - PLAN
## Acceptance (each line testable; tick only with evidence in log)
- [ ] pytest tests/ passes 12/12
- [ ] app imports without error (streamlit not required for tests)
- [ ] data/compounds.csv has >=50 rows with schema
- [ ] data/circuits.json has >=5 circuits, all male-cns:v1.0
- [ ] GitHub repo public with all files pushed
## Facts (Verified - source: file/command/URL fetched)
- Workspace was empty: ls /Users/hemant/Fruite-fly -> 0 entries
- Female FAFB v783 139255 neurons 50M synapses: fetched https://codex.flywire.ai/
- Male MCNS v1.0 166700 neurons 125M synapses CC-BY: fetched https://www.janelia.org/project-team/flyem/male-cns-connectome
- Download API neuprint-python + feathers: fetched https://janelia-flyem.github.io/male-cns/download/
- Google blog male map Sep 2026: fetched https://research.google/blog/a-connectomics-milestone-mapping-the-complete-male-fruit-fly-brain/
- Scope: software only, researchers+consumers, leaderboard+mapper (user answers)
## Assumptions (to validate - how, when)
- Grade C compound values need re-validation vs primary papers before any brand claim (validate via miner subagent reading DOIs)
- neuPrint token needed for live queries; app works offline on bundled feathers (validate via NEUPRINT_TOKEN in .env)
## Unknowns (investigation tasks, owner = you)
- Codex rate limits for bulk fetch (probe after push)
- Sex/strain translation to human (mark UNVERIFIED in reports)
## Decisions (what + why + what was rejected)
- B chosen: Streamlit + bundled small feathers + API for rest (zero cost, differentiator). Rejected A wiki (no moat), C API platform (overkill/cost).
- Small feathers in repo (13MB+42MB refs via query examples, not binaries) to keep repo light; large 1-12GB files via API only.
## Evidence log (command -> exit code / number / screenshot path)
- (to fill during test phase)
## Open risks
- No wet-lab validation; all scores computational
- CC-BY attribution required in app + reports (done)
