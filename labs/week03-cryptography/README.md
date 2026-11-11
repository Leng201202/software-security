# Week 3 — Cryptography Used Correctly (and Misused)

**OWASP 2025:** A04 Cryptographic Failures · **CWE:** CWE-327, CWE-916, CWE-330, CWE-321 (key case of CWE-798)

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Pre-pull images and prepare tools before class. The full concepts, longer questions and extension tasks stay available for preparation/follow-up; the instructor uses the bounded core below in class.

**Both assigned versions include the same common practical 60 points.** Complete that core plus **one** assigned 40-point section: **Conventional** = Part 2 written questions 20 + Part 4 reflection 20; **AIR-Sec** = Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10. Each version totals 100. The unassigned section is reference practice, not another required 40 points. Only the named 100-minute core is assessed in the shared 60; other practical tasks are optional extension/reference unless explicitly used in the assigned written questions, and are not a prerequisite for full marks. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Viva/reproduction checks verify the work within its existing rubric, with no separate score or automatic-zero rule. Complete the common practical evidence in either version, disclose any AI assistance, and use the normal name/Student ID and task-specific evidence requirements. Do not substitute a shared practice flag for proof from an actually assigned hosted instance.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); keep the Week 2 scanner images (`semgrep/semgrep`, `zricethezav/gitleaks`) and run `docker compose build` in this lab while online. The built `kosen-swsec-week03:local` image contains the pinned Python packages, so class tasks can run without a PyPI download. Skim last week's recap.
2. **Slides, then class** — prepare the concepts before class. The 150-minute slot includes quiz/review 10, a brief/demo 15, the common practical core 100, debrief 20 and evidence/exit 5.
3. **Lab (in class)** — complete the bounded common practical core. Baseline behavior (5), scanner observations (10), code review (15), token predictability (10), key-handling analysis (10), student rehash-on-login (30), fixed control checks (20). Then complete only the assigned Conventional written 40 or AIR-Sec 20/10/10; use preparation/follow-up time for the full selected written answers and extensions.
4. **Submit before the next class** (homework included) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: the class contract above and [Week 3 worksheet](worksheet.md). Grading: see the worksheet rubric.*

## Objectives
- Find crypto misuse in application code — with a scanner first, then by reading the code — and know why tools miss some of it.
- Store passwords with a vetted KDF (argon2id), and move legacy MD5 records to it with rehash-on-login.
- Keep keys out of source code, and use a CSPRNG for tokens.

How the primitives themselves work and break (cracking hashes, cipher modes, MACs, TLS) is taught in
Cryptography and Network Security (02005104). This week stays on the application-code side.

## 🔎 Signature game — "Misuse Hunt"
1. **Scan:** run Semgrep and Gitleaks on `vulnerable_crypto.py` and note what they flag — and what they don't.
2. **Hunt:** read the code with the checklist (MD5/SHA-1, `MODE_ECB`, key literals, `random` for secrets) and find all four mistakes with their line numbers.
3. **Remediate:** finish the rehash-on-login in `migrate.py` until it prints `ALL PASS`, then run the fixed version (argon2id, AES-GCM, `secrets`, key from `ENC_KEY_HEX`).

## Deliverable
The mistake table (line, mistake, CWE, flagged by a tool or not) + before/after code + a short note on which CWE each change closes.

## References
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
