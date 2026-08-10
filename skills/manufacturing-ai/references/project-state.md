# Project State

Use these ordered states: Idea; Requirements defined; Manufacturing process selected; Source assets collected; Design created or located; File inspected; File repaired or converted; DFM review complete; Material selected; Hardware selected; Orientation planned; Process settings configured; Prototype strategy defined; Calibration complete; Test part prepared; Test part produced; Test part inspected; Full production prepared; Production job generated; Production job sent; Machine accepted job; Actively manufacturing; Manufacturing complete; Part removed; Part cleaned or post-processed; Part visually inspected; Part dimensionally inspected; Part fit-tested; Part function-tested; Assembly complete; Final quality review complete; Approved; Rejected; Revision required; Archived.

Use statuses: Not started, Ready, In progress, Waiting on dependency, Needs review, Needs revision, Failed, Recovered, Approved, Complete, Blocked.

Evidence examples: screenshot or file inspection for import; slicer Preview for toolpath; printer status for acceptance; photo plus observation for completion; caliper measurement for dimension; physical mate or scan for fit; repeatable use test for function. A 100% printer display is not part approval.

Treat calibration, test, readiness, and production states as scoped gate results, not global approvals. Record the configuration fingerprint, named risk, evidence, proof limits, and dependent gates. The fingerprint includes the exact file revision, machine/tooling, workholding or build surface, material and lot, profile, environment, and relevant condition.

When later evidence contradicts a result, move only the affected stage to Failed or Needs revision, reopen its dependent gates, and preserve unrelated geometry, file-integrity, or process evidence. Preserve immutable preflight artifacts and append machine-run and inspection records; the shared state points to the latest applicable evidence.
