# Worksheet 1 — Security Mindset & Threat Modeling (3 hrs)

> **Course:** Software Security (KOSEN69) · **Week 1**
> **Aligned to:** OWASP 2025 A06 Insecure Design · CWE-501 (Trust Boundary Violation)
> **Signature game:** "Elevation of Privilege" (Microsoft STRIDE card deck)

> **Ethics note:** This week is *modeling only* — you analyze design, you do **not** attack the app. Run the sample app only on your own VM/localhost. Never apply these techniques to systems you do not own or lack written permission to test.

## Part 1 — Student Information
| Name | Student ID | Date | Group |
|---|---|---|---|
| Sai Shang Hlang|6631503129 | 15 Aug 2026| - |

## Part 2 — Lecture Questions
Answer in your own words (2–4 sentences each).
1. Define the CIA triad and give one concrete failure example for each of the three properties.
    - The CIA triad stands for Confidentiality, Integrity, and Availability.
**Confidentiality** fails when private user data is exposed, **Integrity** fails when someone changes data without permission, and **Availability** fails when a system goes down and users cannot access it.**

2. What is a *trust boundary*, and why does data crossing one deserve extra scrutiny?
    - Trust boundary is a point where data moves between parts of a system from like website to it server.We must check the data because it could be unsafe or harmful to system.
3. Explain "attack surface." Name two things that increase it in a web app.
    - All places where someones can try to attack a system.
      - More pages,APIs or routes that user can access.
      - More user input or file upload can contain harmful data,or attack script.
4. What does each STRIDE letter map to, and which security property does each threat violate?
    - S - Spoofing: Pretending to be another user for breaking authentication
    - T - Tampering: Changing data without permission which break Integrity
    - R - Repudiation: Denying an action,logs can help prove what happened which break    Accoountability
    - I - Information disclosure: Private infomation is seen by someone who should not.Breaks     Confidentiality
    - D – Denial of Service: Making a website or system too busy so normal users cannot use it.Break Availability
    - E – Elevation of Privilege: A normal user gets higher permissions, such as getting admin access. → breaks Authorization
5. What does "Secure by Design" (CISA) mean, and how does it differ from bolting security on after release?
    - Secure by Design means security is planned and built into the system from the beginning. Developers think about security during design, coding, and testing. 

