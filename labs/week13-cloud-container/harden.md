<!-- Sandbox/teaching only; for authorized lab use. -->

# Hardening Checklist — Misconfig → Fix

**OWASP 2025:** A02 Security Misconfiguration · **CWE:** CWE-732, CWE-16, CWE-250, CWE-526 (plus CWE-798, which OWASP files under A07)

`Dockerfile.insecure` and `Dockerfile.hardened` are both already written — this
lab is read-and-compare, not edit-and-rerun. Run `./scan.sh` once: its table
lists each file's finding count on its own row (`Dockerfile.insecure` has
findings, `Dockerfile.hardened` is `0`) — that row-to-row comparison **is**
"the findings disappearing." Re-running `./scan.sh` again scans the same
unchanged folder and gives the identical table; it is not a before/after step.

## Container image (`Dockerfile.insecure` → `Dockerfile.hardened`)

| # | Misconfiguration (insecure) | CWE | Fix (hardened) |
|---|------------------------------|-----|----------------|
| 1 | `FROM python:latest` (unpinned, mutable) | CWE-16 (configuration); CWE-1104 only if the selected base is actually unmaintained | Pin to a **digest** (`@sha256:...`); review provenance and vulnerabilities, then update the pin deliberately |
| 2 | Secret in `ENV API_TOKEN=...` | CWE-526 / CWE-798 / CWE-200 | **No secrets in image.** Inject at runtime via secrets manager / mounted secret |
| 3 | `COPY . .` (whole context) | CWE-538 | Copy only needed files; add a `.dockerignore` (exclude `.git`, `.env`, keys) |
| 4 | `chmod -R 777 /app` | CWE-732 | Default perms; app owned by non-root, not world-writable |
| 5 | Runs as root (no `USER`) | CWE-250 | `USER 65532:65532` (non-root); distroless `nonroot` |
| 6 | Unpinned `pip install` | CWE-16 (dependency configuration); unmaintained packages need separate evidence for CWE-1104 | Hash-pinned `requirements-hardened.txt` + `pip install --require-hashes`, in the build stage |

### Extra runtime hardening (not in the Dockerfile, enforce at deploy)
- `docker run --read-only --cap-drop ALL --security-opt no-new-privileges`
- Set resource limits (`--memory`, `--pids-limit`) to blunt DoS.
- Never `--privileged`; never mount the Docker socket into untrusted containers.

## IAM (`iam-policy-insecure.json` → `iam-policy-leastpriv.json`)

| # | Misconfiguration | CWE | Fix |
|---|------------------|-----|-----|
| 7 | `"Action": "*"` | CWE-269 | Enumerate only the actions used (e.g. `s3:GetObject`) |
| 8 | `"Resource": "*"` | CWE-732 | Scope to specific ARNs (one bucket + prefix) |
| 9 | No conditions | CWE-732 | Add `Condition` (e.g. `s3:prefix`, source IP, MFA) |

### Principle
**Least privilege + shared responsibility:** grant the minimum, on the
minimum, under the right conditions. The cloud provider secures *of* the
cloud; you secure what you put *in* it.

## Deliverable
Before/after `scan.sh` output (finding counts) + the diffed policy and
Dockerfile, with one sentence per fix on why it reduces risk.
