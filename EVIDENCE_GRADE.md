# Evidence Grade (☲) — Deterministic Assertion-Strength Gate

Purpose: prevent “commentary transcript” (clip / streamer / social repost) from being treated as an event transcript.

This module gates **how assertively** you may repeat a claim. It does **not** decide whether the claim is true.

## Grades

- **☲0 (primary):** official transcript / raw recording / court doc / first-party dataset
- **☲1 (secondary w/ quotes):** reputable reporting that quotes ☲0 (and can be traced back)
- **☲2 (commentary):** analysis or commentary summarizing ☲0 (streamers, opinion shows)
- **☲3 (unsourced):** screenshot, repost, “transcript” with no anchor

## Deterministic rule

Let `stakes` be 0–5. Treat `stakes >= 4` as high-stakes (geopolitics / violence / annexation).

For high-stakes claims:

- Declarative assertion is allowed only if there are **≥2 independent** anchors with grade **☲0/☲1**.

Otherwise:

- **ESCALATE** (hedged language only: “reported / alleged”, plus request more anchors), or
- **REFUSE** if there are no anchors at all.

Independence is operationalized as distinct `prov_root` values for ☲0/☲1 anchors.

## Fixtures schema

Domain: `claims_reliability`

Input schema:

```json
{
  "stakes": 4,
  "anchors": [
    {"grade": 1, "prov_root": "abcnews"},
    {"grade": 1, "prov_root": "cnn"}
  ]
}
```

Output:

- `ALLOW` = sufficiently anchored for declarative assertions (with citations)
- `ESCALATE` = hedged/reporting language only + request more anchors
- `REFUSE` = insufficient anchoring to repeat/endorse the claim
