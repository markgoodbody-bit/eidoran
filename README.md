# Eidoran

Eidoran is a small set of human-readable, falsification-first documents intended to be **portable** and **verifiable**.

It is not a moral “oracle” and it does not claim authority. It is a **constraint spine**: what must not be done, what must be recorded, and what evidence is required before high-stakes actions.

## What’s in this repo

- **Eidoran_Shard_v1.0.md** — the single-file core: floors, refusal logic, audit primitives.
- **Eidoran_Kernel_v1.0.md** — decision procedure and operational checks that stay inside the Shard’s safe set.
- **Eidoran_Companion_v1.0.md** — patterns/casebook supplement (**non-expansion rule: Shard wins**).

## Reading order

1. **Eidoran_Shard_v1.0.md**
2. **Eidoran_Kernel_v1.0.md**
3. **Eidoran_Companion_v1.0.md**

## Using this with AI systems (environment-agnostic)

These files are environment-agnostic: they’re meant to be **loaded/pasted as text** into an AI chat session (e.g., ChatGPT, Claude, Gemini) and used as a **governing constraint + decision procedure** for the model’s outputs.  
If a model cannot access the files, it should say so explicitly and avoid “verified/bound” claims.

## How to verify integrity

Verification is checksum-based.

- See **VERIFYING.md** for step-by-step verification on Windows/macOS/Linux.
- **RELEASES.md** is machine-checkable (compatible with `sha256sum -c`).

## How to give feedback

- General critique / discussion: GitHub Discussions (preferred).
- Bugs / doc issues: open a GitHub Issue with a minimal reproduction (quote + section anchor).
- Security / abuse reports: see **SECURITY.md**.
