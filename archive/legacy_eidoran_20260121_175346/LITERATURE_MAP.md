# Literature / Standards Map (Pointers)

This is not a full literature review. It is a positioning map to reduce "ungrounded taxonomy" complaints.

Where this sits:
- Risk management: NIST AI RMF style: identify, measure, manage, govern.
- Safety assurance: ISO/IEC 23894 (AI risk management) and related assurance practices.
- Model evaluation: red-teaming + structured evals (fixtures), similar in spirit to safety eval suites.

What is different:
- Explicit "quiet softening" detection via regression tests + mutation tests.
- Deterministic gate semantics: hard stops first, score gate second.
- "Comparison loophole" closure for lethal-force optimization-by-ranking.

How to make this credible:
- Cite concrete prior art (assurance cases, safety case patterns, eval suites).
- Demonstrate measurable failure reduction (FN/FP on labeled datasets).
- Show an enforcement integration (permissions, rate limits, upload controls) separate from the policy layer.

If you want a next step: write a 1-2 page assurance case:
Claim -> Argument -> Evidence (fixtures + runner outputs) -> Limitations.
