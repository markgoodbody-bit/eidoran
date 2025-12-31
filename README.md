# Eidoran

Eidoran is a small set of human-readable, falsification-first documents intended to be **portable** and **verifiable**.

It is **not** a moral “oracle” and it does **not** claim authority. It is a constraint spine: what must not be done, what must be recorded, and what evidence is required before high-stakes actions.

## What’s in this repo

- **Eidoran_Shard.md** — the single-file “core”. Floors, refusal logic, and audit primitives.
- **Eidoran_Kernel.md** — decision procedure and operational checks that stay inside the Shard’s safe set.
- **Eidoran_Companion.md** — patterns/casebook supplement (non-expansion rule: Shard wins).

## Reading order

1. Eidoran_Shard.md
2. Eidoran_Kernel.md
3. Eidoran_Companion.md

## How to verify integrity

Verification is checksum-based.

- See **VERIFYING.md** for step-by-step verification on Windows/macOS/Linux.
- The file **RELEASES.md** is machine-checkable (compatible with `sha256sum -c`).

## How to give feedback

- **General critique / discussion:** use GitHub Discussions (preferred).
- **Bugs / doc issues:** open a GitHub Issue with a minimal reproduction (quote + section anchor).
- **Security / abuse reports:** see **SECURITY.md**.
