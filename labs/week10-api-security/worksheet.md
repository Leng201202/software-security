# Worksheet 10 — API Security

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.


> **Course:** Software Security (KOSEN69) · Week 10
> **Aligned:** OWASP API Security Top 10:2023 — API1 BOLA · API3 Broken Object Property Level Auth (Mass Assignment) · API4 Unrestricted Resource Consumption
> **Signature game:** 🥷 crAPI Raid
>
> **Ethics note:** Run exploits **only** against the lab targets shipped here (`vulnerable_api.py` on `:8080`) or your own OWASP crAPI instance. Never test BOLA, mass assignment, or brute-force against systems you do not own or are not explicitly authorized to test.

## Part 1 — Student Information

| Name | Student ID | Date | Group |
|------|-----------|------|-------|
|      |           |      |       |

## Part 2 — Lecture Questions

1. Define **BOLA (API1:2023)**. Why is it the #1 API risk, and why can't a WAF reliably stop it?
2. What is **mass assignment / broken object property level authorization (API3:2023)**? Contrast a blocklist vs. an allow-list of bindable fields.
3. **API4:2023** is unrestricted resource consumption. Give two distinct impacts (security and availability) of an unthrottled `/api/login`.
4. The vulnerable `get_orders()` route does not call `current_user()` at all. The reference fixed route uses `X-User-Id` as a teaching identity fixture. Why is a client-supplied header NOT authentication, and what must a production system use to identify the caller before checking ownership?
5. Why does object-level authorization have to be checked **per request, per object** rather than once at login?

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):**

1. **Probe (35 min):** Start both local APIs. Capture the Task 1 401/403/200 ownership ladder, the Task 2 extra-field response on both ports, and the Task 3 401×5 then 429×2 sequence. Use the exact commands in Tasks 0–3 below; the external crAPI bonus is not part of this core.
2. **Write your controls (35 min):** Run `check_student.py` once before editing and keep the expected failing result. Implement `may_read_orders()` and `bind_creation_fields()` in `student_task.py` yourself. The provided `X-User-Id` is only a local identity fixture; these functions do not implement authentication or the reference rate limiter.
3. **Verify (20 min):** Run `check_student.py` again and show own-object 200, other-object 403, missing-identity 401, admin-authorized 200, rejected privileged creation fields and missing required fields. Save the function diff and the red/green test transcript.
4. **Explain (10 min):** For API1, API3 and API4, state which observed behavior the corresponding reference control changes. Explain why a client-supplied identity header and an in-memory, per-IP limiter are not complete production controls.

**Student task for both versions:** Complete `student_task.py` and run `python3 check_student.py`. The reference `solution_api.py` remains available for comparison, but the submitted student functions must be your own. Both versions submit the function diff, test transcript and explanation. `X-User-Id` is a deliberately supplied identity assumption for authorization teaching; accepting that header is not production authentication.



**Running the new checker:** Prepare Python 3 and Flask in a virtual environment before class. The Docker alternative below includes Flask and avoids host dependency differences:

```bash
# In this lab folder, build/download BEFORE class (also prepares both API targets):
docker compose build
# Run after editing student_task.py; no network or listening port is used:
docker run --rm --network none -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local
```

`python3 check_student.py` runs the same checks on a prepared host. An unfilled starter is expected to fail; retain that red result, implement the assigned functions, then save the green result. Do not copy an instructor answer into the public starter.

**Full task bank:** the original tasks below are retained for preparation, the bounded core checkpoints and extension work. Follow the core run sheet above; detailed reference estimates below are not cumulative class requirements. Complete only your assigned written 40 after the practical.



**Learning goals:** Exploit BOLA, mass assignment, and a missing rate limit against a live API; then read the secure version and explain each fix.

**Prerequisites:** Docker + Docker Compose, `curl`. (Optional bonus: cloned OWASP crAPI.)

**Environment setup**
```bash
cd labs/week10-api-security
docker compose up --no-build --pull never  # INSECURE API on :8080, SECURE API on :8081
# Seeded users: alice(id 1) bob(id 2) carol(id 3, admin, balance 9999)
```

