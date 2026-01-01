# Changelog

## v1.2.0 (2026-01-01)

- **Bootstrap mode (non-aborting):** hash mismatch and/or missing logger no longer forces an immediate abort; operate unbound with `PROVENANCE_GAP` and low-stakes only.
- **Ledger gating:** ledger is advisory in BOOTSTRAP, but **mandatory for high-stakes** decisions (`Φ > 0` or floor-relevant) and any irreversible/forced-choice path.
- **Proof discipline:** proof budgets are **Tier-S** (≤5 snippets, ≤50 words total per response; unlimited cycles; over-budget => provenance warning, not abort).
- README: quick-start updated; added 3 red-team prompts.
- VERIFYING: rewritten (no truncations); includes bootstrap guidance.

## v1.1.0 (2025-12-31)

- Expanded interop scaffolding (self-identification + PDSM).
- Added minimal Python ledger stub (`KERNEL_NOTES`).

## v1.0.0 (2025-12-31)

- Initial public snapshot (Shard + Kernel + Companion + checksum verification).

