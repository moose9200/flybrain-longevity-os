"""RED: circuit mapper must expose 5 healthspan circuits with Janelia sources."""
import json
import os

CIRCUITS = os.path.join(os.path.dirname(__file__), "..", "data", "circuits.json")


def test_circuits_file_exists():
    assert os.path.exists(CIRCUITS)


def test_five_circuits():
    from src.circuits import load_circuits
    circuits = load_circuits(CIRCUITS)
    assert len(circuits) >= 5
    names = {c["name"] for c in circuits}
    assert {"dopamine_reward", "insulin_mtor", "sleep_arousal",
            "motor_escape", "gustatory_feeding"}.issubset(names)


def test_circuit_has_connectome_refs():
    from src.circuits import load_circuits
    circuits = load_circuits(CIRCUITS)
    for c in circuits:
        assert "neuprint_dataset" in c, f"{c['name']} missing dataset"
        assert "male-cns:v1.0" in c["neuprint_dataset"]
        assert "query_example" in c
        assert "sex_dimorphism_flag" in c


def test_dimorphism_filter():
    from src.circuits import load_circuits, sex_aware_circuits
    circuits = load_circuits(CIRCUITS)
    safe = sex_aware_circuits(circuits, exclude_dimorphic=True)
    assert all(not c.get("sex_specific", False) for c in safe)
    assert len(safe) >= 3
