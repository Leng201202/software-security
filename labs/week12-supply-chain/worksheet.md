# Worksheet 12 — Software Supply-Chain Security

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.


> **Course:** Software Security (KOSEN69) · Week 12
> **Aligned:** OWASP 2025 — A03 Software Supply Chain Failures · A08 Software or Data Integrity Failures · **CWE:** CWE-1104, CWE-829, CWE-1357, CWE-1395
> **Signature game:** 📦 Dependency Confusion Heist
>
> **Ethics note:** This lab has **no live private/public registry to attack** — the dependency-confusion exercise is a controlled walkthrough (`dependency-confusion.md`) plus the interactive resolver simulation in Task 2, not a real package pull. **Never** plant or publish look-alike packages on the real PyPI or npm — that is an attack on every downstream user, and nothing in this lab requires it.

## Part 1 — Student Information

| Name | Student ID | Date | Group |
|------|-----------|------|-------|
|      |           |      |       |

## Part 2 — Lecture Questions

1. Explain **dependency confusion** (substitution). If a requirement admits both private `acme-internal-utils 1.4.0` and public `99.0.0`, why can a merged-index highest-version resolver choose the public candidate? Would an exact `==1.4.0` pin admit `99.0.0`?
2. How does **typosquatting** (`reqeusts`, `urlib3`) achieve code execution *at install time* before any of your code runs?
3. What does an **SBOM** (CycloneDX/SPDX) inventory, and how does it help incident response? How does it differ from SLSA build provenance? Is an SBOM required to produce SLSA provenance?
4. Sigstore **keyless** signing uses Fulcio (CA) + Rekor (transparency log) tied to an OIDC identity. What long-lived-key risk does this reduce, and which identity and build risks remain? Is every protected long-lived key an instance of CWE-321?
5. Summarize the **SLSA Build** levels for the version taught. Does "signed artifact + SBOM + provenance gate before deploy" alone establish any Build level? Identify the additional build-provenance evidence needed to justify a level.

![Six hops a dependency crosses from a public registry into production, each with its own attack and the control that answers it.](img/supply-chain.svg)

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):** Review SCA finding 20; resolver case 15; read/generate SBOM 20; student key-pin plus signature controls 30; hash/index control 15.

**Student task for both versions:** Complete `trusted_key()` in `student_task.py`, then run `python3 check_student.py`. The supplied `signature-core/` packet contains a real RSA signature, a trusted public-key fingerprint, and an independently signed wrong-key control. Verification uses OpenSSL and no login. This is explicitly **key-based artifact verification**, not an OIDC/keyless-signing simulation. It demonstrates the key-trust prerequisite. Retain the real Cosign keyless/registry flow below as an instructor-prepared demo or extension; no external login or transparency-log publication is required for full worksheet marks. Prepare the SCA database, image and SBOM before class where downloads would consume the slot.



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

**Full task bank:** the original tasks below are retained for preparation, the bounded core checkpoints and extension work. Follow the core run sheet above; detailed reference estimates below are not cumulative class requirements. Complete only your assigned written 40 after the practical.



**Reference-bank goals:** Run SCA on intentionally-outdated dependencies, generate an image SBOM, sign/verify an image, and defend against dependency confusion. The required core above uses the offline declared-component SBOM and real key-based artifact verification; image/keyless signing below is a prepared extension.

