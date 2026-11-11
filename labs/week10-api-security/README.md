# Week 10 — API Security

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.

**Shared practical core:** Probe BOLA, mass assignment and throttling (35 min); implement object authorization and allow-list binding in `student_task.py` (35 min); run the positive and negative controls (20 min); explain the header-identity and rate-limit boundaries (10 min). The exact checkpoints and evidence are in the worksheet's Part 3 core run sheet.

Complete `student_task.py` and run `python3 check_student.py`. The reference `solution_api.py` remains available for comparison, but the submitted student functions must be your own. Both versions submit the function diff, test transcript and explanation. `X-User-Id` is a deliberately supplied identity assumption for authorization teaching; accepting that header is not production authentication.

**OWASP API Security Top 10:** API1 BOLA · API3 broken object property level auth (mass assignment) · API4 unrestricted resource consumption



**Running the new checker:** Prepare Python 3 and Flask in a virtual environment before class. The Docker alternative below includes Flask and avoids host dependency differences:

```bash
# In this lab folder, build/download BEFORE class (also prepares both API targets):
docker compose build
# Run after editing student_task.py; no network or listening port is used:
docker run --rm --network none -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local
```

`python3 check_student.py` runs the same checks on a prepared host. An unfilled starter is expected to fail; retain that red result, implement the assigned functions, then save the green result. Do not copy an instructor answer into the public starter.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); run `docker compose build` in this lab folder while online, then skim last week's recap.
2. **Slides, then class** — read `slides/week10.md` and read the worksheet's **Part 2** as preparation; complete only the assigned written version; class opens with the weekly quiz (~10 min) and a short explanation + demo (15 min).
3. **Lab (in class)** — follow the shared practical core and complete **Worksheet 10** (`worksheet.md`, shared practical plus the assigned Conventional or AIR-Sec written section). Kickoff: `docker compose up --no-build --pull never` → `:8080` (insecure) / `:8081` (secure). Follow the 100-minute core run sheet in Part 3; the full original task bank is retained for preparation and extension.
4. **Submit before the next class** (shared core plus assigned written version) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Map the REST/GraphQL attack surface.
- Exploit BOLA and mass assignment.
- Add per-object authorization and allow-list binding in the student task; explain the reference API's rate limiter and the limits of its identity fixture.

## 🥷 Signature game — "crAPI Raid"
Target: **the local API below** — that's the graded lab (see rubric), not crAPI.
1. **BOLA:** read another user's orders by id with zero ownership check (`/api/users/<id>/orders`).
2. **Mass assignment:** smuggle `is_admin`/`balance` into `POST /api/users`.
3. **Resource consumption:** hammer `/api/login` — no rate limit (`401×5 → 429×2`).
4. **Fix:** read `solution_api.py` and cite the exact line that blocks each exploit (the object-level ownership check, the `ALLOWED_CREATE_FIELDS` allow-list, and the rate limiter).

> **Bonus (optional, ~20 min, ungraded): crAPI** — OWASP's own intentionally-vulnerable API, real GUID-based BOLA. Capture-only — **no fix step**.
```bash
git clone https://github.com/OWASP/crAPI.git
cd crAPI/deploy/docker && docker compose -f docker-compose.yml up -d
```

## Run the local target
```bash
docker compose up --no-build --pull never  # vulnerable_api.py on :8080; solution_api.py on :8081
```
The secure API is `solution_api.py` (on :8081).

## Deliverable
Findings report (API Top 10 mapping) + fixes.

## References
- https://owasp.org/API-Security/  ·  https://github.com/OWASP/crAPI
