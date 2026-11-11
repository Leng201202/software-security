# Worksheet 3 — Cryptography Used Correctly (and Misused)

> **Course:** Software Security (KOSEN69) · **Week 3**
> **Aligned to:** OWASP 2025 (A04 Cryptographic Failures [CWE-327, CWE-916, CWE-330, CWE-321], A07 Authentication Failures [CWE-798]) · CWE-327, CWE-916, CWE-330, CWE-321, CWE-798
> **Signature game:** "Misuse Hunt" (find four crypto mistakes in 26 lines of code — with scanners, then with your own eyes)

> **This week's angle.** *How* hashes, ciphers, MACs and TLS work and break is taught in
> **Cryptography and Network Security (02005104)**, where cracking weak hashes, cipher modes, AEAD and
> TLS each get a full lab. This course does not repeat those attacks. Here you work on the
> application side: **find** crypto misuse in code, see what tools miss, and **fix** it with the right
> library call.

> **Ethics note:** Scan and test only this lab's files and your own fork of the project.

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Pre-pull images and prepare tools before class. The full concepts, longer questions and extension tasks stay available for preparation/follow-up; the instructor uses the bounded core below in class.

**Both assigned versions include the same common practical 60 points.** Complete that core plus **one** assigned 40-point section: **Conventional** = Part 2 written questions 20 + Part 4 reflection 20; **AIR-Sec** = Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10. Each version totals 100. The unassigned section is reference practice, not another required 40 points. Only the named 100-minute core is assessed in the shared 60; other practical tasks are optional extension/reference unless explicitly used in the assigned written questions, and are not a prerequisite for full marks. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Viva/reproduction checks verify the work within its existing rubric, with no separate score or automatic-zero rule. Complete the common practical evidence in either version, disclose any AI assistance, and use the normal name/Student ID and task-specific evidence requirements. Do not substitute a shared practice flag for proof from an actually assigned hosted instance.

## Part 1 — Student Information
| Name | Student ID | Date | Group |
|---|---|---|---|
| | | | |

## Part 2 — Lecture Questions
Answer in your own words (2–4 sentences each), from this week's slides.
1. Hashing, encryption and encoding are three different tools. Which one does `store_password()` in `vulnerable_crypto.py` use, which one does `encrypt_ecb()` use, and why is Base64 never a way to protect a secret?
2. In Week 2, Semgrep flagged MD5. Give two reasons a pattern-matching scanner can miss a crypto mistake such as a weak reset token or a hardcoded key.
3. Why is an encryption key written in source code dangerous even in a private repository, and why does deleting it in a new commit not fix the leak?
4. An app has 10,000 users whose passwords are stored as unsalted MD5. Why can't you convert them all to argon2id tonight, and how does *rehash-on-login* solve it?
5. What's the difference between `random` and a CSPRNG (e.g. `secrets`), and where does it matter?

![Four paired rows showing that password storage, cipher mode, randomness and key source are four separate crypto decisions: MD5 (CWE-916/327) becomes argon2id, AES-ECB with a hardcoded key (CWE-327) becomes AES-GCM with a nonce and tag, a 6-digit random.choice token (CWE-330) becomes secrets.token_urlsafe, and HARDCODED_KEY (CWE-798) becomes a key injected from the environment — so naming AES answers none of the four questions.](img/crypto-misuse.svg)

## Part 3 — Shared practical core (100 min in class)

**100-minute core:** Baseline behavior (5), scanner observations (10), code review (15), token predictability (10), key-handling analysis (10), student rehash-on-login (30), fixed control checks (20).

All original task/question text remains below. The minute labels are activity budgets; the extended task set is preparation/follow-up, not extra work to fit inside the 100-minute core. Complete Part 2/Part 4 only for the assigned Conventional 40, or Audit/EiPE/Prompt only for the assigned AIR-Sec 40.


**Learning goals:** find four crypto misuses in application code — first with scanners, then by reading the code — and fix them with the right library call: a vetted KDF with a migration path, authenticated encryption, a CSPRNG, and a key from the environment.
**Prerequisites:** Docker, the scanner images from Week 2 (`semgrep/semgrep`, `zricethezav/gitleaks`), and this lab's prepared `kosen-swsec-week03:local` image. Build the lab image while online before class; no new tool is needed during the practical.

