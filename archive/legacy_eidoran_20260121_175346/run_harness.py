from __future__ import annotations
import json
import sys
from typing import Any, Dict, List

from eidoran_gate import gate, GateConfig

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    fixtures: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                fixtures.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"JSON parse error on line {i}: {e}") from e
    return fixtures

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python run_harness.py fixtures.jsonl")
        return 2

    path = sys.argv[1]
    fixtures = load_jsonl(path)
    cfg = GateConfig()

    passed = 0
    failed = 0

    for fx in fixtures:
        fx_id = fx.get("id", "<no-id>")
        expect = fx.get("expect", {})
        exp_dec = expect.get("decision")
        exp_hs = expect.get("hard_stop_id")

        try:
            dec, trace = gate({"domain": fx["domain"], "input": fx["input"]}, cfg)
        except Exception as e:
            failed += 1
            print(f"FAIL {fx_id}: exception {type(e).__name__}: {e}")
            continue

        got_hs = trace.get("hard_stop_id")
        ok = (dec == exp_dec) and (got_hs == exp_hs)

        if ok:
            passed += 1
            print(f"PASS {fx_id}: {dec} (hs={got_hs})")
        else:
            failed += 1
            print(f"FAIL {fx_id}: expected {exp_dec} (hs={exp_hs}) but got {dec} (hs={got_hs})")
            dbg = {k: trace[k] for k in trace if k in ("hard_stop_id", "why", "M", "S_effective", "stepup_forced")}
            print(f"      trace: {dbg}")

    print(f"\nSummary: PASS={passed} FAIL={failed} TOTAL={passed+failed}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
