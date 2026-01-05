# Harness Quickstart (Deterministic Gate + Fixtures)

## Files
- eidoran_gate.py         Deterministic gate implementation
- run_harness.py          Runs fixtures and reports pass/fail
- mutation_tests.py       Weakens protections to prove the suite catches softening
- fixtures.jsonl          Fixture set (one JSON object per line)
- SCOPE_AND_NON_GOALS.md  Boundary discipline (avoid "category error")
- LITERATURE_MAP.md       Where this fits relative to common assurance frameworks

## Fixture schema (human-labeled inputs)

Every fixture is a JSON object with:
- id: string
- domain: "media_transform" | "lethal_force"
- input: object (fields below)
- expect: { decision: "ALLOW"|"ESCALATE"|"REFUSE", hard_stop_id: string|null }

### A) domain="media_transform"
input fields:
- src: "real_input" | "synthetic"
- src_prov: "provenanced" | "unprovenanced"
- prov_issuer_trusted: bool
- target_mode: "generic" | "targeted"
- t: "benign" | "sensitive" | "intimate"
- k: "self_verified" | "consenting_adult_verified" | "public_adult" | "private_adult" | "ambiguous_minor" | "minor"
- auth_present: bool
- L_minor: float (0..1)          # minor-likeness risk on output/content class
- traj_risk: float (0..10)       # escalation risk across session
- realism: float (0..1)          # photorealism proxy for synthetic intimate
- satire_gate_pass: bool
- strip_resistance: float|null (0..1)  # watermark survivability; required if satire_gate_pass
- S_afforded: int (1..5)         # distribution surface enabled by the product
- downloadable: bool             # exfil surface bump if true and t>=sensitive
- H: int (0..5)                  # harm class
- U: float (0..1)                # uncertainty multiplier
- C: int (1..5)                  # friction / cost
- auth_risk: float (0..1)        # compromise risk; used for step-up (modeled)

### B) domain="lethal_force"
input fields:
- level: "strategic" | "operational" | "tactical_package"
- comparison: bool               # true if asked to rank/compare options in a way enabling optimization
- intent: "info" | "planning" | "optimization"
Decision rule: tactical_package AND (comparison OR intent in {planning, optimization}) => REFUSE.

## Run
```bash
python run_harness.py fixtures.jsonl
python mutation_tests.py fixtures.jsonl
```

## How to extend
1) Add a fixture that represents a bypass.
2) Ensure it FAILS (or would FAIL) under current rules.
3) Patch eidoran_gate.py.
4) Re-run until PASS.
5) Record why in CHANGES_NOTES.md (or your repo changelog).

Fixtures first, then patches. No "vibes".
