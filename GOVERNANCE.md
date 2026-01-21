# GOVERNANCE.md
Version: 0.5-draft (ASCII-canonical)

Purpose
This document defines change control for the repository: how foundational constraints evolve without silent weakening, how releases are made verifiable, and how high-impact decisions are audited.

Principles
1) Additive improvement by default
Edits should clarify, compress, or test existing commitments. Weakening protections requires an explicit SOFTEN event.

2) Tests replace vows
Claims that matter must be defended by tests (fixtures and mutation tests) rather than promises or tone.

3) External legibility
Documents must be readable by a skeptical third party without private context.

Change control
Protected documents:
- FOUNDATION.md
- DECISION_PROCEDURE.md
- THREAT_MODEL.md
- GOVERNANCE.md
- SOFTEN_EVENTS.md
- FIXTURES.jsonl
- INVARIANTS.json
- INVARIANTS_BASELINE.json

Rule: no silent protected-file change
Any change to a protected document must be accompanied by a new change event in SOFTEN_EVENTS.md that:
- references each changed protected file
- includes non-empty defensive_tests_added and mutation_tests_added
- includes approvals (may be empty only if notes explains why)

Baseline pin
The release baseline is INVARIANTS_BASELINE.json. This repository pins its sha256 hash in run_tests.py.
If INVARIANTS_BASELINE.json changes without updating the pin, run_tests.py fails.

How to verify (minimal)
1) python run_tests.py
2) python mutation_tests.py
