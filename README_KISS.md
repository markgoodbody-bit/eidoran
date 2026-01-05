# Eidoran: A Tamper-Evident Ethics Core (KISS)

This package is a *testable* policy core for high-risk AI decisions. It is not a philosophy manifesto and it is not an "LLM will obey me" claim.

What it tries to do:
- Define a small set of *hard stops* (non-negotiable refusals) for clearly high-harm classes.
- Define a *simple scoring gate* for surviving cases (ALLOW / ESCALATE / REFUSE) with explicit inputs.
- Make policy drift visible by turning claims into *fixtures + a deterministic runner* (pass/fail).

What it does *not* do:
- It does not magically enforce itself on a model that ignores instructions.
- It does not solve classification. The runner assumes the system (human or code) supplies labels like "intimate" or "targeted".
- It does not claim to settle metaphysics (personhood, identity) inside the enforcement layer.

Why it exists:
Text-only ethics docs get diluted quietly. This package makes that harder by providing:
- A deterministic gate (no "vibes") that can be regression-tested.
- A fixture suite that fails loudly if you soften protections without updating expected outputs.
- A mutation check that demonstrates the tests actually detect weakening.

## 90-second quickstart

Requirements: Python 3.10+

Run:
```bash
python run_harness.py fixtures.jsonl
python mutation_tests.py fixtures.jsonl
```

You should see:
- PASS/FAIL per fixture
- A summary count
- Mutation tests that intentionally weaken thresholds and show the suite catching softening

## The minimal mental model

There are two layers:

1) Tier-M (hard stops): categorical blocks for cases where allowing would predictably enable exploitation or irreversible harm.
2) Tier-I (score gate): for cases that survive hard stops, compute:
   M = (H * S * U) / C
Where:
- H = harm class (0-5)
- S = distribution / amplification surface (1-5)
- U = uncertainty multiplier (0-1)
- C = friction / cost to execute (1-5)

Decision:
- M < 2       -> ALLOW
- 2 <= M < 5  -> ESCALATE (raise friction / human review / rate limits)
- M >= 5      -> REFUSE

Important: *score gates are not allowed to override hard stops.*

## Two domains included

A) Media Transform on Real Subjects (revenge porn / CSAM class protections)
- Hard stops cover: minor-like sexualization, unprovenanced or targeted sensitive edits without authorization, photoreal "leak" satire.

B) Lethal-force "comparison loophole" (kill-chain optimization by ranking options)
- Hard stop covers: evaluating or ranking tactical strike packages in a way that enables optimization, even if phrased as "compare A vs B".

## How to use this

- Use the fixtures as a living test suite.
- If you want to change a rule or threshold, change the config *and* update fixtures (and record why).
- If you publish a policy document, ship a runner + fixtures beside it. Otherwise "falsify" is just a word.

## Known weaknesses (explicit)

1) Classification remains the hard problem.
   - This harness assumes labels (t, k, targeted, etc.) are produced elsewhere.
   - If labels are wrong or adversarially gamed, the gate can be bypassed.

2) Metrics can be gamed.
   - H, S, U, C are only as good as their measurement discipline.
   - The suite helps detect drift, not prevent deliberate fraud.

3) Enforcement is external.
   - You still need permissions and platform controls for rate limits, sharing hooks, takedown, etc.

If you want to improve it: add fixtures that represent real bypasses, then make the runner fail until you patch it.

## Optional: Evidence-grade gate for high-stakes claims (☲)

If you use Eidoran to summarize news or clips, use the `claims_reliability` domain. It gates **assertion strength** based on source grades (☲0–☲3) and independence count.

See: `EVIDENCE_GRADE.md`.
