# Software Security 2 — Course Syllabus (02005094)

**Year 4 · 1.5 credits · Computer · Compulsory (C) · Semester 2 AY2026.**
**Class format: Lecture**, emphasizing supervised practical work in one 150-minute weekly slot over 20 weeks.
**Instructors:** Nutthakorn Chalaemwongwan and Shinya Oyama.
Updated 2026-11-10 to the owner-approved KOSEN teaching and assessment plan. The institutional XLSX retains its original format and full text.

## Course purpose and outcomes

Students model risks, investigate representative software weaknesses in an authorized sandbox, implement root-cause corrections and test both attack rejection and preserved legitimate behavior. The course covers application cryptographic misuse, web/API authorization and injection, memory safety, software supply chains, container/IAM configuration, AI application boundaries and fail-closed security delivery.

| CLO | On completion, the student can |
|---|---|
| CLO1 | Model assets, trust boundaries and attacker goals, prioritize plausible risks and derive testable security requirements. |
| CLO2 | Demonstrate and explain representative vulnerability mechanisms on the supplied authorized targets. |
| CLO3 | Implement a bounded root-cause correction and show attack rejection together with successful legitimate behavior. |
| CLO4 | Operate security tools, triage findings and limitations, and verify component, artifact and CI controls. |
| CLO5 | Evaluate technical claims, including AI-generated advice, and communicate justified results to technical and general audiences. |
| CLO6 | Work within ethical scope, disclose tools and sources, and provide original, reproducible evidence and accountable contributions. |

These outcomes include secure coding, correct application use of cryptography, supply-chain security, cloud/container/API configuration, AI application defense, DevSecOps and responsible disclosure. The approved programme alignment is C(2), C(4), G(5); MCC mappings follow the actual weekly topics in the institutional form.

## Class work and preparation

Ordinary teaching weeks use **quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence capture 5 = 150 minutes**. Installation, image pulls, account access and long reading happen before class. Full questions remain available; preparation and extension tasks are explicitly labelled. Students complete their assigned written section before the next class deadline.

Both worksheet formats perform the same core. Reference solutions support comparison, while the student implements the assigned bounded patch or configuration change and tests it. Week 1 is modeling and ethics: diagrams, STRIDE, system-wide reasoning and mitigation acceptance criteria are practical evidence; students do not attack the application. Week 3 focuses on scanner/manual misuse review and legacy-password rehash-on-login in application code; it does not repeat the separate Cryptography course's cracking and cipher-attack labs.

Use only the supplied sandbox. Preflight the Week 11 architecture/toolchain; a measured offset belongs to that build. Week 12 uses prepared artifact/signature verification inputs; real registry/OIDC signing needs preparation and is not a promised local-tag success. Week 13 distinguishes static configuration review from real cloud enforcement. Week 14's deterministic mock does not prove a real LLM/RAG system secure. Week 15 starts with a prepared repository and known CI baseline.

## Weekly schedule

| Week | Topic / practical purpose |
|---:|---|
| 1 | Security mindset, DFD/STRIDE and system-wide threat modeling; authorized-use boundaries |
| 2 | Secure SDLC; scanner/secret-finding triage, bounded correction and re-scan |
| 3 | Application cryptographic misuse; scanners/manual review and Argon2id rehash-on-login |
| 4 | Injection; student-written parameterization/validation and positive/negative tests |
| 5 | XSS, cookie/CSP and CSRF boundaries; student output-encoding correction and controls |
| 6 | Authentication and access control; ownership/token-verification correction and tests |
| 7 | Cumulative review and selected bounded mock checkpoints |
| 8 | Individual midterm written examination |
| 9 | Individual midterm practical examination |
| 10 | API BOLA/mass assignment; bounded authorization/schema patch and regression tests |
| 11 | Memory safety; fuzz/crash analysis, build-specific exploit/control and safe routine change |
| 12 | Supply chain; SCA, resolver/SBOM and expected-signer/integrity verification |
| 13 | Container/IAM; scan plus manual review, assigned configuration change and re-test |
| 14 | AI application mock; disclosure/output-XSS analysis, validation and controls |
| 15 | DevSecOps; fail-open/logging correction and prepared CI red/green verification |
| 16 | Project studio and formative checkpoint, peer review and project clarification |
| 17 | Cumulative review and selected final-format practice |
| 18 | Individual final written examination |
| 19 | Team final practical; project video/report/code submitted beforehand |
| 20 | Returned-work feedback, corrections, project clarification and reflection |

