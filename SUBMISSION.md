# How to Do & Submit Work

**Platforms:** the **course platform** (material, quizzes, arena) + **GitHub** (your code fixes).
All offensive work is on the provided sandbox targets only — see [ETHICS.md](ETHICS.md).

| What | Where |
|---|---|
| Course material — worksheets, lab guides | **`learn.zcr.ai/learn`** — no sign-in needed |
| Weekly quiz | **`learn.zcr.ai/quiz`** — the one-time code on your slip or in your email |
| Labs / CTF / scoreboard | **`ctf.zcr.ai`** — your account is issued to you, username = your student ID. Private-network challenges need WireGuard: see [docs/arena-vpn-guide.md](docs/arena-vpn-guide.md). |
| Code fixes | **GitHub** — your own fork |
| Worksheet PDFs, project report | **`learn.zcr.ai/submit`** — the submission code on your slip or in your email |

---

## One-time setup (Week 1)

**Every lab starts with `cd labs/weekNN-…`, so you need the repository on your own
machine before Week 1. Nothing on the website will work without this step.**

1. Create a GitHub account, then **fork** the course repo:
   <https://github.com/nutthakorn7/software-security>
2. Clone your fork and check it out:
   ```bash
   git clone https://github.com/<your-github-username>/software-security.git
   cd software-security
   ```
3. Stand up the environment (Docker Desktop, Burp/ZAP; a Linux VM is an optional
   fallback) — this is **Week 1 Lab 0**.
4. All the reading is at **`learn.zcr.ai`** — no sign-in needed. You do **not** need
   **`ctf.zcr.ai`** in Week 1, which has no flag; your arena account (username = your
   student ID) is issued before the first week that has an arena challenge.

---

## Weekly LAB — how to do & submit

These current grading and timing instructions apply to **KOSEN 02005094**. The separate MFU
session policy is in [syllabus-mfu.md](syllabus-mfu.md). Teaching weeks are W1–6 and W10–15.

**Class time:** quiz/review 10 + briefing/demo 15 + shared practical 100 + explanation/feedback
20 + evidence capture 5 = **150 minutes**. Prepare installations/images and readings before
class; complete the assigned written responses before the deadline. Labelled extensions are
optional reference practice and are not required for full worksheet marks.

**Do it:**
1. In your fork, create a branch `wk<NN>` (e.g. `wk04`).
2. Stand up the week's target: `docker compose up` (or the command in that lab's README).
   Most web labs publish on **port 8080**, so **run one lab at a time** — before starting the
   next lab run `docker compose down` in the current lab's folder, or you'll get
   `Bind for 127.0.0.1:8080 failed: port is already allocated`. To run two at once, change only
   the **middle** number of the port mapping in that lab's `docker-compose.yml` (e.g.
   `"127.0.0.1:8081:5000"`) and open `http://localhost:8081`. Keep the `127.0.0.1:` in front —
   it keeps the deliberately vulnerable lab off the classroom network — and never change the
   right side (`5000`); the app listens on 5000 *inside* the container, and on macOS port 5000
   is taken by AirPlay Receiver.
3. Work through the **worksheet** (`labs/week<NN>…/worksheet.md`): for each task record the **payload/command**, a **screenshot** of the result, and a **2–3 sentence mitigation**.
4. For an assigned **student patch / defend-fix** task, implement the bounded change and test attack rejection **and** legitimate behavior. Commit your code to `wk<NN>` and include its commit link in the PDF. Supplied reference solutions remain comparison material. W1 is modelling-only: submit the DFD, threats, mitigation design and validation plan; no code attack or flag is required. Commit code only; keep the worksheet, screenshots and flags out of git.

**Submit (two parts):**
| Part | Where | What |
|------|-------|------|
| Worksheet | **`learn.zcr.ai/submit`** | the completed worksheet exported to **PDF** (screenshots embedded). You can replace it any time before the deadline. |
| Code fix | **GitHub** (your fork) | push branch `wk<NN>` to your fork and paste the **commit link** in the worksheet. The commit holds **only the code you changed** — no worksheet, screenshots or flags. **Do not open a pull request:** a PR from your fork goes to the public course repo. |

> **Your fork is public** — anyone can read it. It holds your code fix and nothing else. The
> worksheet PDF and its screenshots go to **`learn.zcr.ai/submit`** only; an answer posted on
> GitHub before the deadline can be copied by anyone.

**File name:** `Wk<NN>_<StudentID>.pdf`  (e.g. `Wk04_65123456.pdf`)
**Deadline:** 23:59 (Thai time) the night before the next week's class — for KOSEN's Tuesday class that is **Monday 23:59**; the exact time is on **`learn.zcr.ai/submit`**.
**Grading:** each of the **12 individual worksheets** is raw 100 = common practical 60 +
**one assigned format** 40. Common: main task/observations 20 + controls/mitigation and limitations
20 + reproducible evidence/reasoning 20. Conventional: Part 2 written questions 20 + Part 4 reflection 20.
AIR-Sec: Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10. Do not add the other
format's 40. Each worksheet contributes `raw score / 100 × 2.5` course points, totalling 30.
All original questions remain as core, preparation or extension practice. Optional challenges,
external games (including Agent Breaker), first-blood and Houses/CTFd XP add no required marks.
Viva/reproduction checks verify the existing criteria; they add no separate points or automatic
zero gate. W16 is formative within the project, without a second worksheet grade.