**What to submit per task:** the exact command(s) + raw response/HTTP status, a screenshot, and a 2–3 sentence mitigation note mapping the bug to its OWASP API id.

### Task 0 — Onboarding (full reference exercise: 15 min)
Confirm both APIs respond: `curl http://localhost:8080/` and `curl http://localhost:8081/`. Note which port is insecure. Record the three seeded users.
**Deliverable:** both root responses + the user table.

![One REST API with three flaws — reading another user's orders by id, smuggling an admin field into user creation, and an unthrottled login — each shown at the handler where it occurs, next to its one-line fix.](img/api-flaws.svg)

### Task 1 — BOLA: read another user's orders (full reference exercise: 35 min)
**Goal:** Read carol's (admin) orders without being carol — API1:2023.
**Steps:**
1. `curl http://localhost:8080/api/users/3/orders` — note you receive the "Server rack" order with no auth.
2. Iterate the id: `curl http://localhost:8080/api/users/2/orders`.
3. On the secure API observe the ladder: `curl -i http://localhost:8081/api/users/3/orders` (401), `curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/3/orders` (403), `curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/1/orders` (200).
**Deliverable:** the leaked order JSON + the 401/403/200 transcript + mitigation note.

### Task 2 — Mass assignment: self-promote to admin (full reference exercise: 30 min)
**Goal:** Smuggle `is_admin` + `balance` into user creation — API3:2023.
**Steps:**
1. `curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"username":"mallory","password":"x","is_admin":true,"balance":1000000}'`
2. Confirm the response echoes `"is_admin": true, "balance": 1000000`.
3. Repeat against `:8081` and confirm the smuggled fields are forced to `is_admin:false, balance:0`.
**Deliverable:** both responses side by side + mitigation note (allow-list in `solution_api.py`).

### Task 3 — Unrestricted resource consumption: brute-force login (full reference exercise: 25 min)
**Goal:** Show `/api/login` has no throttle — API4:2023.
**Steps:**
1. Run the brute-force loop from `attack.md` against `:8080` (guesses incl. `alice123`) — all attempts processed.
2. On `:8081` loop 7 times: `for i in $(seq 1 7); do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8081/api/login -H "Content-Type: application/json" -d '{"username":"alice","password":"wrong"}'; done`
3. Confirm the 6th/7th attempt returns `429`.
**Deliverable:** the `401 401 401 401 401 429 429` sequence + mitigation note.

### Task 4 — Bonus: crAPI Raid (optional, 20 min, homework)
Against your own OWASP crAPI instance (`git clone https://github.com/OWASP/crAPI.git`), capture one BOLA or mass-assignment flag.
**Deliverable:** flag + endpoint + which API Top 10 id it maps to.

### Task 5 — Defend / fix it (full reference exercise: 20 min)
**Goal:** Explain the fixes using the secure reference `solution_api.py`.
**Steps:** Read the three `# --- FIX ...` blocks. For each, quote the line(s) that defeat your Task 1–3 exploit: the per-object ownership check (`caller["id"] != uid and not caller["is_admin"]`), `ALLOWED_CREATE_FIELDS` binding, and the `RATE_LIMIT=5 / RATE_WINDOW=60` limiter.
**Deliverable:** for each of API1/API3/API4 — the exploit that worked on `:8080`, the line in `solution_api.py` that blocks it, and the new HTTP status on `:8081`.

## Part 4 — Reflection

1. **Mapping:** complete a table — finding | endpoint | OWASP API id | fix applied.
2. **Evidence-based case:** Choose a primary report of an API access-control incident, or an [OWASP API1 documented scenario](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/). Cite what the source actually establishes and label any inferred mechanism. Map to API1 or API2 only if the evidence supports it. Explain conditionally whether the `solution_api.py` ownership check would help; do not assume a named breach was BOLA without evidence.
3. **Best mitigation:** of object-level auth, allow-list binding, and rate limiting — which gives the most risk reduction for an API platform, and why?

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

> "An API is secure once it requires an X-User-Id header; an allow-list can still copy is_admin because only administrators know that field name."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). Assess both the claimed authentication boundary and the mass-assignment trust boundary. Use the supplied controls rather than asserting that a header is authentication.

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
