# Manufacturing Orchestration

For multi-step execution, maintain one shared record throughout the project; keep simple advisory answers inline. Record approved decisions, versions, settings, evidence, risks, failures, and the next gate. Do not let a specialist discard prior approval.

Use applicable phases within the requested completion scope, recording N/A reasons where appropriate: intake; process selection; asset collection; file review; DFM; material and hardware selection; orientation and settings; calibration and test; production; inspection; approval; archive.

## Delegation decision

Use an installed specialist for its narrow scope, even for a single question; load its skill locally when a separate agent is unnecessary or unavailable. For parallel agents, require authorized, independent questions whose investigation materially improves evidence without simultaneous control of a file, machine, or physical part. Keep dependent phases sequential.

Before delegation, freeze exact baseline paths, versions or hashes, machine/tooling, workholding or build surface, material and lot, profile, environment, approved assumptions, and known failures. Give each assignment an ID, one question, inputs, exclusions, evidence requirement, stop condition, and downstream dependency. Use `templates/specialist-request.md`.

Useful independent evidence links include:

- source CAD or mesh geometry and dimensional comparison;
- slicer objects, settings, assignments, and Preview;
- generated-job or G-code layers, transitions, pauses, and tools;
- official process, machine, material, or safety guidance;
- physically successful versus failed artifact comparison;
- forward-validation design and predicted decision branches.

Do not parallelize overlapping edits, production sends, machine control, disassembly, physical approval, or two agents answering the same question unless deliberate replication is documented. If an agent needs to edit, finish and reconcile the investigation first, then assign one sequential writer.

## Reconciliation

Accept a result only when it identifies inspected inputs and versions, tools used, confirmed findings, inferences, evidence, contradictions, limitations, what it proves and does not prove, and the recommended next validation. Check that every result used the frozen baseline. Do not resolve contradictions by majority vote; request a targeted follow-up only when the conflict changes the next gate.

Maintain the evidence chain without collapsing stages: source geometry; configured process; generated job; machine-delivered state; physical response; removed-part inspection; fit and function. An agent may recommend a gate decision, but Manufacturing AI alone updates shared state and approval.

## Forward validation and recovery

Define every test with a hypothesis, held constants, one controlled variable, predicted observation, pass/fail threshold, proof limits, and next decision for each branch. Compare against the nearest physically successful baseline when available, not merely a file that sliced.

On failure, preserve unaffected work, classify the stage, invalidate only dependent gates, select one meaningful change, verify the changed value or behavior at the machine, retest, and record the physical response. Stop full production when the failure repeats; broaden the hypotheses and return to a smaller diagnostic.
