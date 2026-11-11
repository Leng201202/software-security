# Week 7 — Two bounded mock checkpoints

**02005094 · formative · 70 minutes within the 150-minute review session.** Use the already taught Week 4 and Week 6 local tasks. This is practice, with no new worksheet or exam mark. Start each checkpoint with the untouched starter's failing check, make your own edit, and keep both the legitimate and attack control. Work only in the supplied lab or a personal copy.

## Checkpoint 1 — Injection control, 35 minutes

**File:** [Week 4 student patch](../week04-injection/student_patch.py). Complete `authenticate()` with bound SQL values and `ping_argv()` with one parsed IPv4 argument list. Run the [provided checks](../week04-injection/student_checks.py) from `labs/week04-injection`:

```sh
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/exam:ro" -w /exam week04-injection-injection-lab:latest \
  python3 student_checks.py
```

Record an ordinary login and IPv4 request that still work, plus a SQL payload and shell-metacharacter host that are denied. In one sentence, explain how parameter binding and `shell=False` keep data out of code. The checker mocks the ping subprocess; it does not contact a network target.

## Checkpoint 2 — Token and object boundary, 35 minutes

**File:** [Week 6 student patch](../week06-authn-authz/student_patch.py). Complete pinned JWT verification and the server-side order-owner decision. Run the [provided checks](../week06-authn-authz/student_checks.py) from `labs/week06-authn-authz`:

```sh
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/lab:ro" -w /lab kosen-swsec-week06:local \
  python3 student_checks.py
```

Record owner success, cross-user denial, and one unsigned/wrong-audience token denial. Explain why a valid identity alone does not authorize another person's order. The checker uses Flask's in-process client, without starting a listener.

## Debrief, in the session's 120–145 minute block

Use the [Week 3 migration starter](../week03-cryptography/migrate.py) to explain why a wrong password leaves a legacy record unchanged and why a correct login can trigger Argon2id rehashing. Review one scanner error versus a clean result from Week 2. These are explanation prompts, not extra 35-minute code tasks.

For each checkpoint keep: your diff, exact command and observed result, root cause/trust boundary, legitimate and negative controls, and one limit. The actual midterm practical uses its own sitting pack. [Review schedule](README.md) · [Practical blueprint](../week09-midterm-practical/ctf.md). The historical optional bank is archived in the course source.
