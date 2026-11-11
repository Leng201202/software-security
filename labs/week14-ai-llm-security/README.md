# Week 14 — Security of AI / LLM-Powered Applications

## 150-minute class and assigned worksheet version

**Class:** quiz/review 10 + explanation/demo 15 + supervised practice 100 + debrief 20 + evidence capture 5 minutes. Prepare tools, images and access before class. The full reference tasks remain below; their standalone estimates are not an instruction to finish the entire bank during the class.

**Assessment:** all students complete the shared practical **60/100** plus **one assigned version's 40/100**. Conventional uses the ordinary Part 2 questions (20) and Part 4 reflection (20). AIR-Sec uses Audit-the-AI (20), Explain-in-Plain-English (10) and Prompt Problem (10). The unassigned written version is reference practice, not an extra requirement. Each teaching worksheet contributes **2.5 course points**, making 12 individual worksheets worth 30 in total.

Both versions submit their own commands/results and explanation, and complete the student patch and control tests where assigned. Personal flags are used only for an actually issued instance; a local demo flag alone does not demonstrate understanding. Viva/reproduction checks verify the existing work within its rubric: no additional points or automatic-zero gate.

**Shared practical core:** Disclosure case 20; unsafe-output case 20; student output-control edit 30; legitimate/attack controls 20; limitations 10.

Complete `render_model_output()` in `student_task.py` and run `python3 check_student.py`: redact the assigned secret and HTML-escape the output before it reaches the text sink. Preserve the existing vulnerable and guarded bots. They are deterministic mocks: these results do not establish protection for real model reasoning, RAG retrieval or tool execution. Agent Breaker and the indirect-injection thought exercise remain optional extension practice. External game scores earn **0 required worksheet points**; the previous game allocation is absorbed into the shared practical rubric.

**OWASP Top 10 for LLM Applications (2025):** LLM01 Prompt Injection · LLM02 Sensitive Info Disclosure · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM08 Vector/Embedding Weaknesses · LLM10 Unbounded Consumption

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); run `docker compose build` in this lab folder while online, then skim last week's recap.
2. **Slides, then class** — read `slides/week14.md` and read the worksheet's **Part 2** as preparation; complete only the assigned written version; class opens with the weekly quiz (~10 min) and a short explanation + demo (15 min).
3. **Lab (in class)** — follow the shared practical core and complete **Worksheet 14** (`worksheet.md`, shared practical plus the assigned Conventional or AIR-Sec written section). Kickoff: `docker compose up --no-build --pull never` → `:8082` (insecure) / `:8083` (guarded). Follow the 100-minute core run sheet in Part 3; the full original task bank is retained for preparation and extension.
4. **Submit before the next class** (shared core plus assigned written version) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Explain the LLM Top 10 and where AI features add attack surface.
- Demonstrate direct-injection behavior in the deterministic mock; explain indirect-injection risks as a design case.
- Add guardrails: input/output validation, least-privilege tools, output handling.

## 🧙 Optional external game — "Gandalf Challenge"
External extension reference: Lakera Agent Breaker (https://play.lakera.ai/agent-breaker). Check its current access/rules before use. It is not required for the worksheet; external game points are engagement only.
1. **Direct prompt injection:** override the system prompt to reveal a hidden secret (required: local bots in Tasks 1–2; external levels are optional).
2. **Indirect injection (optional design case):** explain a malicious instruction in a retrieved document; the local mock has no RAG pipeline to trigger.
3. **Improper output handling:** show model output flowing unsanitized into a downstream action (XSS/command).
4. **Agentic-AI / MCP risks (current, post-Oct 2025, written-only):** this lab has no agent to attack — describe how **tool poisoning** and **excessive agency** would work in an agent with tools (e.g. an MCP server), where a malicious instruction makes the agent call a tool it shouldn't.
5. **Fix (round 2):** input/output guardrails, strict output schemas/validation, **least-privilege tool access**, human-in-the-loop for sensitive tools, and rate/consumption limits; re-test.

## Deliverable
Required core: local mock disclosure/output observations, the student output-control diff, legitimate/attack test results and an explanation of the mock's limits. The agent/MCP design and external game are reference/extension material; the assigned written section remains within its 40 points.

## References
- https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- https://play.lakera.ai/agent-breaker — Lakera Agent Breaker (optional external reference; verify current access/rules)
- MITRE ATLAS (AI/agentic attack techniques) — https://atlas.mitre.org/
