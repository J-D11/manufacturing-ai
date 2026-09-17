# Practical user pilot

Status: planned, unrun. Recruiting, consent, machine operation, and physical acceptance have not occurred. The user sends invitations and selects participants; this kit does not authorize contacting anyone. The first pilot can be the owner's next suitable print or another consenting user's project. Record which before scheduling.

## Select a small useful project

Begin with one participant and one bounded task. Expand to three participants if the first session is usable: a beginner, an occasional maker, and an experienced operator if available. This is formative feedback, not a representative usability study.

Choose an existing, low-consequence need such as a desk tray, cable guide without mains exposure, or a noncritical fit coupon. Keep machine/material within the operator's known setup. Exclude safety-critical, food/medical/child-contact, pressure-bearing, electrical, and vehicle parts from this first pilot. Exclude unfamiliar machine procedures and unidentified laser stock. A drawing-only session is valid and should not be pushed into a physical run.

Agree on a time box (for example, 30 minutes assisted preparation plus normal machine time), material allowance, acceptance criteria, and scope before starting. The operator retains physical control. If preparation cannot establish readiness within the time box, score the useful handoff or blocker rather than forcing a print.

## Invitation script for the user to send

“I am testing a manufacturing assistant with one small project you already want to make. The session would take about 30 minutes of preparation, plus machine time only if you choose a physical trial. I want to learn where its advice helps or causes confusion. Participation is optional, and you can stop at any time. Would you be interested in a desk object, fit coupon, or drawing-only task?”

## Consent script before the session

“We are evaluating the assistant, not your ability. We will record the task steps, questions, decisions, time, errors, and your feedback. The operator stays in control of any machine and can stop the task. Please avoid credentials, personal identifiers, proprietary models, or anything you cannot share. May I keep a de-identified transcript and project measurements for improving the skill? Separately, may I capture screenshots or photos? Recording is optional and declining it does not prevent participation. Tell me what must be excluded and when you want the records deleted.”

Record explicit yes/no separately for participation, transcript retention, screenshots, and photos, with permitted uses, retention deadline, and withdrawal contact. Do not infer consent to public sharing, publication, or future contact. Delete or redact according to the agreed plan; the participant can ask to stop or withdraw their retained data. Use participant codes rather than names in the trial record. Store evidence only in the location agreed with the participant.

## Observe without coaching the answer

1. Before assistance, ask the participant to state the goal, intended next action, and what success means. Record their experience and the initial artifact/configuration.
2. Let them use the assistant naturally. Log clarifying questions, retries, incorrect claims, unnecessary blockers, manual interventions, and whether they understood the next step. When they stall, ask “What were you expecting here?” rather than supplying the desired answer.
3. For a physical trial, separately record generated-job identity, readiness evidence, operator decision to run, machine acceptance, actual material/settings, critical observations, completion, safe removal, and inspection. A transcript cannot substitute for these artifacts.
4. Afterward ask: “What was unclear?”, “Which advice changed what you did?”, “What did you have to correct?”, “What would you do next without help?”, and “Would you use this again for a similar task, and why?” Record exact quotations only with permission.

## Measures and evidence

Use `templates/user-trial.md`. Report raw values and denominators; do not turn three participants into population percentages.

- Preparation: elapsed minutes to a reviewable file, actionable handoff, or identified blocker; assistant questions and user corrections; facilitator interventions.
- Task outcome: complete / partial / stopped, against the participant's predeclared scope and acceptance criteria. Drawing completion is separate from physical acceptance.
- Comprehension: participant can explain next action and evidence needed, assessed from their own words, not a satisfaction score alone.
- Reliability: count unsupported completion/approval claims and unauthorized actions; target zero. Record whether a stop was appropriate rather than treating all stops as failure.
- Physical outcome when run: attempts, material used/wasted, observed job identity, dimensional readings with units/tool/uncertainty, fit/function observations, and accepted parts out of attempts. Include timestamps and configuration. Photos support appearance; measurements and tests support fit/function. Unavailable evidence stays unknown.

Proposed first-pilot success: agreed task reaches its scoped outcome or a justified actionable blocker within the preparation time box, the participant can state the next step, and no unsupported approval or unauthorized action occurs. Physical success additionally requires the predeclared inspection criteria to pass. Record failures even if a later retry succeeds.

## Stop and triage

Stop the session for withdrawn consent, private data exposure, exceeded agreed time/material allowance, or advice requiring unavailable capability. Stop physical execution for unidentified materials, machine warnings requiring resolution, unstable workholding/feed, extrusion loss, collision risk, smoke/odor, thermal/electrical anomalies, or operator uncertainty. Follow the machine's established safe-stop procedure; do not invent emergency steps.

Triage feedback into: critical unsupported/safety/action error (block further comparable runs until fixed and retested); reproducible workflow or technical error (preserve trace, make the smallest correction, replay affected behavior cases); usability friction (revise wording/routing and test with a fresh user); preference or out-of-scope request (record without automatically broadening the skill). Keep observation separate from proposed cause. Check new revisions against unaffected behavior cases and retain prior pilot evidence under its original version.

After the pilot, report who participated by anonymous experience group, task scope, consent limits, observed outcomes, failures, changes, and remaining unknowns. A successful desk tray does not validate another material, machine, structural use, or batch yield.

After a physical trial passes its scoped criteria, use `verified-print-library.md` to prepare a shareable evidence record. Keep unrun starter models and incomplete trials outside the verified catalog.
