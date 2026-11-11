# Lesson Plan — Week 4: Injection and interpreter boundaries

**Software Security 2 (02005094) · Year 4 · Semester 2 AY2026 · Lecture · 150 minutes.**
**Outcomes:** CLO2, CLO3, CLO5, CLO6. Current KOSEN approved policy, updated2026-11-10.

## Purpose and preparation

Reproduce bounded injection cases and complete the assigned student parameterization/validation function. Preserve vulnerable and comparison targets; the student tests both legitimate behavior and the original attack.

Before class: Prepare the supplied target, student_patch.py/student_app.py and student_checks.py; resolve ports and dependencies before class. Full concepts and longer questions remain available for preparation/follow-up. [Worksheet](../../labs/week04-injection/worksheet.md) and [README](../../labs/week04-injection/README.md) name the commands and bounded student task; [slides](../../slides/week04.md) support the explanation.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Quiz/review and goal; use the actual published quiz instrument. |
| 10–25 | Brief explanation/demo of the mechanism and the required observation/control. |
| 25–125 | Supervised practical core below; circulate and verify individual reasoning. |
| 125–145 | Compare results, explain limitations and correct one misunderstanding. |
| 145–150 | Save evidence and next actions. |

**100-minute core:** Baseline login (5), bounded login bypass (15), UNION observation (20), command-injection observation (20), student parameterization/input patch with controls (40).

## Evidence and assessment

Payload/root cause, the core UNION observation, student patch, legitimate/attack results and explanation. Upload remains an optional extension.

Each student completes common practical60 (task/observations20 + correction/control/limitations20 + reproducible evidence/reasoning20) plus one assigned format40: Conventional written40, or AIR-Sec Audit20 + EiPE10 + Prompt10. Raw 100×0.025 gives2.5course points. The other version and practical extensions are reference practice, not another requirement. A technically correct AI answer can earn full audit marks when its correctness is independently verified; no fabricated error is required.

Viva/reproduction checks verify the submitted work within its existing criterion, with no additional mark or automatic-zero gate. Use task-appropriate evidence and ordinary name/ID plus issued-instance requirements where actually applicable. The shared practical is common to both versions. This is one of12 individual graded worksheets; Week 16 is a separate formative project checkpoint.

## Instructor review

Run the required positive/negative controls before teaching and record actual tool versions/build assumptions and observed failures. A planning budget is not a measured student timing pilot. Record actual completion time and revise within the published course weights. Historical expanded plans are retained privately; existing other-course session/grade records are not rewritten by this KOSEN update.

See [agenda](../../AGENDA.md), [syllabus](../../syllabus.md) and [submission rules](../../SUBMISSION.md).

[Complete previous lesson details and commands, retained as reference](../reference/lesson-plans-before-20261110/week04-injection.md). Historical timings and required task counts are superseded for current KOSEN.
