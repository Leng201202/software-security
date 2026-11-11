# Week 15 — DevSecOps: Putting It Together

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.

**Shared practical core:** Compare fail-open/closed 20; student authorization/logging fix 20; one prepared CI red run 30; corrected green/control run 20; evidence 10.

Complete the bounded fail-closed/logging functions in `student_task.py` and run `python3 check_student.py`. Add that same command as a job step in the prepared lab repository: first retain its failing run, then the corrected passing run. A local run is the required fallback when an external CI queue is unavailable, under the same criteria. The existing full scanner workflow and all three defect families remain extended project practice. No new public repository, PR or external service is created by running the local checker. Test a legitimate admin as well as missing, unknown, non-admin and lookup-error cases.

**OWASP 2025:** A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); run `docker compose build` in this lab folder while online, then skim last week's recap.
2. **Slides, then class** — read `slides/week15.md` and read the worksheet's **Part 2** as preparation; complete only the assigned written version; class opens with the weekly quiz (~10 min) and a short explanation + demo (15 min).
3. **Lab (in class)** — follow the shared practical core and complete **Worksheet 15** (`worksheet.md`, shared practical plus the assigned Conventional or AIR-Sec written section). Two run paths: **(a)** start the prepared local target with `docker compose up --no-build --pull never` → the **insecure** service on `:8090` (fails OPEN) vs the **secure** service on `:8091` (fails CLOSED + logs); **(b)** use the prepared CI repository for the pipeline gate, or the local checker if Actions is unavailable. Follow the 100-minute core run sheet in Part 3; the full original task bank is retained for preparation and extension.
4. **Submit before the next class** (shared core plus assigned written version) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Add logging/monitoring/alerting and fail-safe error handling.
- Build a CI/CD pipeline that enforces security gates.
- Understand vulnerability management and coordinated disclosure, framed by **CISA "Secure by Design"**.

## 🔴🔵 Signature game — "Break the Build" (Red vs Blue)
Use this lab's own pipeline template as the starting point: [`security-ci.yml`](security-ci.yml) (wiring steps in [`README-pipeline.md`](README-pipeline.md)).
- **Blue team** builds the gate:
  1. Add **SAST** (Semgrep), **SCA + IaC** (Trivy), and **secret scanning** (Gitleaks) jobs.
  2. Configure Semgrep to fail on selected-rule findings, Trivy on HIGH/CRITICAL, and Gitleaks on detected secrets; upload SARIF to the GitHub Security tab. Gate-step scanner errors also fail.
  3. Add structured security logging + an alert on auth failures; ensure errors **fail closed**, not open.
- **Red team** submits PRs trying to sneak a vuln/secret past the gate.
- **Score:** Blue gets points for each catch, Red for each bypass.

## Hand-in and extended pipeline practice
Required core: the student function diff, local failing-then-passing checker output, and one prepared CI red/green run where available, with the relevant logs and explanation. The full scanner PR exercise below is retained as extended project practice; its scoreboard does not add course points.

## References
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://docs.github.com/actions