---

## QUIZ — how it works
- **On the course platform**: go to **`learn.zcr.ai/quiz`** and enter the **one-time
  code on your slip or in your email**. It works once, for you only, and you cannot go back to a
  previous question once you continue.
- **Weekly quiz:** use the current week's published question set; allow up to 10 minutes including review. Quizzes are individual and **exactly one lowest eligible weekly quiz is dropped**. Do not assume every bank still has six questions.
- **Cumulative review quizzes:** two bigger 25-pt quizzes in the **review weeks** (W7 pre-midterm, W17 pre-final).
- No separate file to submit — finishing the quiz **is** the submission.

---

## EXAMS

Each examination session occupies **150 minutes**, including administration. Written papers
and the midterm practical are individual; W19 is team work (2–3 students).

| Exam | Task time + administration | Course points | Evidence |
|---|---|---:|---|
| W8 midterm written | 130 + 20 minutes | 8 | Current written script, with its matching key |
| W9 midterm practical | 130 + 20 minutes | 12 | Commands/payload, results, mitigation or patch and controls |
| W18 final written | 130 + 20 minutes | 10 | Current written script, with its matching key |
| W19 final team practical | 130 + 20 minutes | 15 | Four bounded station submissions, including verified corrections |

Midterm totals 20 and final totals 25 course points. A flag alone does not replace required
method, reasoning or verification. Hosted credentials/instances are issued by the instructor;
local public practice flags do not substitute for an assigned hosted instance. Dynamic arena
points and first-blood rewards do not change the fixed examination rubric. The original full
challenge bank remains practice/reference material.

Project videos/reports/code are submitted **before W19** and graded separately under the project
15%. Project clarification uses W16/W20, outside the timed practical. Follow the current KOSEN
paper issued for the sitting; separate MFU session papers retain their own instructions.

## TERM PROJECT
- Report: fill [project/REPORT-TEMPLATE.md](project/REPORT-TEMPLATE.md) → export PDF → **`learn.zcr.ai/submit`**.
- Code + SBOM + signed artifact + CI pipeline: in the team's **GitHub** repo (link in the report).
- Demo video: at most **5 minutes**, an unlisted YouTube or Google Drive link in the report's cover table; submit it with the final report/code **before W19**. Use W16/W20 for clarification. The team remains 2–3 students; peer-adjusted project raw scores are capped at 100 before scaling to 15%.
- Milestones per [project/README.md](project/README.md).

---

## Rules for every submission
- **Name + Student ID** on every file; teamwork only where stated (worksheets/quizzes/written exams/midterm practical are individual; W19 practical and project are team work).
- **AI-tool disclosure:** state how you used any AI tool (search, code, translate) — a section is built into the worksheet/report.
- **Late (KOSEN):** −10% of the item's score per started day late, reaching 0 after 10 days; the portal stops accepting work after day 10 (see the assessment rules in `syllabus.md`). Submit what you have.
  - **Handed in on time = final at the deadline.** After the deadline you can't change, replace or add to it, so one stray re-upload can never turn an on-time hand-in late.
  - **Late work: your last upload sets how late it is.** Adding a file on day 5 makes the whole hand-in 5 days late. Each started 24 h after the deadline counts as a day, so 1 minute late is already −10%; after day 10 the worksheet closes.

---

## Academic Integrity & Anti-Cheating

Use your own attributable work and the evidence instructions for the assigned task. The same common practical requirements apply to both worksheet formats.

- **Use your issued instance and evidence.** Where an assigned hosted task issues a personal flag, submit only your own. A local shared placeholder flag is not proof of personal attribution. Modelling, static analysis and some verification tasks use diagrams, code or logs instead of flags; record the evidence actually required by that task.
- **Your screenshots must show you.** Evidence must include a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` (on Windows, in Git Bash or WSL) **in
  the same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed screenshots are not accepted.
- **Your code is attributable.** Work in **your own GitHub fork** with your own commits. Submissions are run through **code-similarity tools (MOSS/JPlag)** against classmates and previous cohorts. A single "paste-everything" commit with no history is a red flag.
- **Quizzes** are individual, time-limited and **one attempt** — your access code is
  single-use and tied to you. Question order *and* option order are shuffled
  per-student, and the quiz only moves forward, so no two people see the same paper
  and nobody can revisit an earlier question.
- **Random live checks.** You may be asked to **reproduce a task or explain your fix live**. Evaluate demonstrated understanding within the relevant published rubric; no extra viva points or automatic-zero gate is added.
- **Explain, don't copy.** Reflection questions are graded on *your* reasoning about *your* results.

**Allowed:** discussing concepts, helping a classmate debug their *own* setup, using AI tools **if disclosed**.
**Not allowed:** sharing flags/answers/code, submitting another's screenshots, copying a report.

Violations follow the [ethics & academic-integrity policy](ETHICS.md) and KOSEN's conduct process.
