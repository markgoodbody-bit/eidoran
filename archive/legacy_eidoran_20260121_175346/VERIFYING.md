# Verifying an Eidoran snapshot (SHA-256)

This repo uses file checksums to make silent tampering harder to miss.

**Current version:** 1.2.1 (2026-01-01)

## What you are verifying

You are verifying that the contents of the repo files in your local folder match the
hashes listed in `RELEASES.md`.

**Important:** `RELEASES.md` itself needs a trust anchor (e.g., a Git tag, a GitHub Release,
or an out-of-band copy). Checksums detect changes; they do not, by themselves, tell you
which source to trust.

## macOS / Linux

From the repo folder:

```bash
sha256sum -c RELEASES.md
```

If `sha256sum` is not available (some macOS setups), use:

```bash
shasum -a 256 -c RELEASES.md
```

Success looks like every listed file ending in `OK`.

## Windows

### Option A (recommended): WSL

Use Windows Subsystem for Linux and run the macOS/Linux command above.

### Option B: PowerShell (manual compare)

```powershell
Get-FileHash .\Eidoran_Shard.md -Algorithm SHA256
Get-FileHash .\Eidoran_Kernel.md -Algorithm SHA256
Get-FileHash .\Eidoran_Companion.md -Algorithm SHA256
```

Compare the printed hashes with the corresponding lines in `RELEASES.md`.

## If verification fails

- Treat the snapshot as **unverified** (`PROVENANCE_GAP`).
- You may still read/test in **BOOTSTRAP mode**, but **do not claim bound status** and do **not**
  use Eidoran for high-stakes / irreversible decisions until verification passes.
- Re-download or re-clone from a trusted anchor and re-run the check.