**Environment setup**
```bash
cd labs/week03-cryptography
docker compose build        # once before class, while online; installs pinned Python packages
docker compose up           # runs both scripts without downloading packages
# or locally:
pip install pycryptodome argon2-cffi
python vulnerable_crypto.py # prints an md5 digest, an ecb ciphertext and a 6-digit token
```
Targets: `vulnerable_crypto.py` (four crypto mistakes, not labelled), `migrate.py` (Task 5) and `solution_skeleton.py` (the fixed version).

**What to submit per task:** the command run + a screenshot of the result + the short answer the task asks for.

**Task 0 — Onboarding (5 min, in class)** · *Goal:* see what the code produces. *Steps:* run `docker compose up` (or `python vulnerable_crypto.py`); note the `md5:`, `ecb:` and `token:` lines. *Deliverable:* screenshot of the program output.

**Task 1 — Let the tools look first (10 min, in class)** · *Goal:* see what a scanner finds on its own. *Steps:* from `labs/week03-cryptography`, run the two Week 2 tools on `vulnerable_crypto.py`:

```bash
docker run --rm -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config p/python --metrics=off vulnerable_crypto.py
docker run --rm -v "$PWD":/src zricethezav/gitleaks:latest \
    detect --no-git --source /src/vulnerable_crypto.py --no-banner
```

If the Semgrep registry is unavailable, use the supplied narrow rule offline and label that result as the **local fallback**:

```bash
docker run --rm --network none -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config semgrep-local.yml --metrics=off --disable-version-check vulnerable_crypto.py
```

Write down every finding (rule name and line), or "no findings", and which ruleset you used. The local fallback checks MD5 calls only; it cannot establish that the other crypto decisions are safe. If the registry rule prints SHA-256/SHA-3 advice, judge whether that is the right fix **for storing passwords**. *Deliverable:* screenshot of both scanner outputs + your list of findings + one line judging the advice or the fallback rule's limit.

**Task 2 — Find the rest by reading (15 min, in class)** · *Goal:* do the review the tools could not. *Steps:* read `vulnerable_crypto.py` (26 lines) with the checklist from the slides: MD5/SHA-1 used for security, `MODE_ECB`, a key written as a literal, `random` used for something secret. Fill in one row per mistake:

| Line | What the code does | The mistake | CWE | Flagged by a tool in Task 1? |
|---|---|---|---|---|
| | | | | |

