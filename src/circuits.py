"""Circuit mapper: Janelia Male CNS v1.0 + FlyWire female refs."""
import json


def load_circuits(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def sex_aware_circuits(circuits: list, exclude_dimorphic: bool = True) -> list:
    if not exclude_dimorphic:
        return circuits
    return [c for c in circuits if not c.get("sex_specific", False)]


def circuit_lookup(circuits: list, name: str) -> dict:
    for c in circuits:
        if c["name"] == name:
            return c
    raise KeyError(f"unknown circuit: {name}")
