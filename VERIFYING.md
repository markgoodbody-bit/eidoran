# Verifying Eidoran

This repo is designed so you can verify artifact integrity **offline**.

## 1) Verify via RELEASES.md (recommended)

### Linux/macOS (or Git Bash / WSL)

From the repo root:

```sh
sha256sum -c RELEASES.md
```

You should see `OK` for every file.

### Windows PowerShell (built-in)

PowerShell does not ship `sha256sum` by default. Use `Get-FileHash`:

```powershell
# Compare every file in RELEASES.md against its expected SHA-256
Get-Content .\RELEASES.md |
  Where-Object { $_ -and (-not $_.StartsWith('#')) } |
  ForEach-Object {
    $parts = $_ -split '\s+', 2
    $expected = $parts[0].ToLower()
    $file = $parts[1].Trim()
    $actual = (Get-FileHash -Algorithm SHA256 $file).Hash.ToLower()
    if ($actual -ne $expected) { throw "HASH MISMATCH: $file`nexpected $expected`nactual   $actual" }
    else { "OK  $file" }
  }
```

## 2) Verify a GitHub release/tag (optional)

If you publish a GitHub Release:

- Treat the release asset ZIP as a convenience only.
- The authoritative integrity check is still `RELEASES.md` + file hashes in the repo.

Optional hardening (if you later want it): sign tags and/or release commits with GPG or SSH signing and document the public key fingerprint in the README.
