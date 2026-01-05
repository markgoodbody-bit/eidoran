# Change notes (package)

This zip is a minimal "earn the spec" bundle:
- Deterministic gate code (no LLM)
- Fixture suite (pass/fail)
- Mutation tests (detect quiet softening)

What it does not include:
- Upstream classification (labeling) code
- Dataset-backed calibration
- CI wiring (add it in your repo)

- Added `claims_reliability` gate + `EVIDENCE_GRADE.md` for deterministic assertion-strength gating on high-stakes claims.
