# Week 12 — Software Supply-Chain Security

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.

**Shared practical core:** Review SCA finding 20; resolver case 15; read/generate SBOM 20; student key-pin plus signature controls 30; hash/index control 15.

Complete `trusted_key()` in `student_task.py`, then run `python3 check_student.py`. The supplied `signature-core/` packet contains a real RSA signature, a trusted public-key fingerprint, and an independently signed wrong-key control. Verification uses OpenSSL and no login. This is explicitly **key-based artifact verification**, not an OIDC/keyless-signing simulation. It demonstrates the key-trust prerequisite. Retain the real Cosign keyless/registry flow below as an instructor-prepared demo or extension; no external login or transparency-log publication is required for full worksheet marks. Prepare the SCA database, image and SBOM before class where downloads would consume the slot.

*(Merges the former Dependencies and Integrity/Provenance weeks into one.)*

**OWASP 2025:** A03 Software Supply Chain Failures, A08 Software or Data Integrity Failures · **CWE:** CWE-1104, CWE-829



**Running the new checker:** Prepare Python 3 and OpenSSL on `PATH` before class. The Docker alternative below includes OpenSSL and avoids host dependency differences; this signature core does not need Flask:

```bash
# In this lab folder, build/download BEFORE class:
docker build -f Dockerfile.student -t softsec-student-checks:local .
# Run after editing student_task.py; no network or listening port is used:
docker run --rm --network none -v "$PWD:/work:ro" -w /work softsec-student-checks:local
```

`python3 check_student.py` runs the same checks on a prepared host. An unfilled starter is expected to fail; retain that red result, implement the assigned functions, then save the green result. Do not copy an instructor answer into the public starter.

### Offline core commands

```bash
python3 sbom_core.py                  # real CycloneDX 1.5 component inventory
python3 resolver_core.py --mode merged
python3 resolver_core.py --mode single
python3 check_student.py              # after implementing trusted_key()
```

`sbom_core.py` inventories the nine pinned entries in this lab's `requirements.txt`; `sbom-core.cdx.json` is its supplied reference output. It does **not** claim to list resolved transitive dependencies, installed image packages, CVEs or provenance. Identify Flask's component and explain the scope; the prepared image/Syft inventory remains the broader extension. `resolver_core.py` is an executable, bounded single-package numeric-version model; it demonstrates merged-vs-single-index selection without downloading packages, not pip's full dependency resolver. For an offline SCA case, inspect `sca-core.snapshot.json`: an actual pip-audit 2.10.1 run of these nine pins, with the run time, command and scope recorded. Advisory IDs/aliases/fixed versions are extracted; descriptions and severity are not supplied. Counts belong to that captured advisory database, not a promise of current completeness. Label it as supplied evidence and explain its conclusions rather than claiming a personal scan. For the offline hash control, independently compute SHA-256 of `signature-core/artifact.txt`, compare it with the issued manifest, then alter a temporary copy and show the mismatch. The original package `--require-hashes` download exercise remains extension practice.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); skim last week's recap.
2. **Slides, then class** — read `slides/week12.md` and read the worksheet's **Part 2** as preparation; complete only the assigned written version; class opens with the weekly quiz (~10 min) and a short explanation + demo (15 min).
3. **Lab (in class)** — follow the shared practical core and complete **Worksheet 12** (`worksheet.md`, shared practical plus the assigned Conventional or AIR-Sec written section). Kickoff: inspect the supplied `sca-core.snapshot.json` and run the offline commands above; `bash sca_scan.sh` is a live-scan extension that needs prepared scanner images and advisory databases. Follow the 100-minute core run sheet in Part 3; the full original task bank is retained for preparation and extension.
4. **Submit before the next class** (shared core plus assigned written version) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Explain why the supply chain is now a top-tier risk; recognize dependency confusion, typosquatting, malicious packages, transitive risk.
- Interpret the supplied, dated SCA results; run a fresh scan only when the scanner images and advisory databases are prepared.
- Generate/read an SBOM (CycloneDX/SPDX); explain SLSA provenance levels.
- Verify a real artifact signature against the issued trusted key; distinguish integrity, trusted signer identity and provenance. Retain Sigstore/Cosign keyless/OIDC signing as prepared extension practice.

## 📦 Resolver case and prepared keyless-signing extension
**Round 1 — Attack:** no live registry ships with this lab — walk the resolver's own "highest version wins" rule via `dependency-confusion.md` and the embedded resolver simulation (Worksheet 12 Task 2) and watch the wrong package win the version comparison.
```bash
# SCA: this is a Python lab (no package.json, so no npm audit) — trivy fs on
# requirements.txt, then pip-audit; run both with:
bash sca_scan.sh
```
**Prepared extension — real keyless signing:** pin versions / add a lockfile and registry scoping. Run the following only when the instructor has preflighted registry, digest, networking and OIDC access; the offline signature core above earns the required control marks:
```bash
docker build -t week12-supplychain:lab .
bash sign.sh week12-supplychain:lab   # pushes to a throwaway local registry, SBOM, cosign sign + verify
```
- Produce an SBOM and identify the component inventory.
- Show a tampered/unsigned image **fails** verification.
- Add a provenance/attestation gate before a simulated deploy.

## Deliverable
Required core: SCA/SBOM observations, resolver/hash-index analysis, the student key-pin diff and the real-signature positive/tamper/wrong-signer transcript. A prepared keyless-signing transcript and SLSA self-assessment are extension material; distinguish component inventory, signature integrity and provenance claims.

## References
- https://slsa.dev/  ·  https://www.sigstore.dev/  ·  https://cyclonedx.org/
- https://owasp.org/www-project-dependency-check/

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
