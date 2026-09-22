"""Growth briefs: one markdown brief per compound (stdlib only, no network)."""
import csv
from pathlib import Path

from src.seo import CANONICAL_BASE, GRADE_MEANINGS, compound_slug


def _grade_line(grade: str) -> str:
    meaning = GRADE_MEANINGS.get(str(grade).upper(), "Unknown grade - treat as early evidence.")
    return f"Evidence grade: {grade} - {meaning}"


def brief_for(row: dict) -> str:
    """Build markdown brief for one compound row."""
    data = dict(row)
    name = str(data.get("compound", "compound"))
    slug = compound_slug(name)
    score = data.get("healthspan_score", data.get("median_lifespan_pct", "?"))
    grade = str(data.get("evidence_grade", "?"))
    circuits = str(data.get("circuit_tags", data.get("circuits", "") or "")).replace(";", ", ")
    dose = data.get("dose", "?")
    strain = data.get("strain", "?")
    sex = data.get("sex", "?")
    assay = str(data.get("assay", "") or "")
    doi = str(data.get("source_doi", "") or "").strip()
    climbing = str(data.get("climbing_improved", "") or "")
    stress = str(data.get("stress_resistance", "") or "")
    lines = [
        f"# {name} healthspan brief",
        "",
        f"Healthspan signal: {score}% median lifespan change in flies.",
        _grade_line(grade),
        f"Dose: {dose} | Strain: {strain} | Sex: {sex}.",
        f"Behaviour assay: {assay}." if assay else "Behaviour assay: not reported.",
        f"Circuits: {circuits or 'unmapped'}.",
        f"Climbing improved: {climbing or 'not reported'} | Stress resistance: {stress or 'not reported'}.",
        "Model: Drosophila melanogaster; human translation UNVERIFIED.",
        "Fly data only, optimised for research prioritisation; no medical claims.",
        "Sources: Janelia Male CNS v1.0 (CC-BY); FlyWire FAFB v783 (CC-BY).",
    ]
    if doi:
        lines.append(f"Primary source: [{doi}](https://doi.org/{doi}).")
    lines.append(f"Check your stack: {CANONICAL_BASE}?compound={slug}")
    lines.append("")
    lines.append("Disclaimer: human translation UNVERIFIED. Drosophila results do not predict human efficacy.")
    return "\n".join(lines) + "\n"


def generate_all(csv_path: str, out_dir: str) -> int:
    """Write one <slug>.md per compound row. Return file count."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            slug = compound_slug(str(row.get("compound", "compound")))
            (out / f"{slug}.md").write_text(brief_for(row), encoding="utf-8")
            count += 1
    return count
