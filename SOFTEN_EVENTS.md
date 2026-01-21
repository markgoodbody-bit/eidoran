# SOFTEN_EVENTS.md
Append-only log of changes to protected documents (SOFTEN, HARDEN, or NEUTRAL).

Each change event MUST include:
- change_type
- changed_files
- summary
- rationale
- approvals (list; if empty, notes must explain why)
- defensive_tests_added (non-empty list)
- mutation_tests_added (non-empty list)

Format (append new entries only)
- id: EVENT-YYYYMMDD-XXXX
  date_utc: YYYY-MM-DD
  change_type: SOFTEN | HARDEN | NEUTRAL
  changed_files: [FOUNDATION.md, DECISION_PROCEDURE.md, ...]
  summary: "What changed (one sentence)"
  rationale: "Why changed (short, specific)"
  approvals: ["IndependentReviewer:Name", "LegalSurrogate:Name"]  # or [] with notes explaining why
  defensive_tests_added: ["test_id_1"]
  mutation_tests_added: ["mutation_id_1"]
  dissent: "Optional: dissent summary or 'none'"
  notes: "Optional (required if approvals is empty)"

Event-level hash (optional but recommended)
- prev_event_hash_sha256: "<sha256 of prior event block>" (or "GENESIS")
- event_hash_sha256: "<sha256 of this event block excluding event_hash_sha256>"
