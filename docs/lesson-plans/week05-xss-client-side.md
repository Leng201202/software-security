# Lesson Plan — Week 5: XSS and browser request controls

| Item | Plan |
|---|---|
| Course | Software Security 2 (02005094, KOSEN-KMITL) |
| Contact time | **150 min:** quiz/review 10 + mechanism demo 15 + practical 100 + debrief 20 + evidence exit 5 |
| Core | `labs/week05-xss-client-side/worksheet.md` Tasks 0–4 |
| Slides | `slides/week05.md`; native deck `slides/pptx/week05.pptx` |
| Standards | OWASP 2025 **A05 Injection / CWE-79** (XSS); **A01 Broken Access Control / CWE-352** (CSRF) |
| Assessment | Common practical 60 + one assigned Conventional/AIR-Sec format 40 |

## Learning outcomes and CLOs

- **CLO2:** Reproduce reflected and stored XSS and a cookie-bearing same-site forgery on the authorized local target; explain the HTML sink and origin/site boundary.
- **CLO3:** Implement the student patch, then demonstrate legitimate behavior and rejected XSS/CSRF controls.
- **CLO5:** Audit AI advice with an independently checked edge case, explain the mechanisms in plain English, and verify the prompt result.
- **CLO6:** Keep tests within the sandbox, disclose AI/tool use, and submit original reproducible evidence.

## Before class

Build the pinned image on each machine while network is available: `docker compose build`. Test `docker compose up --no-build --pull never` offline. Host the supplied `csrf.html` on `localhost:8081`; the target is `localhost:8080`. Check both ports are free. Students prepare the worksheet's concept questions from the slides. The live Week 5 quiz has **three** questions on encoding, CSP and SameSite and a 10-minute limit; do not promise five questions.

## Teaching sequence

| Clock | Activity | Instructor check |
|---|---|---|
| 0:00–0:10 | Quiz and Week 4 bridge | Data becoming code in SQL versus HTML |
| 0:10–0:25 | Show raw `/hello` response, browser execution, then encoding; explain origin versus site | Ask which boundary changes when only the port changes |
| 0:25–0:30 | Task 0 baseline | Session cookie, normal comment |
| 0:30–0:45 | Task 1 reflected XSS | Exact payload, sink, visible effect |
| 0:45–1:00 | Task 2 stored XSS | Persisted payload, sandbox cookie only |
| 1:00–1:20 | Task 3 forged form from port 8081 | Cookie header; 200 with session, 401 in fresh profile |
| 1:20–2:05 | Task 4 student patch | Normal text/comment, XSS text, forged 403, no-session 401 |
| 2:05–2:25 | Debrief and viva | Encoding versus CSP; origin versus site; token validation |
| 2:25–2:30 | Save evidence and exit | Code link, screenshot and assigned-format reminder |

The 100-minute task budgets are **planned**, not representative student timing data. Record actual start/finish times while teaching.

## Mechanism and limits

The vulnerable comment POST checks the sandbox session cookie but no CSRF token. Port 8081 and port 8080 are different origins but the same site; a same-site form POST can carry the cookie even if it is `SameSite=Strict`. A cross-site `file://` PoC is unreliable in modern Chromium because an unspecified SameSite cookie defaults to Lax. The reference app adds output encoding, CSP, `HttpOnly` and a server-generated token checked on POST. The fixed app uses a static sandbox session and loopback HTTP for teaching; it is not production authentication. A production session should be random per user and sent over HTTPS with `Secure`.

The core requires a **student-written patch** and normal/attack controls. Showing only the supplied reference app does not meet the 25-point patch criterion. The optional DOM XSS, XSS Golf and cookie-beacon exercises add no required points.

## Assessment and release checks

Common 60 = reflected/stored XSS 20 + CSRF/session controls 15 + student patch 25. Assigned 40 = Conventional 4×10 or AIR-Sec Audit 20 + EiPE 10 + Prompt 10. Odd final ID digit takes Conventional; even, including zero, takes AIR-Sec. The live assignment deadline and late policy are authoritative. Source quiz and hosted quiz must be checked separately before teaching.

## Contingencies

- If the image is missing, build while online before class; no runtime `pip install` is part of the lab.
- If port 8080/8081 is occupied, use a free pair and update the URL in `csrf.html` and instructions consistently.
- If the forged request appears to work without a cookie, confirm the browser profile is really fresh and inspect the request Cookie header and response; do not infer CSRF from a comment alone.
- If CSP shows no violation, inspect the response header; output encoding already removed the script.
- If `student_checks.py` passes but browser evidence differs, inspect the actual `student_app.py` process, port and active browser profile.

## After class

Record actual student task durations, reproducible failures, and whether each student could explain the normal and attack controls. Use these observations to decide whether the 100-minute block is truly sufficient.