See [AGENDA.md](AGENDA.md) and the [lesson plans](docs/lesson-plans/) for topic-specific run sheets. All 20 slots are 150 minutes; the 12 teaching worksheets are Weeks 1–6 and 10–15.

## Assessment

| Component | Course points | Mode |
|---|---:|---|
| 12 teaching worksheets, 2.5 each | 30 | Individual |
| Midterm written W8 / practical W9 | 8 / 12 | Individual |
| Final written W18 / practical W19 | 10 / 15 | Individual / team |
| Secure Build project | 15 | Teams of 2–3 |
| Quiz / participation | 10 | Individual |
| **Total** | **100** | |

Each teaching worksheet is **raw 100 = common practical 60 + one assigned format's 40**:

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Core task and observations | 20 | 20 |
| Control/correction and limitations | 20 | 20 |
| Reproducible evidence and reasoning | 20 | 20 |
| Conventional Part2 written questions | 20 | — |
| Conventional Part4 reflection | 20 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Complete the common 60 and the assigned 40; the other form is reference practice. A worksheet contributes `raw score / 100 × 2.5` course points. Viva and reproduction checks verify the submitted work within its existing criteria, with no additional marks or automatic-zero rule. The common evidence is appropriate to the actual task, not a requirement to force a flag onto every activity.

Week 16 retains its complete studio worksheet as **formative project feedback**. It is not a thirteenth item in the 30-point worksheet category. Its work supports the existing project rubric. External Agent Breaker is optional enrichment; the former 8 raw worksheet marks are reassigned within the required practical criteria, not added to the course total. CTFd dynamic points, first-blood bonuses, Houses and game XP are engagement information, not academic marks.

Drop the **lowest one weekly quiz**. Participation assesses the student's own work and reasoning; a team's leaderboard position does not determine this mark. The published quiz instruments and maxima apply; no additional scoring category is introduced.

| Ability category | Midterm | Final | Quiz/participation | Worksheets | Project | Total |
|---|---:|---:|---:|---:|---:|---:|
| Basic | 10 | 5 | 5 | 0 | 0 | 20 |
| Technical | 10 | 20 | 5 | 25 | 10 | 70 |
| Interdisciplinary | 0 | 0 | 0 | 5 | 5 | 10 |
| **Total** | **20** | **25** | **10** | **30** | **15** | **100** |

Midterm written and practical each allocate raw Basic/Technical 50/50, giving course 4/4 and 6/6. Final written allocates raw 50/50, giving 5/5; final practical's 15 course points are Technical. These are classifications of the same marks, not extra grades.

## Examination and project arrangements

Every exam slot is **150 minutes**: written work/checking 130 + administration 20; practical work 130 + briefing/submission 20. The final practical has four bounded stations, raw 100, with evidence and correction/control tests. The full older challenge bank is retained for practice/reference, not an additional mandatory fourteen-challenge sitting. Current private KOSEN papers, keys and preflight instructions are under `instructor/exams/kosen-02005094/`.

Project teams remain 2–3. Submit a final report, code and a **video no longer than 5 minutes before Week 19**, following [project/README.md](project/README.md) and [REPORT-TEMPLATE.md](project/REPORT-TEMPLATE.md). Project clarification is in Weeks 16/20. Preserve the project rubric 20/25/25/15/10/5; apply documented contribution adjustment and cap the adjusted raw score at 100 before scaling to 15 course points.

## Submission, integrity and resources

The existing deadline is 23:59 ICT before the next class, with the exact date/time on the submission portal. The existing late-work rule remains 10% of the item's score per started 24 hours, reaching zero after 10 days; published individual extensions apply. In-class quizzes have no late window. See [SUBMISSION.md](SUBMISSION.md).

Provide original work, commands/results, tested corrections and explanations; disclose AI assistance and sources. Use only authorized targets and follow [ETHICS.md](ETHICS.md). Historical grades, consent records and other courses' assessment instruments are not recalculated by this teaching update.

References: [OWASP Top 10](https://owasp.org/Top10/2025/), [OWASP API Security](https://owasp.org/API-Security/), [OWASP LLM security](https://genai.owasp.org/), [MITRE CWE](https://cwe.mitre.org/), [SLSA](https://slsa.dev/), [Sigstore verification](https://docs.sigstore.dev/cosign/verifying/verify/), CISA Secure by Design, and the course [readings](readings.md). Use current documentation and observed output rather than memorized scanner counts or unsupported guarantees.
