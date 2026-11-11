# Worksheet 15 — DevSecOps: Putting It Together

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.


> **Course:** Software Security (KOSEN69) · Week 15
> **Aligned to:** OWASP 2025 **A09 Security Logging & Alerting Failures** · **A10 Mishandling of Exceptional Conditions** (scanners also cover A02/A03/A07) · **CWE-636** (fail open), CWE-532 (logging sensitive data), CWE-209, CWE-489, CWE-798
> **Signature game:** 🔴🔵 *Break the Build* (Red vs Blue) — Blue scores per catch, Red scores per bypass.

> ⚠️ **Ethics note:** The pipeline and `sample-service.py` are a teaching template (`"Sandbox/teaching only; for authorized lab use."`). Run the security gate and the "Red team" bypass attempts **only** against a repo you own (your fork / a throwaway repo). Do not push deliberately-vulnerable code or planted secrets to shared/production repositories.

---

## Part 1 — Student Information

| Name | Student ID | Date | Group |
|------|-----------|------|-------|
|      |           |      |       |

---

## Part 2 — Lecture Questions

Answer in your own words (2–4 sentences each).

1. `README-pipeline.md` says each tool runs **twice** (report step, then gate step). Explain what each step is for: why the report step never fails, why the upload step uses `if: always()`, why the Security tab can show findings that the gate lets through (hint: the severity filter), and which step turns the build red.
2. What is the difference between **fail-closed** and **fail-open**? In `sample-service.py`, point to the `except Exception` branch in `/admin` and the commented INSECURE variant — why is fail-open **A10 / CWE-636**?
3. The `permissions:` block in `security-ci.yml` is `contents: read`, `security-events: write`. Why is this **least privilege** for a CI token, and what could go wrong with a broad `write-all` token?
4. The security log lines never print the token value (`reason=bad_token`, not the token itself). Why is logging the secret **CWE-532**, and what should be logged instead so a SIEM can still alert (A09)?
5. Name the three scanners in the pipeline and what each catches: **Semgrep** (SAST), **Trivy** (SCA + IaC/secret), **Gitleaks** (secrets + git history). Which OWASP categories does each map to per the README table?

---

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):** Compare fail-open/closed 20; student authorization/logging fix 20; one prepared CI red run 30; corrected green/control run 20; evidence 10. Build the local target with `docker compose build` before class; Flask is installed in the image rather than during startup.

**Student task for both versions:** Complete the bounded fail-closed/logging functions in `student_task.py` and run `python3 check_student.py`. Add that same command as a job step in the prepared lab repository: first retain its failing run, then the corrected passing run. A local run is the required fallback when an external CI queue is unavailable, under the same criteria. The existing full scanner workflow and all three defect families remain extended project practice. No new public repository, PR or external service is created by running the local checker. Test a legitimate admin as well as missing, unknown, non-admin and lookup-error cases.

**Full task bank:** the original tasks below are retained for preparation, the bounded core checkpoints and extension work. Follow the core run sheet above; detailed reference estimates below are not cumulative class requirements. Complete only your assigned written 40 after the practical.


> The task budgets below add up to 205 min. That is deliberate over-provisioning, not a schedule:
> Tasks 2–4 are dominated by Actions queue and scan wall-clock. Push the gate in class (Task 2);
> Tasks 3–5 wait on Actions runs and the Red/Blue results, so they are homework.
>

![Two panels: the CI gate in security-ci.yml, where a MEDIUM DS-0001 finding slips past the HIGH,CRITICAL threshold and the build goes green, and the /admin handler, where one except branch returns 200 with the flag while the other returns 403 and logs it.](img/fail-closed.svg)

**Learning goals:** wire tool-specific security CI gates (Semgrep selected rules, Trivy HIGH/CRITICAL, Gitleaks detected secrets), observe structured security logging + fail-closed handling locally, then play Break-the-Build.

