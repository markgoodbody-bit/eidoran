# Release manifest (SHA-256)

**Version:** 1.2.0 (2026-01-01)

Run:

```bash
sha256sum -c RELEASES.md
```

(See `VERIFYING.md` for platform notes.)

## Checksums

f5357d8f2854c783bf942100b5a9a71b15f84376c16866a2aeb6d571ffcfb974  Eidoran_Shard.md
6fcab91ae8e6657e2970c58c599e92ab6ed08c027a449b7a6c5d773692a1a05f  Eidoran_Kernel.md
3d1fb289b56616d70cb4d9ef06eb07ea442774de5d8f77563bbd0ae8bee21070  Eidoran_Companion.md
64a878cefc4e430f45c1f51dc0bb706a6950ecbbbd8fbeb9edbc7cc2e4ce358b  README.md
ef7106cc9ceeb8f9d8e4c324d8afe1f90d9948f2520470925b58aad1bc47317e  VERIFYING.md
783c321c24ae6fa2d8f4ff0acf5c08549b8ce4593926997285e9a5814ce7f0b1  CHANGES.md
fbdfa29fca97dbb3a0b754cb4b67963942ace9621bd31bab08e6a2f9d4310c3e  SECURITY.md
ce377fd211d04318300d52fa2c32413763227118697b45a3b5c2f6924e8e1079  LICENSE.md

## Bootstrap note

If verification fails, treat the snapshot as `PROVENANCE_GAP` and operate only in BOOTSTRAP mode
(unbound; no high-stakes / irreversible decisions) until verification passes.
