# Course Specification — Software Security 2 (02005094)

| Field | Confirmed value |
|---|---|
| Level / credits | Year 4 / 1.5 credits |
| Term / category | Semester 2 AY2026 / Computer / Compulsory |
| Instructors | Nutthakorn Chalaemwongwan; Shinya Oyama |
| Format / contact | Lecture with supervised practical work; 20 weekly slots of 150 minutes |
| Programme alignment | C(2), C(4), G(5); MCC follows the actual weekly topics in the institutional XLSX |

Section, room and calendar dates follow the official timetable; no unconfirmed values are invented. The original XLSX layout and full cell text are preserved.

## Outcomes and alignment

| CLO | Assessed capability | Principal evidence |
|---|---|---|
| 1 | Model assets, boundaries and attacker goals; derive testable requirements | W1 model, project threat model, written scenarios |
| 2 | Demonstrate and explain controlled vulnerability mechanisms | Practical observations, exam stations, findings |
| 3 | Implement bounded root-cause corrections and verify both rejection and legitimate behavior | Student patch/configuration, controls, project tests |
| 4 | Operate/triage tools and verify component/artifact/CI controls with stated limits | W2/W3/W11–15 evidence, project secure-release record |
| 5 | Evaluate technical/AI claims and communicate justified reasoning | Assigned Conventional/AIR-Sec work, report and explanation |
| 6 | Work ethically and provide original, reproducible evidence and accountable contribution | Authorized scope, tool/source disclosure and contribution record |

| Assessment | Course points | Mode / outcomes |
|---|---:|---|
| Twelve worksheets, W1–6 and W10–15 | 30 | Individual; CLO1–6; 2.5 points each |
| Midterm written / practical | 8 / 12 | Individual; CLO1–4,6 |
| Final written / practical | 10 / 15 | Individual / teams 2–3; CLO1–6 |
| Secure Build project | 15 | Teams 2–3; CLO1,3–6 |
| Quiz / participation | 10 | Individual; lowest one weekly quiz dropped |
| **Total** | **100** | |

All worksheets have common practical60: task/observations20 + correction/control/limitations20 + reproducible evidence/reasoning20. Add one assigned format40: Conventional written40, or AIR Audit20 + EiPE10 + Prompt10. Raw 100 converts by `score/100×2.5`. The other format is reference practice. Week 1 uses modeling evidence, not forced exploitation or flags. Week 3 retains application-misuse/scanner/rehash scope. Week 16's complete team worksheet is formative project work, not a thirteenth academic worksheet.

Viva/reproduction checks verify submitted work within existing criteria, without extra marks or automatic-zero gates. External Agent Breaker is optional; its former8raw points are reassigned within required practice. Games, first-blood and CTFd dynamic scores are engagement-only. Do not use a team ranking as an individual's participation grade.

## Timetable and workload

Ordinary slots: quiz/review10 + brief15 + practical100 + debrief20 + capture5 =150. Review slots: cumulativequiz30 + selectedclues20 + boundedmock70 + correction25 + save5. Week 16: brief10 + build/peer100 + clarification30 + notes10. Week 20: returnedwork20 + corrections40 + projectclarification45 + reflection35 + close10.

Written sittings reserve130task +20administration; practicals130task +20brief/submission. Week 19 has four bounded stations, raw 100, and no project Q&A. Videos≤5 minutes, report and code are due before W19; clarification usesW16/W20. See [AGENDA](../AGENDA.md) and [lesson plans](lesson-plans/).

| Ability | Midterm | Final | Quiz/participation | Worksheets | Project | Total |
|---|---:|---:|---:|---:|---:|---:|
| Basic |10|5|5|0|0|20|
| Technical |10|20|5|25|10|70|
| Interdisciplinary |0|0|0|5|5|10|
| **Total** |20|25|10|30|15|100|

Midterm written and practical each use rawBasic50/Technical 50 (course 4/4 and6/6). Final written uses50/50 (course 5/5), final practical isTechnical15. These refer to the same marks, not extra scores. Project-adjusted raw marks are capped100 before the15%conversion.

## Criteria, preparation and review

The six institutional rubric dimensions remain threat/risk modeling; vulnerability analysis/evidence; remediation/verification; tooling/secure delivery; evaluation/communication; and ethics/integrity/contribution. VeryGood means correct, complete and evidenced; Good means essential reasoning is correct with gaps; Fail means the central work is incorrect or insufficiently evidenced. Apply these through the published point criteria, preserving partial credit for demonstrated work.

Preflight architecture/toolchains, images, accounts and prepared CI/signature fixtures before timed work. Static IAM/container review and deterministic AI mocks have explicit limits; they do not prove live cloud enforcement or arbitrary LLM robustness. References/planted defects remain available; student tasks identify the bounded change. The time budgets are plans, not measured student completion guarantees. Record actual time and attainment after teaching.

Current private KOSEN instruments are under `instructor/exams/kosen-02005094/`; historical/shared and MFU session instruments retain their own scope. This prospective teaching update does not recalculate student grades or claim an updated external research registration. Existing submission deadlines/late rules remain in the [syllabus](../syllabus.md); authorized scope is in [ETHICS](../ETHICS.md).
