# Week 17 — Two bounded mock checkpoints

**02005094 · formative · 70 minutes within the 150-minute review session.** Use the already taught Week 10 and Week 14 local tasks. This is practice, with no new worksheet or exam mark. Start each checkpoint with its failing starter check, make your own edit, and keep the legitimate and attack controls. Work only in the supplied lab or a personal copy.

## Checkpoint 1 — API object and field boundary, 35 minutes

**File:** [Week 10 student task](../week10-api-security/student_task.py). Complete `may_read_orders()` and `bind_creation_fields()`. Run the [provided checks](../week10-api-security/check_student.py) from `labs/week10-api-security`:

```sh
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local \
  python3 check_student.py
```

Record owner and server-trusted admin success, cross-user denial, and rejection/ignoring of `is_admin` in account creation. Explain why the teaching `X-User-Id` header is a supplied identity fixture, not a production authentication method. The checker uses an in-process client without opening a port.

## Checkpoint 2 — Untrusted output boundary, 35 minutes

**File:** [Week 14 student task](../week14-ai-llm-security/student_task.py). Complete `render_model_output()`: redact the exact assigned secret, then HTML-escape for a text sink. Run the [provided checks](../week14-ai-llm-security/check_student.py) from `labs/week14-ai-llm-security`:

```sh
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/lab:ro" -w /lab kosen-swsec-week14:local \
  python3 check_student.py
```

Record ordinary text remaining readable, script markup rendered inert, and secret text absent. Explain why this deterministic local mock cannot establish safety of a remote model or tool authorization.

## Debrief, in the session's 120–145 minute block

Read the [Week 11 Rust counter](../week11-memory-safety-exploitation/student_safe.rs) and state how byte length differs from Unicode scalar count and how malformed UTF-8 should fail. Use the [Week 12 signature fixture](../week12-supply-chain/signature-core/manifest.json) to explain why a valid signature under an untrusted key must fail. Use the [Week 15 bounded checker](../week15-devsecops-pipeline/check_student.py) to explain why a lookup exception denies and logs an error type without token text. These are explanation prompts, not extra 35-minute code tasks.

For each checkpoint keep: your diff, exact command and observed result, root cause/trust boundary, legitimate and negative controls, and one limit. The final practical uses its own sitting pack. [Review schedule](README.md) · [Practical blueprint](../week19-final-ctf-capstone/ctf.md). The historical optional bank is archived in the course source.
