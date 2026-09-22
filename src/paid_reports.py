"""Paid dossiers: gate exact scores by plan (zero-dep, no IO, no network)."""
import re


def _score_band(score: float) -> str:
    if score >= 10:
        return "top quartile"
    if score >= 5:
        return "upper quartile"
    if score > 0:
        return "lower quartile"
    return "bottom quartile"


def _normalise_circuits(circuits) -> list[str]:
    if circuits is None:
        return []
    if isinstance(circuits, str):
        parts = re.split(r"[;,]", circuits)
        return [p.strip() for p in parts if p.strip()]
    return [str(c).strip() for c in circuits if str(c).strip()]


def _disclaimer() -> str:
    return "- Model: Drosophila melanogaster; human translation UNVERIFIED"


def _sources_line() -> str:
    return "- Sources: Janelia Male CNS v1.0 CC-BY; FlyWire FAFB v783"


def _methods_note() -> str:
    return ("- Methods: healthspan score sums median lifespan gain plus functional "
            "bonus (climbing/behaviour, stress resistance) plus circuit overlap; "
            "Drosophila melanogaster model; human relevance requires validation.")


def build_dossier(compound: str, score: float, circuits, grade: str,
                  plan: str, source_dois=None) -> str:
    """Build markdown dossier. Free returns teaser with score band only."""
    if plan not in ("free", "researcher", "brand"):
        raise ValueError(f"unknown plan: {plan}")
    name = str(compound)
    band = _score_band(float(score))
    disclaimer = _disclaimer()

    if plan == "free":
        return (f"# FlyBrain Longevity Teaser: {name}\n\n"
                f"- Score band: {band} (exact score reserved for paid tiers)\n"
                f"- {disclaimer}\n"
                f"- Upgrade to Researcher (£19/month) or Brand (£299/month) "
                f"for full dossier with exact scores, circuits, and methods.\n")

    circuit_list = _normalise_circuits(circuits)
    circuits_str = "; ".join(circuit_list) if circuit_list else "none mapped"
    lines = [
        f"# FlyBrain Longevity Dossier: {name}",
        "",
        f"- Healthspan score: {float(score)}",
        f"- Score band: {band}",
        f"- Circuits: {circuits_str}",
        f"- Evidence grade: {grade} (A=fetched paper, C=needs validation)",
        _methods_note(),
        _sources_line(),
        disclaimer,
    ]
    if plan == "brand":
        lines.append("")
        lines.append("## Claim-support")
        dois = list(source_dois) if source_dois else []
        if isinstance(source_dois, str):
            dois = [source_dois]
        if dois:
            lines.append("Source DOIs supporting this dossier:")
            for doi in dois:
                doi = str(doi).strip()
                lines.append(f"- https://doi.org/{doi}")
        else:
            lines.append("No source DOIs supplied for this dossier.")
    return "\n".join(lines) + "\n"


def dossier_filename(compound: str, plan: str) -> str:
    """Safe markdown filename containing compound and plan slugs."""
    base = str(compound).lower().strip()
    base = re.sub(r"[/\\\\]+", "_", base)
    base = re.sub(r"\s+", "_", base)
    base = re.sub(r"[^a-z0-9_\-]", "_", base)
    base = re.sub(r"_+", "_", base).strip("_-") or "compound"
    safe_plan = re.sub(r"[^a-z0-9_\-]", "_", str(plan).lower().strip()) or "free"
    return f"{base}_{safe_plan}.md"