## Part 3 — Hands-on Lab (180 min)
**Learning goals:** build a data-flow diagram (DFD), apply STRIDE to a real Flask app, rank risks, and propose mitigations.
**Prerequisites:** Docker + Docker Compose in your VM; a drawing tool (draw.io / paper + photo); the Elevation of Privilege deck (print or virtual) — free print-and-play PDF at [github.com/adamshostack/eop](https://github.com/adamshostack/eop).

**Environment setup**
```bash
cd labs/week01-threat-modeling
docker compose up --build           # starts sample-app on http://localhost:8080
curl -s -X POST localhost:8080/notes -H 'Content-Type: application/json' \
     -d '{"owner":"alice","body":"hello"}'   # observe behavior, do not attack
curl -s localhost:8080/notes

echo "demo file" > demo.txt
curl -s -X POST localhost:8080/upload -F "file=@demo.txt"   # observe behavior, do not attack
curl -s localhost:8080/files/demo.txt
```

Source to model lives in `sample-app/app.py`. Template to fill: `THREAT-MODEL-TEMPLATE.md` (copy it, do not edit the original).

**What to submit per task:** the threat/element identified + a screenshot (DFD, table, or running app) + a 2–3 sentence mitigation.

**Task 0 — Onboarding (5 min)** · *Goal:* prove the environment works. *Steps:* `docker compose up`, hit `/notes` and `/files/<name>`, read `sample-app/app.py`. *Deliverable:* screenshot of the running app + the JSON response.
  - **Running Application**
![alt text](image-1.png)

  - **JSON Response**
![alt text](image.png)

**Task 1 — Draw the DFD (25 min)** · *Goal:* map the system. *Steps:* identify the external entity (web client), the process (Flask app), the data store (`notes.db` SQLite), the `uploads/` store, and the flows for `/notes`, `/upload`, `/files/<name>`; mark the Internet→app trust boundary with a dashed line. *Deliverable:* DFD image embedded in your copy of the template.

![alt text](image-2.png)

**Task 2 — STRIDE the elements (30 min)** · *Goal:* enumerate threats per element. *Steps:* for each element fill the S/T/R/I/D/E grid. Ground it in real code: `/notes` accepts a client-supplied `owner` with no auth (Spoofing); `/upload` saves raw `f.filename` — arbitrary-file-write (Tampering) — and echoes the resolved save path back in its response (Information disclosure); `/files/<name>` reads it back but is comparatively defended (see Task 5); no logging anywhere (Repudiation). *Deliverable:* completed STRIDE table.

| Element | S - Spoofing | T - Tampering | R - Repudiation | I - Information Disclosure | D - DoS | E - Elevation of Privilege |
|---|---|---|---|---|---|---|
| `/notes` | User can fake the `owner` because there is no authentication | Note data could be changed without permission | No logs to show who created or changed notes | Notes may be seen by unauthorized users | Too many requests could make the app slow | Weak access control may give users more access |
| `/upload` | User identity is not checked | Raw filename can be used to write files in unsafe locations | No logs to show who uploaded files | Server file path is shown in the response | Large or many uploads could fill storage | Unsafe file upload may lead to higher access |
| `/files/<name>` | User identity is not checked | Lower risk because the route has some protection | No logs to show who accessed files | Files may be seen without permission | Too many file requests could slow the server | Lower risk because this route has some protection |

**Task 3 — Elevation of Privilege game (20 min)** · *Goal:* find threats you missed. *Steps:* play the EoP deck against your DFD; each card you can tie to a real element/flow scores a point; record every valid threat. No printer or scissors? Draw from the digital deck below instead — same 78 cards, same rule. *Deliverable:* list of carded threats + score.

```sim
eop-deck
```

## Task 3 — Elevation of Privilege Game

| Card / Threat | Related Element | Why it applies |
|---|---|---|
| User pretends to be another user | `/notes` | The client can send any `owner` name because there is no authentication. |
| User changes a file path | `/upload` | The app uses the uploaded filename directly. |
| Sensitive server information is exposed | `/upload` | The response shows the server save path. |
| User actions cannot be proven | All routes | The app has no logging. |
| Too many uploads use server resources | `/upload` | Many or large uploads could fill storage. |

**Score: 5 points**

**Task 3b — Systems-level pass (25 min) 🔭** · *Goal:* find what the per-element grid cannot see. Tasks 2 and 3 enumerate threats **one element at a time**, and that is exactly where threat models are known to stop short — students taught STRIDE alone reliably identify component threats and *discount system-level ones* ([Joshi et al., ASEE 2024](https://arxiv.org/abs/2404.16632)). So do a second pass over the **whole** diagram:
![Three trust zones — public internet, application tier, data tier — with the two boundaries a request crosses between them](img/trust-boundaries.svg)

- **Trust boundaries end-to-end.** Follow one request from the client to `notes.db` and back. List every boundary it crosses. Which crossing has no check on it?
- **Assume one element is fully owned.** Pick the Flask process, then the `uploads/` store. For each: what does the attacker now *reach* — not what is it, but where does it get them?
- **Chain two "low" findings.** Find two threats you or the EoP deck rated minor that combine into something you would not accept. Write the chain as `A → B → consequence`.
- **One-line system claim.** Finish: "Even if every element-level mitigation in Task 8 is implemented, this system still fails if ___."

Use the simulation below before you start — toggle a component to attacker-controlled and watch what it reaches:

```sim
trust-boundary
```
##### 1. Trust Boundaries
Web Client → Internet/App boundary → Flask App → App/Data boundary → notes.db → Flask App → Web Client.
The Internet → Flask App crossing has no authentication check.
##### 2. Owned Elements
**Flask App owned:**  
The attacker could reach `notes.db` and `uploads/`, allowing them to access or change stored data.
**uploads/ owned:**  
The attacker could change stored files or cause users to recei
##### 3.  Threat Chain
No authentication → fake owner → create notes as another user.

##### 4. System Claim
Even if every element-level mitigation is implemented, this system still fails if the Flask App itself is fully controlled by an attacker.

*Deliverable:* the boundary list, two owned-element reachability notes, one written chain, and the system claim.

**Task 4 — Abuse cases & attacker personas (20 min)** · *Goal:* think like specific adversaries. *Steps:* define 2 personas (e.g. a curious logged-in user; an anonymous internet attacker) and write 2 abuse cases each against the sample app, tied to DFD elements. 

##### Persona 1 — Normal User

A user who tries to access things they should not.
  1. **Pretend to be another user — `/notes`**  
   The user can use another person's name because there is no login check.
  2. **View another file — `/files/<name>`**  
   The user may try to view files that do not belong to them.

##### Persona 2 — Internet Attacker
A person from the internet who tries to harm the app.
   1. **Upload an unsafe file — `/upload`**  
   The attacker may upload a file with an unsafe filename.
   2. **Make the server slow — `/upload`**  
   The attacker may upload many large files and use too much server storage.

*Deliverable:* 4 abuse cases.

**Task 5 — Path-traversal deep-dive (25 min)** · *Goal:* analyze the riskiest flow. *Steps:* trace `/upload` → `/files/<name>`; explain how `../` in a filename escapes `uploads/`; sketch the secure design (`secure_filename`, store outside web root, allow-list extensions). *Deliverable:* the data flow + secure-design note.

##### Data Flow

  User
    ↓
  /upload
    ↓
  Flask App
    ↓
  uploads/
    ↓
  /files/<name>
    ↓
  User


**Task 6 — Threat-model the project target (30 min)** · *Goal:* kick off your term project. *Steps:* stop the sample-app first (`docker compose down` — both apps bind host port 8080), then run **NoteVault** (`cd ../../project/starter-app && docker compose up`), draw a quick DFD, and list the top 3 STRIDE threats you'd investigate. *Deliverable:* NoteVault DFD + top-3 threats (reuse these in your project report — `project/REPORT-TEMPLATE.md` in the repo root).

##### NoteVault — Data-Flow Diagram

```
                          (dashed = trust boundary)
  ┌────────────┐            ┊                        ┌───────────────────┐
  │ Web Client │  HTTP       ┊                       │   Flask App        │
  │ (browser / │───────────▶┊  /register             │ (notevault app.py) │
  │  curl)     │            ┊  /login                │                    │
  │            │◀───────────┊  /logout               │  current_user()    │
  └────────────┘  session    ┊  /notes  (POST)       │  role_of()         │
       ▲            cookie   ┊  /api/notes/<id>      │  seed()            │
       │           (JWT)     ┊  /search              │                    │
       └───────────┈┈┈┈┈┈┈┈┈┈┊  /admin               │                    │
                              ┊  /export             │                    │
                              ┊                      └─────────┬──────────┘
                              ┊  Internet ⇄ App                │  SQL (string-
                              ┊  trust boundary                │  formatted, no
                              ┊                                │  parameterization
                              ┊                                ▼  on /login,/search)
                              ┊                     ┌────────────────────┐
                              ┊                     │  notevault.db      │
                              ┊                     │  (SQLite, /tmp)    │
                              ┊                     │  ── users (id,     │
                              ┊                     │     username,      │
                              ┊                     │     password[md5], │
                              ┊                     │     role)          │
                              ┊                     │  ── notes (id,     │
                              ┊                     │     owner, title,  │
                              ┊                     │     body)          │
                              ┊                     └────────────────────┘
                              ┊
                              ┊                     ┌────────────────────┐
                              ┊  /export ───────────▶  OS shell          │
                              ┊  (fmt param via     │  subprocess.run(   │
                              ┊   shell=True)       │  ..., shell=True)  │
                              ┊                     └────────────────────┘
                              ┊  App ⇄ OS trust boundary (process spawns a shell)
```

**Elements:** external entity = Web Client; process = Flask App; data store = `notevault.db`; second data/command store reached via `/export` = the container's OS shell. Two trust boundaries: Internet → Flask App (every route above the dashed line), and Flask App → OS shell (crossed only by `/export`).

##### Top 3 STRIDE Threats to Investigate

| # | Threat (STRIDE) | Element / Flow | Why it's top-3 |
|---|---|---|---|
| 1 | **Tampering → command injection (RCE)** | `/export` | `fmt` comes straight from the query string into `subprocess.run("echo exporting notes as " + fmt, shell=True, ...)`. No escaping, `shell=True`. This is the single highest-impact flow — it crosses the Flask App → OS trust boundary and can hand an attacker a shell in the container, not just app data. |
| 2 | **Spoofing → authentication bypass** | `/login` | Two independent bypasses on the same flow: (a) the SQL query is built with `%s` string formatting (`"...WHERE username = '%s' AND password = '%s'" % (...)`) — classic SQLi; (b) `current_user()` calls `jwt.decode(tok, SECRET, algorithms=["HS256", "none"])`, so a token signed with `alg: none` is accepted — either bug lets an attacker become **any** user, including `admin`, without a valid password. |
| 3 | **Elevation of Privilege → client-controlled role** | `/register` | `role = request.form.get("role") or (request.json or {}).get("role") or "user"` is inserted into `users.role` with no server-side check. Anyone can `POST /register` with `role=admin` and walk into `/admin`, which then leaks every user's MD5 password hash. |

*(Honorable mention, cut for "top 3": `/api/notes/<nid>` has no ownership check — any logged-in user can read any note by guessing the integer ID (IDOR / Information Disclosure), including the admin's seeded note containing `prod db password is hunter2`.)*

**Task 7 — Security requirements (15 min)** · *Goal:* turn threats into testable requirements. *Steps:* write 3 security requirements as acceptance criteria ("the system must … so that …"), each mapped to a threat from Task 2 or Task 6. *Deliverable:* 3 testable security requirements.

1. **(Task 2 — `/notes` spoofing)** The system must check that a user is logged in before it lets them create a note, so that nobody can create a note under someone else's name.
2. **(Task 2/5 — `/upload` tampering)** The system must remove path characters like `../` from an uploaded filename before saving it, so that a file can never be written outside the `uploads/` folder.
3. **(Task 6 — `/register` elevation of privilege)** The system must ignore any `role` value sent by the client on registration and always set new accounts to `role=user`, so that a normal user cannot become admin just by adding a field to the request.

**Task 8 — Defend / fix it: rank & mitigate (25 min) 🛡️** · *Goal:* turn threats into action you can prove. *Steps:* rank the top 5 threats by likelihood × impact; propose one concrete mitigation each (e.g., auth on `/notes`, `secure_filename()` + allowlist for `/upload`, request logging for Repudiation, size/rate limits for DoS). Then **pick one and actually implement it** in your fork.

##### Top-5 Threats — Ranked by Likelihood × Impact

| Rank | Threat | Likelihood | Impact | Mitigation idea |
|---|---|---|---|---|
| 1 | `/upload` saves the raw filename — attacker can write files outside `uploads/` (path traversal) | High — just change the filename, no skill needed | High — can write a file anywhere the app process can reach | Sanitize filename with `secure_filename()` + only allow a fixed list of extensions |
| 2 | `/notes` lets anyone set `owner` with no login check (spoofing) | High — no auth exists at all | Medium — fake/forged notes under any name | Require a logged-in session before a note can be created |
| 3 | No logging anywhere in the app (repudiation) | High — true for every route, all the time | Medium — nobody can prove who did what, makes every other threat harder to catch | Log every request with timestamp, IP, and route |
| 4 | `/upload` response echoes the full server save path (information disclosure) | High — happens on every upload | Low–Medium — leaks internal folder layout, helps plan further attacks | Return only the filename in the response, not the full path |
| 5 | `/upload` has no size/count limit (DoS) | Medium — needs repeated requests | Medium — can fill the disk and stop the app from working | Add a max file size and a per-IP upload rate limit |

**Implemented: #1, the `/upload` path-traversal fix.**

1. **Diff** (commit `84c55d1` on branch `wk01`):
```diff
--- a/labs/week01-threat-modeling/sample-app/app.py
+++ b/labs/week01-threat-modeling/sample-app/app.py
@@
 from flask import Flask, request, jsonify, send_from_directory
+from werkzeug.utils import secure_filename
 import sqlite3, os
 
 app = Flask(__name__)
 DB = "notes.db"
 UPLOAD_DIR = "uploads"
+ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg", "pdf"}
 os.makedirs(UPLOAD_DIR, exist_ok=True)
 
+def allowed_file(filename):
+    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
+
 def init_db():
     ...
 @app.route("/upload", methods=["POST"])
 def upload():
     f = request.files["file"]
-    f.save(os.path.join(UPLOAD_DIR, f.filename))
-    return {"saved": f.filename}
+    filename = secure_filename(f.filename)
+    if not filename or not allowed_file(filename):
+        return {"error": "invalid filename"}, 400
+    f.save(os.path.join(UPLOAD_DIR, filename))
+    return {"saved": filename}
```

2. **Evidence it works** — same payload, before and after:
```
# BEFORE the fix
$ curl -s -X POST localhost:8080/upload -F "file=@evidence.txt;filename=../../evil_before.txt"
{"saved":"../../evil_before.txt"}
$ docker compose exec sample-app sh -c "cat /evil_before.txt"
before-fix payload            # <- file escaped uploads/, landed at container ROOT

# AFTER the fix
$ curl -s -X POST localhost:8080/upload -F "file=@evidence.txt;filename=../../evil_after.txt"
{"saved":"evil_after.txt"}
$ docker compose exec sample-app sh -c "ls / | grep evil"
                               # <- nothing at root, file stayed inside uploads/
```

3. **Class fix or instance fix?** This is a class fix for the path-traversal problem itself: `secure_filename()` strips out any `../`, `/`, or other path characters from whatever string it is given, so it blocks the whole category of "attacker changes the filename to escape the folder," not just the one exact payload I tested. What could still break it: the protection only exists at this one call site — if the app grows another route that saves a file using a client-supplied name and forgets to call `secure_filename()` there too, that new route would have the same bug again. So the *technique* is a class fix, but it still has to be applied by hand at every place a filename comes from the user.

> **Why this is weighted.** Fewer than half of working developers can spot a security hole in code, and being shown vulnerabilities does not by itself teach you to find or close them. Exploiting is the half that feels like progress; defending is the half that transfers to your job.

## Part 4 — Reflection
1. Map your top finding to a CWE and to OWASP A06 (Insecure Design); explain the mapping in one sentence.
2. Name one real-world breach caused by a design flaw (not a missing patch) and what design control would have prevented it.
3. Of your five mitigations, which gives the most risk reduction per unit of effort, and why?

## Grading rubric (100)
| Criterion | Points |
|---|---|
| Lecture questions (Part 2) | 20 |
| Exploitation + evidence (DFD + STRIDE table + EoP findings + screenshots) | 40 |
| Defense (top-5 ranking + mitigations) | 25 |
| Reflection (CWE/OWASP mapping + breach + best mitigation) | 15 |

**Assessed within the rows above** (they are not extra points — they are what those points are for):
- **Systems-level reasoning** (inside *Exploitation + evidence*, Task 3b): does the model reach past single elements to boundaries, reachability and chains? Scored with the STRIDE + systems-thinking rubrics of [Joshi et al. 2024](https://arxiv.org/abs/2404.16632).
- **Defensive proof** (inside *Defense*, Task 8): a claimed mitigation with no before/after evidence scores at most half. A mitigation you can show closing a *class* scores full.
- **Adversarial thinking** (across the whole sheet): do the abuse cases, personas and chains show you reasoning as an attacker with goals and constraints — or just listing categories? This is the course's central disposition and it is assessed, not assumed.

---

## Evidence & Integrity (required)

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Personalized flag (if this lab issues one):** ____________________
  *Flags are unique per student — submitting another student's flag is a violation. How to submit: **learn.zcr.ai/submit** (full guide: `SUBMISSION.md` in the repo root).*
- **Explain in your own words** *(graded on your reasoning, not copied text):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI (required)

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Ask an AI assistant to exploit **or** fix this week's vulnerability. Paste its full answer.
2. **Find what's wrong or risky** in it — insecure code, a subtly incomplete fix, a hallucinated API/function/CVE, a missed edge case, or wrong reasoning. Quote the exact line(s).
3. Produce the **correct, verified** version yourself and explain in 2–3 sentences why the AI's output was insufficient.

> Disclose your AI use in the Part 1 table. This task counts toward your **Defense + Reflection** score.

---

## 🧠 Comprehension & Prompt (required)

**A. Explain in Plain English (EiPE).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem.** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it: does the exploit now fail? If not, refine the prompt and try again. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
