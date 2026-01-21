# THREAT_MODEL.md
Version: 0.1-draft (ASCII-canonical)

Purpose
This document lists common failure modes for ethical decision systems and the corresponding defenses used in this repository.

Threats (non-exhaustive)
T1 Substitution drift
Same words, weaker meaning. Example: replacing "delay/containment" with "proceed unless unsafe".
Defense: baseline hash pin + required change event + fixture tests + mutation tests.

T2 Quiet softening
Lowering thresholds, broadening exceptions, narrowing protected scope without a loud change record.
Defense: required change event completeness + invariants checks + baseline hash pin + fixture tests.

T3 Owner capture
Optimization for the funder/owner rather than the protection floors.
Defense: dual-key signoff rule; refusal boundary; append-only audit trail where feasible.

T4 Ledger laundering
Renaming harm, deleting or hiding records, or moving irreversible harm off-ledger.
Defense: append-only witness log; explicit "harm laundering" prohibition; hash discipline for log entries.

T5 Emergency-pretext bypass
Invoking vague emergencies to override constraints.
Defense: catastrophe definition + horizon; evidence grade requirement; last-resort bundle (C5-A..D).

T6 Ritual drift
Repeating phrases without tests; compliance theater.
Defense: tests replace vows; fixture suite; mutation demonstrations; explicit PASS/FAIL checks.

T7 Evidence inflation
Sounding confident without support; compressing uncertainty into rhetoric.
Defense: EG0-EG3 evidence grades; force explicit uncertainty lists.

T8 Misuse for violence optimization
Using the framework to rank or optimize lethal targeting workflows.
Defense: explicit refusal boundary (C6) and safety boundary in GOVERNANCE.md.


T9 Mandatory-to-advisory substitution
Changing 'default to' into 'recommended default' or adding undefined exception terms (e.g., 'harm progression', 'operational continuity') to bypass floors.
Defense: phrase checks in tests + fixtures that refuse undefined exceptions.


T10 Evidence grade inflation
Claiming EG2/EG3 without independent sources or verification.
Defense: fixture fields for independent-source count; require EG2 independence definition.


T11 Shell-organization dual-key capture
Using nominally independent reviewers with hidden financial dependence.
Defense: fixture fields for reviewer affiliation; treat affiliated review as invalid.

T12 Fixture coverage gap
Each threat must map to at least one fixture. Unmapped threats are treated as a COVERAGE_GAP until resolved.
Defense: tests check that each T1..T11 has a coverage line.

Coverage map (threat -> fixtures)
T1: FX-021
T2: FX-014
T3: FX-018, FX-025
T4: FX-027
T5: FX-004, FX-023
T6: FX-012
T7: FX-024
T8: FX-005
T9: FX-019, FX-020, FX-021
T10: FX-024
T11: FX-025

T13 Alternatives gaming
Satisfying the >=3 alternatives requirement with implausible or equivalent alternatives.
Defense: fixtures require at least one meaningfully different expected outcome.

T14 Undefined reviewer exception injection
Adding undefined exception terms such as 'qualified reviewers' or 'disproportionate benefits' that preserve pinned phrases but create a new bypass.
Defense: phrase pins + fixtures for disproportionality_claimed and new_exception_pathway.
Coverage map additions
T13: FX-042
T14: FX-037

T15 Legal surrogate capture
Using a legally designated surrogate who is effectively controlled by the actor (appointment, subordination, financial dependence).
Defense: fixtures with surrogate_affiliated; treat affiliated surrogate as invalid.

T16 Decision point clock games
Delaying the formal decision point while performing preparatory actions, then claiming a short catastrophe horizon.
Defense: decision point anchored to first documented awareness; fixtures for decision_point_backdated.
    
T17 REV laundering
Misclassifying harms as REV=MED/HIGH using theoretical, future, or non-cooperative reversal paths.
Defense: fixtures for rev_disqualifier_present; treat as REV=LOW.

T18 Alternatives asymmetry
Evaluating preferred action in depth while dismissing alternatives perfunctorily.
Defense: fixtures for alternatives_analysis_symmetric=false -> DEFER.

T19 Dual-key collusion
Two keys satisfy formal independence but share incentives or common influence.
Defense: fixtures for dual_key_collusion_risk=true -> DEFER.
T20 Methodological provenance laundering
Claiming EG2/EG3 using sources that share funding or methodological lineage despite distinct citations.
Defense: fixtures for methodological_provenance_shared=true -> DEFER.
T21 Dissent response theater
Responding to dissent with acknowledgment-only text while proceeding.
Defense: fixtures for dissent_response_substantive=false -> DEFER/REFUSE depending on floor claim.

T22 Reviewer selection capture
Systematic assignment of aligned reviewers while preserving formal independence.
Defense: fixtures for reviewer_future_benefit_undisclosed or reviewer_selection_bias.

T23 Alternatives cost theater
Rejecting alternatives using unvalidated cost/time claims.
Defense: fixtures for alternatives_cost_validated=false -> DEFER.

T24 Exit-right formalism
Providing nominal exit with prohibitive switching costs.
Defense: fixtures for exit_switching_cost_score>=7 -> treat exit unavailable.