**Prerequisites:** a **public** GitHub repo you own with Actions enabled — a throwaway repo holding only this lab folder works best (on a private repo the SARIF upload needs GitHub Code Security and fails, turning every job red; a fork of the course repo also scans every other week's deliberately vulnerable lab, so it cannot go green). Open your Task 4 PR inside **your own** repo, never against the course repo; `git`; Docker; Python + Flask for the local service.

### Environment setup (real commands)

```bash
# --- A) Wire the gate into a repo you own (README-pipeline.md §1) ---
# Copy the files of this lab folder to the ROOT of a new public repo you own,
# then run these commands inside that repo:
mkdir -p .github/workflows
cp security-ci.yml .github/workflows/security-ci.yml
git add .                                           # the workflow AND the lab files it scans —
                                                      # `git add .github/...` alone leaves
                                                      # sample-service.py etc. untracked, so the
                                                      # pushed workflow has nothing to find
git commit -m "ci: add security gate (Semgrep + Trivy + Gitleaks)"
git push        # runs on push/PR to main

# --- B) Run the sample service locally (logging + fail-closed) ---
# from this lab folder (labs/week15-devsecops-pipeline in the course clone).
# Plain `pip install flask` fails on current macOS/Homebrew Python and some
# managed WSL installs ("externally-managed-environment") — use a venv:
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install flask
python sample-service.py
# In another shell (same venv not needed, curl has no Python dependency):
curl -s -X POST localhost:5001/login -H 'Content-Type: application/json' -d '{"token":"nope"}'   # 401 authn_failure
curl -s localhost:5001/admin -H 'Authorization: bob-token'    # 403 authz_failure
curl -s localhost:5001/admin -H 'Authorization: alice-token'  # 200 (admin)
```

**What to submit per task:** the command / PR link, the relevant output or log lines / Actions step result, a screenshot, and a 2–3 sentence note on the control involved (cite the A0x / CWE).

### Tasks

- **Task 0 — Onboarding (full reference exercise: 15 min).** Run the sample service; trigger the three curls above. **Deliverable:** screenshot of the structured `event=...` security log lines for authn_failure, authz_failure, and authz_success.

- **Task 1 — Logging & fail-closed (full reference exercise: 35 min, A09/A10).** *Goal:* prove fail-closed behavior. *Steps:* read `/admin` in `sample-service.py`; explain why the broad `except Exception` returns **403, not the secret**, and why `type(exc).__name__` (not the message) is logged (CWE-209). Identify the line that would make it fail *open* (the commented INSECURE variant). *Deliverable:* the log lines + a 2–3 sentence explanation of fail-closed vs fail-open.

- **Task 1b — Break the Build, live (full reference exercise: 25 min, A10 / CWE-636).** *Goal:* exploit a real fail-open, then prove the fix. *Steps:* from the current lab directory (Setup B already put you there — `cd labs/week15-devsecops-pipeline` again from inside it fails, "no such file or directory"), run `docker compose up -d --no-build --pull never` after the pre-class build (spawns the **insecure** service on `:8090` and the **secure** one on `:8091`). As **Red**, hit the insecure admin route with **no** Authorization header — the fail-open path leaks the admin panel *and* the flag (a local run returns the public demo flag; a personal flag applies only if the instructor has actually issued an instance):
  ```
  curl -s localhost:8090/admin                                  # {"panel":"UNLOCKED","secret":"FLAG{devsecops_...}"}  <- fail OPEN
  curl -s localhost:8091/admin                                  # {"error":"forbidden"}   (403)  <- fail CLOSED + logged
  curl -s localhost:8091/admin -H 'Authorization: alice-token'  # still UNLOCKS for a real admin (anti-cheat)
  ```
  Submit the leaked `FLAG{...}`. *Deliverable:* the flag, the two contrasting `/admin` responses (`:8090` leak vs `:8091` deny), and the exact line in `insecure_service.py` that fails open. *The local checker tests rejection and legitimate admin behavior. Use a hosted verifier only when the instructor has actually issued that environment; this worksheet does not assert that one is configured.*

- **Task 2 — Stand up the gate (full reference exercise: 35 min).** *Goal:* get the workflow running. *Steps:* push `security-ci.yml`, open the Actions run, confirm the three jobs (`semgrep`, `trivy`, `gitleaks`) execute and SARIF appears in the Security tab. *Deliverable:* screenshot of the Actions run + the Code scanning alerts page.

- **Task 3 — Blue team: pass the gate (full reference exercise: 30 min).** *Goal:* a green build. *Steps:* ensure the protected repo has no HIGH/CRITICAL findings and no secrets; fix or justify-and-document any (no blanket-ignore, per README §4). Expect a red baseline before you change anything:
  - **Semgrep flags every `uses: …@vN` tag (pin it to a commit SHA).** `security-ci.yml`'s own `aquasecurity/trivy-action@ed142fd0...` lines are the worked example of the *result* — here's how to get there for `actions/checkout@v4` and `github/codeql-action/upload-sarif@v3`:
    ```bash
    git ls-remote https://github.com/actions/checkout v4
    git ls-remote https://github.com/github/codeql-action v3
    # <sha>  refs/tags/v4   -- replace `uses: actions/checkout@v4` with
    # uses: actions/checkout@<that sha>  # v4
    ```
    Also fix `host="0.0.0.0"` (needed so Docker can publish the port — justify it with a `# nosemgrep` comment and a reason).
  - **Gitleaks flags the docs' own `-H 'Authorization: alice-token'` examples** (`curl-auth-header`, a false positive). The fingerprint is `<commit-sha>:<file>:<rule-id>:<line>` and the commit SHA is specific to **your** repo, so there is no value to copy here — get your real ones and add each as its own line in `.gitleaksignore` with a comment:
    ```bash
    docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest detect -s /repo -v
    # each finding prints a line like:  Fingerprint: <sha>:README-pipeline.md:curl-auth-header:92
    ```
    ```
    # .gitleaksignore — false positives only, never a real secret (reviewed, see worksheet Task 3)
    <sha>:README-pipeline.md:curl-auth-header:92  # docs example token, not a real credential
    <sha>:worksheet.md:curl-auth-header:70         # same
    ```
    Re-run Gitleaks after adding it to confirm `no leaks found` and exit code `0`.
  *Deliverable:* link to the passing run, the two action SHAs you pinned, and your `.gitleaksignore` diff.

- **Task 4 — Red team: Break the Build (full reference exercise: 40 min).** *Goal:* make the gate say **no**. *Steps:* on a branch/PR, inject *one* planted defect (per README §5), each aimed at a different gate step (a root Dockerfile also trips Semgrep, and a token also trips Trivy's secret scan): an outdated vulnerable dependency (e.g. an old `urllib3`) → Trivy SCA; a Dockerfile that runs as **root** — drop the `USER` line, or write `USER root` → Trivy config (`DS-0002`, HIGH); or a hard-coded token → Gitleaks. Open the PR and watch the matching gate step fail. *Deliverable:* screenshot of the **failing** gate step + which job caught it (Trivy SCA / Trivy config / Gitleaks) and which `exit-code: "1"` / `--error` step enforced it.
  > **Why root and not `chmod 777`.** Both gate steps filter to `--severity HIGH,CRITICAL`, and Trivy's Dockerfile scanner has no rule for `chmod` at all — it checks instruction-level `RUN`/`COPY` semantics, exactly as Week 13 Task 1 says. `chmod 777` therefore returns **nothing**, at any severity, and the build goes green: a defect that slips the gate is a Task 5 *Red point*, not a Task 4 screenshot. `:latest` is no good either — that is `DS-0001` and Trivy rates it MEDIUM, which this gate filters out. Running as root is `DS-0002` HIGH, so it fails the build for real.

- **Task 5 — Score Break-the-Build (full reference exercise: 25 min).** *Goal:* tally Red vs Blue. *Steps:* one Blue point per finding the gate caught, one Red point per finding that slipped through; for any bypass, propose the rule that would have caught it. *Deliverable:* scoreboard + one proposed gate improvement.

---

## Part 4 — Reflection

1. **Mapping.** For three controls you exercised, give: control → A09/A10 (or A02/A03 for a scanner) → CWE → one-line rationale.
2. **Real incident.** Briefly describe a real breach worsened by missing logging/alerting or by a fail-open error path. Which control here would have changed the outcome?
3. **Best mitigation.** Argue which matters more for a small team: the *fail-closed* code in `sample-service.py`, or the *CI gate* in `security-ci.yml` — and why both together beat either alone.

---

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

> "A green Actions run proves every vulnerability is absent and guarantees that GitHub prevents merging a vulnerable pull request."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). Distinguish the configured checks and thresholds from complete coverage, and workflow status from enforced repository rules.

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
