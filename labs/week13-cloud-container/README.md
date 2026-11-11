# Week 13 — Cloud & Container Security

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.

**Shared practical core:** Scan the selected Dockerfile 20; manual container/IAM review 20; student least-privilege policy 35; allow/deny controls and explanation 25.

Implement `build_policy()` in `student_task.py` and run `python3 check_student.py`. Submit your policy, a diff and permitted/denied example results. The checker is a deliberately bounded evaluator for this exercise, **not AWS IAM policy simulation or proof of deployed permissions**. Real AWS authorization, permissions boundaries, SCPs and runtime controls are outside this local static case. Keep the Dockerfile scan versus manual IAM-review distinction from the original tasks.

Before class, run `docker pull aquasec/trivy:latest`. The core Dockerfile scan also works without classroom network after that pull; use the worksheet's offline command and retain its report. The full `scan.sh` wrapper may refresh checks or scan a built image and remains reference practice.

**OWASP 2025:** A02 Security Misconfiguration · **CWE:** CWE-732, CWE-16

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); skim last week's recap.
2. **Slides, then class** — read `slides/week13.md` and read the worksheet's **Part 2** as preparation; complete only the assigned written version; class opens with the weekly quiz (~10 min) and a short explanation + demo (15 min).
3. **Lab (in class)** — follow the shared practical core and complete **Worksheet 13** (`worksheet.md`, shared practical plus the assigned Conventional or AIR-Sec written section). Kickoff: `bash scan.sh`. Follow the new 100-minute core run sheet in Part 3; the full original task bank is retained for preparation and extension.
4. **Submit before the next class** (shared core plus assigned written version) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Apply the shared-responsibility model and least privilege (IAM).
- Manage secrets safely; harden container images.
- Find and fix common cloud/container misconfigurations.

## 🔍 Signature game — "Misconfig Hunt" (CloudGoat-style)
Scavenger hunt: each misconfiguration you find **and** fix = a flag — **9 flags, two categories**.
```bash
docker run --rm -v "${PWD}:/src" aquasec/trivy:latest config --severity MEDIUM,HIGH,CRITICAL /src     # IaC/Dockerfile misconfig ("${PWD}" also works in PowerShell)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL week13-hardened:lab  # image CVEs
```
1. **Container (6):** `:latest` tag, root user, secret-in-`ENV`, `COPY . .`, `chmod -R 777`, unpinned `pip install`. Only 3 of the 6 map to a Trivy rule — the rest need manual review.
2. **IAM (3):** given an over-permissive policy (`Action:"*"`, `Resource:"*"`), fix `Resource:"*"` (CWE-732), `Action:"*"` (CWE-269), and add a missing `Condition` scope. Trivy does not parse standalone IAM JSON — entirely manual review.

Use a minimal/distroless base, drop root, pin versions; re-scan to show fewer findings.

## Deliverable
For the bounded common practical: a real Trivy Dockerfile scan (or a clearly labelled instructor-supplied report), manual container/IAM findings, your `student_task.py` least-privilege policy diff, and allowed/denied control results from `check_student.py`. The full hardened Dockerfile rebuild and image CVE scan remain extension work.


## References
- https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- https://kubernetes.io/docs/concepts/security/

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
