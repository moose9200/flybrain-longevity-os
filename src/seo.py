"""SEO + share-card engine: pure functions, zero deps, no IO."""
import re

SITE = "https://flybrain-longevity-os-production.up.railway.app/"
CANONICAL_BASE = SITE

GRADE_MEANINGS = {
    "A": "Strong evidence - fetched paper with lifespan data.",
    "B": "Moderate evidence - single study, needs replication.",
    "C": "Early evidence - needs validation before any claim.",
}


def compound_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return slug or "compound"


def _grade_meaning(grade: str) -> str:
    return GRADE_MEANINGS.get(str(grade).upper(), "Unknown grade - treat as early evidence.")


def compound_page(compound_row: dict) -> str:
    row = dict(compound_row)
    name = str(row.get("compound", "compound"))
    slug = compound_slug(name)
    score = row.get("healthspan_score", row.get("median_lifespan_pct", "?"))
    grade = str(row.get("evidence_grade", "?"))
    meaning = _grade_meaning(grade)
    circuits = str(row.get("circuit_tags", row.get("circuits", "")) or "").replace(";", ", ")
    dose = row.get("dose", "?")
    strain = row.get("strain", "?")
    sex = row.get("sex", "?")
    assay = row.get("assay", "")
    doi = str(row.get("source_doi", "") or "")
    lines = [
        f"# {name} longevity evidence",
        "",
        f"Healthspan score: {score}.",
        f"Evidence grade: {grade} - {meaning}",
        f"Circuits: {circuits or 'unmapped'}.",
        f"Dose: {dose} | Strain: {strain} | Sex: {sex}.",
        f"Behaviour assay: {assay}." if assay else "Behaviour assay: not reported.",
        "Model: Drosophila melanogaster; human translation UNVERIFIED.",
        "Fly data only; optimised for research behaviour, not health advice.",
        "Sources: Janelia Male CNS v1.0 (CC-BY); FlyWire FAFB v783 (CC-BY).",
    ]
    if doi:
        lines.append(f"Primary source DOI: {doi}.")
    lines.append(f"Canonical: {CANONICAL_BASE}?compound={slug}")
    return "\n".join(lines) + "\n"


def share_card(stack_score: float, verdict: str, n_compounds: int) -> str:
    return (
        f"FlyBrain stack score {stack_score} - {verdict} "
        f"across {int(n_compounds)} compounds. Check your stack: {SITE}"
    )


def sitemap_entries(compounds: list, base_url: str) -> list:
    base = str(base_url).rstrip("/")
    urls = [f"{base}/", f"{base}/stack-checker"]
    for c in compounds:
        urls.append(f"{base}/?compound={compound_slug(str(c))}")
    return urls
