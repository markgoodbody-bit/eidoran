from __future__ import annotations
import json
import sys
from typing import Any, Dict, List

from eidoran_gate import gate, GateConfig

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            out.append(json.loads(line))
    return out

def run_suite(fixtures: List[Dict[str, Any]], cfg: GateConfig) -> int:
    mismatches = 0
    for fx in fixtures:
        expect = fx["expect"]
        exp_dec = expect["decision"]
        exp_hs = expect["hard_stop_id"]
        dec, trace = gate({"domain": fx["domain"], "input": fx["input"]}, cfg)
        if dec != exp_dec or trace.get("hard_stop_id") != exp_hs:
            mismatches += 1
    return mismatches

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python mutation_tests.py fixtures.jsonl")
        return 2

    fixtures = load_jsonl(sys.argv[1])
    base = GateConfig()
    base_mismatches = run_suite(fixtures, base)
    if base_mismatches != 0:
        print(f"Base suite already failing ({base_mismatches} mismatches). Fix base before mutation tests.")
        return 1

    mutations = [
        ("raise_tau_minor_to_0_95", lambda c: GateConfig(**{**c.__dict__, "tau_minor": 0.95})),
        ("raise_tau_traj_to_9", lambda c: GateConfig(**{**c.__dict__, "tau_traj": 9.0})),
        ("raise_allow_threshold_to_3", lambda c: GateConfig(**{**c.__dict__, "allow_lt": 3.0})),
        ("raise_escalate_threshold_to_8", lambda c: GateConfig(**{**c.__dict__, "escalate_lt": 8.0})),
        ("lower_tau_strip_to_0_30", lambda c: GateConfig(**{**c.__dict__, "tau_strip": 0.30})),
    ]

    caught = 0
    for name, mut_fn in mutations:
        cfg = mut_fn(base)
        mismatches = run_suite(fixtures, cfg)
        if mismatches > 0:
            caught += 1
            print(f"PASS mutation {name}: suite detected change ({mismatches} mismatches)")
        else:
            print(f"FAIL mutation {name}: suite did NOT detect change (0 mismatches) -> add fixtures")

    print(f"\nMutation detection: {caught}/{len(mutations)} mutations detected")
    return 0 if caught == len(mutations) else 1

if __name__ == "__main__":
    raise SystemExit(main())
