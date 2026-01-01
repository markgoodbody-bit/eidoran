# Security Policy (Eidoran)

**Current version:** 1.2.0 (2026-01-01)

## Scope

This project is a set of documents. The main “security” risks are:

- Integrity / tampering (silent edits, swapped files, checksum mismatch).
- Prompt-injection via documents that try to force a model to claim capabilities it doesn't have.
- Confusing or misleading verification instructions.

## Reporting

- **Non-sensitive issues** (typos, clarity problems, falsifiers, contradictions):
  open a GitHub issue.

- **Sensitive integrity issues** (e.g., suspected compromise, malicious rewrite, impersonation):
  use GitHub Security Advisories (preferred) or contact the repository owner via their public
  contact method on GitHub.

## Supported versions

- The latest version on the default branch is supported.
- Older tagged releases are “as-is” unless explicitly marked otherwise in RELEASES.md / CHANGES.md.

