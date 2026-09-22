"""Consumer/researcher reports: markdown + CSV export (zero-dep)."""
import pandas as pd


def build_report_row(compound: str, score: float, circuits: str, grade: str) -> str:
    return (f"# FlyBrain Longevity Report: {compound}\n\n"
            f"- Healthspan score: {score}\n"
            f"- Circuits: {circuits}\n"
            f"- Evidence grade: {grade} (A=fetched paper, C=needs validation)\n"
            f"- Model: Drosophila melanogaster; human translation UNVERIFIED\n"
            f"- Sources: Janelia Male CNS v1.0 CC-BY; FlyWire FAFB v783\n")


def export_csv(df: pd.DataFrame, path: str) -> str:
    df.to_csv(path, index=False)
    return path
