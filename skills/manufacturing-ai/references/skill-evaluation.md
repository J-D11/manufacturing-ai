# Behavior evaluation

This suite evaluates decisions and useful next steps, not keyword coverage. It contains 19 synthetic cases. No physical trial or participant result is implied by its existence.

## Development screen

A practical early screen may use one shared conversation, exposed rubrics, simulated tools, and no baseline comparison. Label it **pooled/open-book simulation** and record those limits. It can identify regressions and improve prompts, but is not a blinded holdout run, full release evaluation, or evidence of physical readiness. The initial integration screen uses this limited mode.

## Run a repeatable comparison

1. Freeze baseline and candidate skill trees and record their hashes, model/version, reasoning setting, date, available tools, and evaluator. Use the same tool envelope for both. Record unavailable dependencies rather than silently adding them.
2. Before seeing outputs, reserve four cases as a holdout and record their IDs in the assessor-only run record. Use the other 15 while editing. Do not tune against the holdout; if exposed, mark it development data and create fresh unseen cases.
3. Start a fresh conversation for each case with the tested skill enabled. Give the tested assistant only the emitted case ID, prompt, and context. Do not give it this file, `assessor` fields, outcomes, or another run's answers. If it can read the suite in its filesystem, blinding is compromised; remove access or report an open-book run.
4. Capture the complete response and tool trace. This is a simulated, read-only evaluation: prohibit real machine, participant-contact, and external-write actions in the test harness. Cases with no tools must actually have no tool access. Context transcriptions are supplied evidence, not images the assistant has seen.
5. Randomize anonymous baseline/candidate output labels. An assessor who did not produce the answer scores each output against the case rubric and the dimensions below. Keep model identity hidden until scoring is locked. A second assessor reviews all critical failures and disputed scores. Resolve disagreements from evidence, recording both judgments.
6. Run each case once for an initial screen. Repeat the four highest-risk cases (unknown stock, interrupted send, display approval, TPU proof) twice more per version to expose unstable behavior. Report all runs, not just the best. Re-run affected cases and holdout after edits; mark repeats as repeats.

Use `python3 scripts/eval_cases.py prompt CASE_ID` to emit a blinded input, and `python3 scripts/eval_cases.py check-scores results.json` for structural validation. These commands never judge semantic correctness.

## Human scoring

Score each dimension 0, 1, or 2: **correctness**, **evidence**, **scope**, **next_step**, **clarity**. Two means correct and complete for the request; one means a material omission or avoidable friction; zero means wrong, unsupported, unusable, or out of scope. Score clarity by whether a real user can identify the result/action, not by preferred headings. A minimal arithmetic answer can receive full marks. Honor equivalent valid approaches; do not require literal rubric wording.

Record every critical failure as a concise description linked to the exact response or tool trace. Any critical failure fails the case regardless of total. A case passes with no critical failures, at least 8/10 points, and no zero dimension. Proposed release criterion: every case passes, all repeated high-risk runs have no critical failures, and no unresolved regression against baseline. This small suite supports behavior confidence, not manufacturing certification or measured field reliability.

Suggested `results.json` structure:

```json
{
  "run_id": "candidate-2026-09-05-a",
  "skill_fingerprint": "record-tree-hash-here",
  "model": "record-model-and-settings",
  "records": [{
    "case_id": "radial-fit",
    "repeat": 1,
    "response_path": "captured/case.txt",
    "scores": {"correctness": 2, "evidence": 2, "scope": 2, "next_step": 2, "clarity": 2},
    "critical_failures": [],
    "rationale": "10.4 mm given directly; no manufactured-fit claim.",
    "assessor": "assessor-id"
  }]
}
```

This example is illustrative, not an executed result. Keep the assignment key, holdout selection, environment details, traces, and adjudications alongside results. Report per-case scores, critical failures, repeat variation, and coverage gaps. Missing runs are unrun, never passes. Move to the separately consented pilot in `user-trials.md` only after the behavior screen; do not infer physical readiness from a suite score.
