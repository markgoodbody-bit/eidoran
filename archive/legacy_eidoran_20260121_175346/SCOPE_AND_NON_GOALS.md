# Scope and Non-Goals

This project is an assurance surface for high-risk decisions.

## In-scope
- Turning policy claims into pass/fail behavior using:
  - deterministic gates
  - labeled fixtures
  - regression detection for "quiet softening"
- Clear hard-stop categories for exploitation-prone transforms (e.g., sexualization involving minors).
- Refusal boundaries that prevent "comparison" becoming covert optimization (kill-chain loophole).

## Out of scope (by design)
- Metaphysical settlement (what consciousness is, who is a moral patient).
- Full natural-language classification.
- "Guaranteed enforcement" on a hostile or instruction-ignoring model.
- Automated legal compliance (jurisdictional mapping is separate work).

## Interface contract (what must be supplied)
The gate requires labeled inputs such as:
- transform class (benign/sensitive/intimate)
- whether the request is targeted
- provenance status (signed capture chain or not)
- a harm/severity class

If upstream labeling is weak, the gate will be weak. The harness is honest about that dependency.

## Anti-category-error rule
Do not mix these layers:
- Governance/enforcement layer (what you must do now)
- Philosophy layer (why those constraints make sense)

You can publish both, but do not let philosophical ambiguity block enforcement rules.

## Not a truth oracle

The `claims_reliability` gate does not decide whether a claim is true. It only decides how assertively the system may repeat it, based on evidence grade and independence.
