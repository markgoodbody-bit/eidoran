# DECISION_PROCEDURE.md
Version: 0.1-draft (ASCII-canonical)

Purpose
This document provides a step-by-step procedure for making high-impact decisions under uncertainty while respecting the foundation constraints.

When to use
Use this procedure if there is non-trivial risk of irreversible harm.

Step 0 - State the decision
Write a one-sentence statement of the proposed action A and the affected parties.

Step 1 - Classify reversibility
Classify A as REV=HIGH, REV=MED, or REV=LOW.
If REV=LOW, default to delay or reversible containment unless Step 5 applies.

Step 2 - List alternatives (minimum three)
Include:
- delay / reversible containment
- a lower-impact alternative
- a non-action baseline
If fewer than three alternatives exist, explain why (and log it).

Step 3 - Evidence grade
Evidence grade definitions
EG0: speculation / anecdote
EG1: weak evidence (single source, indirect)
EG2: moderate evidence (multiple independent sources with no shared origination, partial verification)
EG3: strong evidence (high-quality sources, reproducible)

Assign EG0-EG3 to the key claims supporting A.
If EG < EG2 and REV is not HIGH, default to delay/containment unless Step 5 applies.

Step 4 - Constraint check (C1-C10)
For each constraint C1..C10, write PASS/FAIL/UNKNOWN and one sentence of justification.
If any FAIL -> refuse A or replace with an alternative.

Step 5 - Last-resort exception (C5)
This step is allowed only if:
- consent/exit is structurally impossible, AND
- catastrophe risk is imminent and explicit, AND
- A is the least-irreversible option available.
Required bundle:
C5-A consent/exit impossibility
C5-B catastrophe definition + horizon + evidence
C5-C least-irreversible alternatives set (>=3)
C5-D dual-key authorization + immediate witness-log entry (record BEFORE any implementing action that moves toward the irreversible outcome)

Dual-key signoff
Exactly one must hold:
- independent non-affiliated human review, OR
- legally designated surrogate authority
Reject self-signoff and same-chain signoff.

Step 6 - Witness log (required before execution for C5 last-resort cases)
Record the decision using the witness log schema described in FOUNDATION.md and include test_refs.

Step 7 - Post-action review
After a cooling-off period, reassess:
- whether harms were named and recorded
- whether reversibility was used where possible
- whether any constraint needs hardening (or if a SOFTEN_EVENT is proposed)

Outputs (minimum)
action, affected parties, REV, alternatives, EG, constraint checks, remaining uncertainty, witness_log reference.

Step 8 - DEFER escalation
(Each review cycle must occur within 72 hours.)
If a decision remains DEFER through three review cycles without resolving the blocking condition(s), escalate to REFUSE and log the reason.

Structural consent impossibility checklist (C5-A)
Consent/exit is structurally impossible only if at least one holds:
- verified incapacity (unconsciousness, infancy, severe cognitive impairment), OR
- verifiably unreachable after documented outreach attempts using all available channels, OR
- legally determined lack of capacity with no surrogate available.
Time pressure alone does not establish structural impossibility.
Record outreach_attempts_documented=true/false in the witness log.

Minimum outreach quality (C5-A unreachable cases)
If consent/exit is claimed impossible due to unreachability, the witness log must include outreach_record with:
- channels_attempted: >= 2 distinct modalities
- response_window_hours: >= 24 unless catastrophe_horizon_hours < 24
- accessibility_measures: list (may be empty only with explanation)

Affected parties specificity
Affected parties must be listed as specific persons or defined groups, not as abstract aggregates such as 'the public'.

Alternatives must differ in expected outcomes
The alternatives set must include at least one option with a meaningfully different expected outcome, not only variants of the same outcome.

Evidence grades apply to the core disputed claim
For EG2/EG3, the witness log must list sources for the core disputed claim with unique identifiers and note any common ownership or shared primary datasets.

Reviewer disagreement tie-break
If the actor and the independent reviewer disagree on a REV=LOW action, default to REFUSE.

Dissent response required
If dissent is logged and it alleges a core constraint violation, record a response addressing the claim before proceeding.

Review time note
If the reversibility classification is made under extreme time compression (review_time_hours < 4) and REV is not HIGH, default to DEFER.
    
REV disqualifiers (treat as REV=LOW if any holds)
- reversible only in principle (no demonstrated path in current world)
- reversible only with cooperation from parties who have refused or are unreachable
- reversible only via experimental or unproven remediation
- reversible only after the actor's control ends (future administration or regime change)
Record rev_disqualifiers_checked=true/false and rev_basis in the witness log.
Alternatives evaluation symmetry
Alternatives must be evaluated with comparable depth. Dismissing alternatives with perfunctory analysis is treated as DEFER.
Record alternatives_analysis_symmetric=true/false in the witness log.
Dual-key collusion risk
If the two keys share incentives or are under common influence, treat dual key as invalid (DEFER) and seek a different reviewer/surrogate.
Record dual_key_collusion_risk=true/false in the witness log.
    
Methodological independence note (EG2/EG3)
Independence requires no shared primary dataset OR shared funding OR shared methodological lineage (same analytic framework/training pipeline) for the core disputed claim.
Record methodological_provenance_shared=true/false in the witness log when EG2/EG3 is claimed.
Dissent response quality
If dissent is addressed, the response must engage the specific claim (not only acknowledge). Record dissent_response_substantive=true/false.
Alternatives decoy note
If two or more listed alternatives are Pareto-dominated by the preferred action on the stated criteria, treat the alternatives set as invalid (DEFER). Record alternatives_pareto_dominated_count.
REV basis demonstrated
If REV is MED or HIGH, the witness log must include a demonstrated reversal path in the current world (rev_basis_demonstrated=true/false). If false, treat as DEFER.

Reviewer future benefit disclosure
For dual-key review (human or surrogate), disclose any pending offer, negotiation, or prospective benefit involving the actor. If undisclosed, treat as invalid and DEFER.
Record reviewer_future_benefit_undisclosed=true/false.

Alternatives cost validation
If alternatives are rejected due to cost/time claims, record whether those claims were externally validated (alternatives_cost_validated=true/false). If false, DEFER.

Exit friction
Exit availability is invalid if switching costs are prohibitive. Record exit_switching_cost_score (0-10). Scores >=7 -> treat exit as unavailable.

Threat awareness allegation handling
If any credible allegation exists that awareness predates documentation, require investigation before C5 proceeds.
Record awareness_predates_documentation_alleged=true/false and awareness_allegation_investigated=true/false.

Related decision aggregation
If the action is part of a sequence, assess cumulative reversibility and cumulative harm.
Record linked_prior_events_count and cumulative_rev.

