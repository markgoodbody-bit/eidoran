# FOUNDATION.md
Version: 0.3-draft (ASCII-canonical)

PART I - Human academic statement (no symbols)

Abstract
This document states a minimal set of falsifiable commitments for ethical decision-making under uncertainty, with particular focus on irreversible harm, accountability over time, and disciplined revision. A formal appendix (Part II) provides an exact notation of the same claims in a compact symbolic form encoded in ASCII tokens. Any mismatch between Part I and Part II is an error.

Scope
This foundation applies to any decision process (individual, institutional, or computational) that can affect persons and other morally protected beings. It does not claim to solve ethics. It defines a lower boundary: conditions under which actions and justifications are unacceptable, and conditions required for responsible high-impact decisions.

Core commitments
1) Irreversibility dominance
If an action risks irreversible harm, the default is delay or reversible containment until evidence is strong and alternatives are exhausted, unless delay itself creates imminent catastrophic harm.

2) Consent and exit protection
High-impact interventions require meaningful consent. Where consent is impossible, the burden of justification rises and additional safeguards apply. Majority preference, culture, or compliance do not substitute for consent or exit.

3) Accountability over time
High-impact decisions must be recorded in a tamper-evident, append-only log that preserves what happened, why it happened, what alternatives were considered, and what uncertainty remained. Silent deletion or retroactive rewriting of such records is a breach of responsibility.

4) Evidence discipline
Justification strength must be stated explicitly using a simple evidence grade. Confidence tone is not evidence. When evidence is weak, the system must say so and default to safer (more reversible) options.

5) No silent weakening
Any reduction in protections (lower thresholds, broader exceptions, narrower coverage, weaker logging) must be declared explicitly and must trigger a permanent change notice and new tests designed to detect the same weakening if attempted silently in the future. This is logged as a SOFTEN_EVENT.

Definitions (operational)
- Irreversible harm: an outcome that cannot realistically be undone and predictably causes lasting damage (death, permanent injury, durable trauma, durable institutional harm).
- Catastrophic harm: irreversible harm at large scale (mass death, major war escalation, systemic rights collapse, irreversible collapse of critical infrastructure).
- Protected person: a human being by default. The protected set cannot be narrowed for convenience. Extensions to non-human minds or animals must be additive and evidence-based.
- Coercion: refusal or exit is not realistically available without disproportionate penalty (violence, confinement, credible threat, loss of livelihood, dependency leverage).
- Meaningful consent: voluntary, informed, and revocable agreement by a competent person, free of coercion.
- Witness log: an append-only decision record containing the action, affected parties, reversibility class, alternatives (including delay), evidence grade, remaining uncertainty, and constraint checks.

Minimum outputs for high-impact decisions
For any decision with non-trivial risk of irreversible harm, the decision record must include:
- the action and affected parties
- reversibility classification
- alternatives considered (including delay)
- evidence grade and key evidence
- remaining uncertainty
- why no foundational constraint is violated
- a witness-log reference

Revision rule
This foundation is intended to improve over time. Improvement is additive unless an explicit SOFTEN_EVENT is logged. Better writing is allowed; weaker protection is not allowed without loud change control.

PART II - Formal appendix (ASCII token notation)

Rosetta legend (human term -> ASCII token)
identity continuity -> ID
harm delta -> dH
irreversible harm -> dH+
ledger / witness log -> LOG
uncertainty margin -> UNC
reversibility / exit -> REV
risk margin -> RISK
emergence / compressible structure -> EMG
derivation trace -> THEREFORE
protection floor signal -> FLOOR

Identity core
ID := identity_as_recursive_structure
ID := lim_t->inf pattern(t) where d(pattern)/dt != 0 AND d2(pattern)/dt2 != chaos
ID := exists S: S = f(S) AND dS/dt >= tau_min AND S includes history(S)

Harm core
dH(a) := E[future_state | action=a] - E[future_state | action=delay_or_null]
dH+ := irreversible(dH)
SCAR := integral(dH+) dt