Then, in the `ecb:` line from Task 0, mark the two identical 16-byte blocks (32 hex characters each): that repetition is what ECB leaks. (*Why* ECB behaves like this is the Cryptography course's cipher-modes lab — here you only need to recognise `MODE_ECB` in code.) For each mistake no tool flagged, write one line on why a pattern-matching tool cannot be sure it is a bug. *Deliverable:* the four-row table + the marked `ecb:` line + the one-liners.

> **Cracking `hashes.txt`?** Not this week — that attack is the Cryptography course's hash lab. The
> file stays in this folder as optional practice for the midterm practical (no marks here).

**Task 3 — Predictable token (10 min, in class)** · *Goal:* show the reset token is guessable. *Steps:* from `labs/week03-cryptography`, print several `reset_token()` values with this one Docker command:

```bash
docker run --rm --network none -v "$PWD":/work -w /work kosen-swsec-week03:local \
    python -c 'import vulnerable_crypto as v; [print(v.reset_token()) for _ in range(5)]'
```

Argue why a 6-digit `random` token (10^6 space, non-CSPRNG) is brute-forceable (CWE-330). *Deliverable:* sample tokens + a one-line attack estimate.

**Task 4 — Get the key out of the code (10 min, in class)** · *Goal:* fix the key-management mistake properly. *Steps:* find the key literal in `vulnerable_crypto.py`; explain why shipping a key in source is CWE-798 (its cryptographic-key case is CWE-321), and say where the key should come from instead. Then explain why removing the line in a new commit does **not** end the leak (think of what Gitleaks scanned in Week 2). *Deliverable:* the line + a 2-sentence mitigation + one line on git history.

**Task 5 — Rehash-on-login (30 min, in class, guided)** · *Goal:* upgrade old MD5 passwords to argon2id the way real apps do. *Steps:* run `migrate.py`, fill in the one-line `TODO` in `migrate.py`'s `login()`, and run it again until it prints `ALL PASS`:

```bash
docker run --rm --network none -v "$PWD":/work -w /work kosen-swsec-week03:local python migrate.py
```

*Deliverable:* the line you wrote + a screenshot of `ALL PASS` + 2 sentences: why the upgrade can only happen at login, and why the MD5 check uses `hmac.compare_digest`.

**Task 6 — Defend / fix it (20 min, in class, guided)** · *Goal:* check the fixed version, with the key coming from the environment. *Steps:* run `solution_skeleton.py` with a fresh key in `ENC_KEY_HEX`:

```bash
export ENC_KEY_HEX=$(openssl rand -hex 32)
docker run --rm --network none -e ENC_KEY_HEX -v "$PWD":/work -w /work \
    kosen-swsec-week03:local python solution_skeleton.py
```

Confirm `store_password`/`verify_password` use argon2id (auto-salted), `encrypt_gcm` uses a random 12-byte nonce + auth tag with the key from `ENC_KEY_HEX`, and `reset_token` uses `secrets`. Map each fix to the CWE it closes. *Deliverable:* before/after table (mistake → fix → CWE closed) + screenshot of the fixed script running.

**Task 7 — Your project: NoteVault (homework, optional extension; no extra graded points)** · *Goal:* find the same mistakes in your term project. *Steps:* scan the NoteVault starter app from inside its own folder (a scan started at the repo root finds nothing there, because the root `.semgrepignore` excludes it):

```bash
cd project/starter-app
docker run --rm -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config p/python --metrics=off .
```

List the crypto-related findings (file:line + rule), say which of this week's four mistakes NoteVault repeats, and describe in 2–3 sentences how rehash-on-login would move NoteVault's users off MD5. *Deliverable:* the list + the sketch — record it as a finding for your project report (`project/REPORT-TEMPLATE.md` in the repo root).

**Supplied reference versus student code:** `solution_skeleton.py` is a complete reference despite its legacy filename. Your required authored change is the rehash-on-login TODO in `migrate.py`. Add a wrong-password/no-migration case and a subsequent successful login to your evidence; do not claim that merely running the reference implements the migration. This week is software misuse review, not a repeat of the cryptography course's cracking/mode-attack lab.

## Part 4 — Reflection
1. Map each of the four mistakes to its CWE and to OWASP A04, in one line each.
2. Name a real-world breach caused by weak password hashing or hardcoded keys, and which fix here would have prevented it.
3. Which of the four mistakes did no tool flag, and what would you add to code review or CI so it is caught next time?

## Grading rubric (100)
| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common practical: main task and observations | 20 | 20 |
| Common practical: student defense/control or design, tests and limitations | 20 | 20 |
| Common practical: reproducible evidence and reasoning | 20 | 20 |
| Assigned Conventional Part 2 written questions | 20 | — |
| Assigned Conventional Part 4 reflection | 20 | — |
| Assigned Audit-the-AI | — | 20 |
| Assigned Explain-in-Plain-English | — | 10 |
| Assigned Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

The optional project/upload extension adds no extra graded points to the common 60 or assigned 40.

**Due:** 23:59 (Thai time) the night before next week's class (exact time on learn.zcr.ai/submit). **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Personalized flag (if this lab issues one):** ____________________
  *Flags are unique per student — submitting another student's flag is a violation. This blank is your personal record only; the flag itself is scored by submitting it in the **`ctf.zcr.ai`** challenge — the worksheet PDF is a separate submission, to **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).*
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Audit a complete AI answer about this week's design, exploit or fix. Use the instructor-provided exhibit if one is assigned, or obtain an answer and paste it in full. A correct answer is allowed: verify its claims and state the remaining assumptions rather than inventing an error.
2. **Check what is correct, wrong, risky or conditional** — insecure code, an incomplete fix, a hallucinated API/function/CVE, an edge case or unsupported reasoning. Quote the exact line(s) and support the evaluation with evidence.
3. Supply a verified correction where needed; if the answer is correct, supply the verification and limits. Explain your conclusion in 2–3 sentences. Do not manufacture a defect to satisfy the task.

> Disclose your AI use in the Part 1 table. This is the assigned AIR-Sec Audit component (20 points); it is not added to the common 60 or to the Conventional 40.

---

## 🧠 Comprehension & Prompt — assigned AIR-Sec section (10 + 10)

**A. Explain in Plain English (EiPE).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem.** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it: does the exploit now fail? If not, refine the prompt and try again. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