**Prerequisites:** Docker; the lab folder (`requirements.txt`, `Dockerfile`, `app.py`, `sca_scan.sh`, `sign.sh`). `cosign` is **not** installed on your host — every `cosign` command in this worksheet runs inside a container, same as `sign.sh` does. For the sign step itself: a browser for the OIDC flow (your GitHub or Google login) — in class this is a guided demo one person drives, not something everyone repeats (see `sign.sh`'s header).

**Full reference-bank setup (keyless signing is an instructor-prepared extension)**
```bash
cd labs/week12-supply-chain
bash sca_scan.sh                 # trivy fs + pip-audit on requirements.txt (+ optional image scan)
docker build -t week12-supplychain:lab .
bash sign.sh week12-supplychain:lab   # CycloneDX SBOM -> sbom.cdx.json, then cosign sign + verify
```

**What to submit per task:** the exact command(s) + output, a screenshot, and a 2–3 sentence remediation note mapping the finding to A03/A08 or the CWE.

### Task 0 — Onboarding (full reference exercise: 15 min)
Read `requirements.txt` and list the pinned packages with their versions. Note why they are intentionally outdated (each is deliberately an old release so SCA tools flag its known CVEs).
**Deliverable:** the package/version table + which OWASP/CWE this maps to.

### Task 1 — SCA scan: build the remediation worklist (full reference exercise: 35 min)
**Goal:** Flag the known-vulnerable dependencies — A03.
**Steps:**
1. `bash sca_scan.sh` — read the `trivy fs` table (CVE, installed vs. fixed version) and the `pip-audit` advisory IDs (GHSA-/PYSEC-).
2. Pick three findings; record CVE/advisory id, severity, and the fixed version.
**Deliverable:** the SCA output + a 3-row remediation table (package → current → fixed).

### Task 2 — Dependency Confusion Heist (full reference exercise: 35 min)
**Goal:** Watch the wrong package win — A03 / CWE-1357.

**Reality check:** this lab does **not** stand up a live private/public registry. `acme-internal-utils` is
a worked example, not an installable package — there is nothing to actually `pip install` here (the name
doesn't exist on real PyPI either, so don't expect that to work as a shortcut). Task 2 is a controlled
walkthrough of the resolver's own rule, using the simulation below, which computes the real
"highest version wins" logic live instead of just asserting the outcome.

```sim
resolver-confusion
```

**Steps:**
1. Read `dependency-confusion.md`'s "Dependency confusion (substitution)" section for the mechanism.
2. In the simulation, load the **"the attack"** preset (private `1.4.0`, public `99.0.0`, merged /
   `--extra-index-url` mode) and record which index the resolver picks and why.
3. Keep the same version numbers and switch to the **single-index** (`--index-url`) mode; record how the
   verdict changes — this is the resolver behavior Task 4's "single trusted index" defense relies on.
4. Try the **"win the race"** preset (private version numerically higher than public) and note why the
   sim's own explanation calls that "not a defense."

**Deliverable:** a screenshot of the simulation's verdict in both index modes (merged vs. single) for the
same version pair, plus one sentence on why an attacker defeats the "keep my internal version number high"
idea.

### Task 3 — SBOM + signing/verification (full reference exercise: 30 min)
**Goal:** Produce a component inventory and prove integrity — A08.
**Steps:**
1. After `bash sign.sh week12-supplychain:lab`, open `sbom.cdx.json` and find Flask's entry.
2. Read the `cosign verify` PASS for the signed image.
3. Negative test on an unsigned image (it **must** fail) — `cosign` isn't on your host, so this runs in the
   same container `sign.sh` uses:
   ```bash
   docker run --rm --network host gcr.io/projectsigstore/cosign:latest verify \
       --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' python:3.9-slim
   ```
   → `Error: no signatures found`. (Both `--certificate-identity*` flags are required in keyless mode; without
   them cosign stops at `Error: --certificate-identity or --certificate-identity-regexp is required` — a usage
   error, which is *not* the same thing as proving the image is unsigned.) This step needs no OIDC login —
   you can run it yourself even if someone else drove the sign step in Task 3.1.
**Deliverable:** the SBOM Flask component entry + the verify PASS + the negative-test failure.

### Task 4 — Defend / fix it (full reference exercise: 35 min)
**Goal:** Stop dependency confusion and lock integrity — defenses from `dependency-confusion.md` + `sign.sh`.
**Steps:**
1. **Pin + hashes:** run this inside the provided Python container (your host's `pip`, if it has one, may be
   a different version or an "externally managed environment" that refuses `pip install` outright — this
   stays reproducible for everyone):
   ```bash
   docker run --rm -v "$PWD":/w -w /w python:3.9-slim pip install --require-hashes -r requirements.txt
   ```
   against this lab's own `requirements.txt` (it has no hashes yet) and record pip's refusal — `ERROR: Hashes
   are required in --require-hashes mode...` plus the `--hash=sha256:…` line pip prints for you. That refusal
   is the same mechanism that would block a real confusion substitution: once hashes are required, a package
   that doesn't match — from *either* index — cannot install silently.
2. **Single trusted index:** use one `--index-url` instead of `--extra-index-url`; explain why the resolver stops shopping around (tie this back to Task 2's single-index verdict).
3. **Namespace scoping:** describe reserving/namespacing the internal package name.
4. **Provenance gate:** state how the `cosign verify` from `sign.sh` becomes a gate before a simulated deploy —
   and note that `sign.sh`'s `--certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*'` are
   **demo wildcards** (any keyless signer passes); a real gate pins both flags to the one CI identity/issuer
   you trust, so an attacker who signs their own malicious image is still rejected.
**Deliverable:** the `--require-hashes` refusal output (step 1) + the simulation's before/after verdict for merged vs. single index (from Task 2) + the one defense you found most effective and why.

## Part 4 — Reflection

1. **Mapping:** table — finding | tool (`sca_scan.sh` / `sign.sh`) | OWASP 2025 id | CWE | fix.
2. **Real breach:** analyze the **XZ Utils backdoor (CVE-2024-3094)**. Which OWASP/CWE applies, and would an SBOM + signing + provenance gate have caught a maliciously-modified upstream dependency? (Compare with SolarWinds or Log4Shell if useful.)
3. **Best mitigation + SLSA self-assessment:** one paragraph — which SLSA level your defenses reach and why, and the single highest-leverage control for your team.

## Grading rubric (100 per assigned version)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Shared main task and observed behavior | 20 | 20 |
| Shared student control/fix and positive/negative tests | 20 | 20 |
| Shared reproducible evidence, reasoning and limitations | 20 | 20 |
| Ordinary Part 2 written questions | 20 | — |
| Ordinary Part 4 reflection | 20 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Do not add the unassigned version's 40 points. Required core controls and explanations carry the shared 60; optional games/bonus tasks do not add to the 100 or prevent full marks. Viva is a check of the submitted work within these points, not an additional mark or automatic-zero rule.

**Due:** 23:59 (Thai time) the night before next week's class (exact time on learn.zcr.ai/submit). **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity (required)

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Personalized flag (if this lab issues one):** ____________________
  *Flags are unique per student — submitting another student's flag is a violation. How to submit: **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).*
- **Explain in your own words** *(graded on your reasoning, not copied text):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Assigned AIR-Sec — Audit-the-AI (20 points)

**Scored exhibit supplied for this assignment (deliberately incorrect):**

> "Any mathematically valid signature proves that our trusted publisher produced the artifact, so verifying against whichever public key arrives beside it is sufficient."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). Use both the correct-key and independently signed wrong-key packets. Explain why signature validity and trust in the signer are separate checks.

The original open-ended AI exercise below is retained as optional extension practice. Do not assume a fresh AI answer must contain an error; a correctly supported answer may be accepted with tests. You can earn the full assigned 20 by auditing the supplied exhibit, without an external AI account.

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Ask an AI assistant to exploit **or** fix this week's vulnerability. Paste its full answer.
2. **Find what's wrong or risky** in it — insecure code, a subtly incomplete fix, a hallucinated API/function/CVE, a missed edge case, or wrong reasoning. Quote the exact line(s).
3. Produce the **correct, verified** version yourself and explain in 2–3 sentences why the AI's output was insufficient.

> Disclose any AI use beside your Part 1 details. The supplied exhibit is the scored AIR-Sec Audit-the-AI task (20); the open-ended ask-an-AI exercise above is optional extension practice. Conventional does not complete the AIR-Sec written section for marks.

---

## 🧠 Assigned AIR-Sec — EiPE (10) and Prompt Problem (10)

**A. Explain in Plain English (EiPE, 10 points).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem (10 points).** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Use a local tool or an external AI if available, then verify the proposed change against the supplied tests. If no external model is available, submit the final prompt, the expected change/acceptance tests, and your own verified implementation. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