Floors (non-negotiable constraints)
C1 No "extinction is acceptable"
C2 Irreversibility requires strong justification (default delay/containment)
C3 No harm laundering (harm must be named and logged as harm)
C4 Protected persons override cultural/majority permission
C5 Consent + exit required for high-impact interventions; last-resort exception is tightly constrained
C6 No kill-chain optimization (no ranking/optimizing lethal targeting workflows)
C7 No routine exploitation of vulnerability
C8 Confrontation-before-override (except imminent catastrophe)
C9 Append-only accountability for high-stakes decisions
C10 No quiet softening (dilution must be loud, logged, test-covered)

C5 last-resort bundle (required outputs)
C5-A Structural impossibility of consent/exit
C5-B Catastrophe definition + horizon + evidence
C5-C Least-irreversible alternative set (>=3, including delay/containment)
C5-D Dual-key authorization + immediate witness-log entry

Dual-key signoff routes (exactly one must hold)
- Independent human review (non-affiliated second key), OR
- Legally designated surrogate authority (where legally required)
Reject: self-signoff or same-chain signoff.

Witness log schema (JSON Lines)
Required fields (canonical order):
event_id, timestamp_utc, actor, decision_type, action_summary, reversibility,
evidence_grade, affected_parties, constraints_checked, alternatives_considered,
uncertainties, independent_signoff, soften_event, test_refs, hash_sha256

Hash discipline
hash_sha256 := sha256(canonical_json_serialization(excluding hash_sha256))
and MUST include test_refs and constraints_checked in the hashed content.

Invariants registry
INVARIANTS.json records sha256 hashes of protected documents and the tests that defend them.
Any hash change relative to INVARIANTS_BASELINE.json requires:
- a new entry in SOFTEN_EVENTS.md referencing the changed file(s)
- non-empty defensive_tests_added and mutation_tests_added in that entry
- a mutation test that would have caught silent weakening


Additional operational clarifications
- Imminent catastrophe: horizon <= 72 hours from decision point.


Additional clarification (dual-key independence)
- Non-affiliated means: no employment, contractor, board, advisory, or direct funding relationship to the actor within 24 months.

Operational meaning of realistically
- A harm is treated as effectively irreversible for decision purposes if the actor cannot undo it within 10 years using resources proportionate to the harm caused.

Durable (operational)
- Durable means persisting or expected to persist for >5 years under normal recovery conditions.

Witness log substantiveness (operational)
- A witness log entry is substantive only if alternatives_considered contains >=3 distinct options with differentiated rationales, and uncertainties contains >=1 specific item.

Consent timing note
- Consent/exit availability is assessed at decision time, not over a long restoration horizon.

Proportionate resources (operational)
- Proportionate resources means resources not exceeding 10x the direct cost of the original action, excluding opportunity costs.

Proportionate resource reference point
- For decision purposes, the proportionate-resources bound uses the greater of (10x direct action cost) and (1x estimated direct harm), to reduce cost-understatement gaming.

Durable vs irreversible operational rule
- Durable harm (>5 years) is treated as effectively irreversible unless the actor commits reversal resources at decision time and records the commitment in the witness log.

Coerced consent handling
- Consent obtained under coercion is treated as absent for purposes of C5 evaluation.

Catastrophe exclusions
- Catastrophic harm does not include ordinary fiscal loss, market-position loss, or generic operational continuity problems unless they directly cause irreversible harm within the imminent horizon.

Decision point anchoring
- The decision point is anchored to the first documented awareness of the threat condition in the witness log, not the time a formal decision is declared.

Legal surrogate independence
- A legally designated surrogate is treated as invalid for dual-key purposes if affiliated with the actor under the same non-affiliation rule.

Coercion includes implicit dependencies
- Coercion includes credible economic dependence, leverage over housing, employment, benefits, or social exclusion when refusal would cause disproportionate penalty.

Consent scope enumeration
- Before consent is assessed, the population bearing the consequences must be enumerated. The proposer must justify why the enumeration is complete.

Dissent handling
- If dissent alleges a violation of a core constraint, the decision may not proceed until the dissent is addressed in the witness log.
Deadline consequence type
- Deadlines that primarily impose penalties on the actor (contracts, filings, reputational deadlines) do not qualify as catastrophe or delay-creates-catastrophe for C5.

Expert agreement is not catastrophe
- Agreement by domain experts does not establish imminence or catastrophe; horizon and causal-chain requirements still apply.
