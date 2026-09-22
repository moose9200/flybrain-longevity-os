"""RED: growth brief generator (stdlib only, no network)."""
from pathlib import Path

import pytest

from src.content_gen import brief_for, generate_all

DATA_CSV = Path(__file__).resolve().parent.parent / "data" / "compounds.csv"


def _row(**kw):
    base = {
        "compound": "Luteolin",
        "median_lifespan_pct": "11.6",
        "sex": "female",
        "assay": "lifespan+climbing+stress",
        "dose": "50uM",
        "strain": "Oregon-R",
        "source_doi": "10.3389/fnut.2026.1909085",
        "evidence_grade": "A",
        "climbing_improved": "True",
        "stress_resistance": "False",
        "circuit_tags": "dopamine_reward;insulin_mtor;sleep_arousal",
    }
    base.update(kw)
    return base


def test_brief_contains_score():
    brief = brief_for(_row())
    assert "11.6" in brief


def test_brief_contains_disclaimer_unverified():
    brief = brief_for(_row())
    assert "UNVERIFIED" in brief
    assert "Drosophila" in brief


def test_brief_contains_doi_link():
    brief = brief_for(_row())
    assert "10.3389/fnut.2026.1909085" in brief
    assert "https://doi.org/10.3389/fnut.2026.1909085" in brief


def test_brief_contains_cta_with_slug():
    brief = brief_for(_row(compound="HMB Male"))
    assert "?compound=hmb-male" in brief


def test_brief_h1_and_circuits_dose_strain_sex():
    brief = brief_for(_row())
    assert brief.startswith("# ")
    assert "Luteolin" in brief.splitlines()[0]
    assert "dopamine_reward" in brief
    assert "50uM" in brief
    assert "Oregon-R" in brief
    assert "female" in brief


def test_slug_file_naming_safe():
    from src.seo import compound_slug

    slug = compound_slug("HMB-Male (10mg/mL) @ yw")
    assert slug == "hmb-male-10mg-ml-yw" or (" " not in slug and "/" not in slug)
    row = _row(compound="HMB-Male (10mg/mL)")
    brief = brief_for(row)
    assert f"?compound={compound_slug(row['compound'])}" in brief


def test_generate_all_writes_51_files_to_tmp_path(tmp_path):
    count = generate_all(str(DATA_CSV), str(tmp_path))
    files = list(Path(tmp_path).glob("*.md"))
    assert count == 51
    assert len(files) == 51


def test_generate_all_idempotent_rerun(tmp_path):
    first = generate_all(str(DATA_CSV), str(tmp_path))
    second = generate_all(str(DATA_CSV), str(tmp_path))
    assert first == second == 51
    assert len(list(Path(tmp_path).glob("*.md"))) == 51


def test_grade_c_flagged_needs_validation():
    brief = brief_for(_row(compound="resveratrol", evidence_grade="C"))
    assert "C" in brief
    assert "needs validation" in brief.lower()
