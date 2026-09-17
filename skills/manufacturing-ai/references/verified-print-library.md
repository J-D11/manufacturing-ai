# Library of physically verified prints

Use this library to reuse a result that someone actually printed and checked. Its catalog is `assets/verified-prints/catalog.csv`. It starts with zero entries because the bundled starter models have not had physical trials. Editable source, a rendered STL, a successful slice, and a planned test do not qualify as verified entries.

Keep candidate work and failed attempts in the project record. Add a catalog entry only when the named use and applicable inspection, fit, and function criteria have passed with recorded evidence. The library is a curated record of scoped results, not a list of universally recommended profiles.

## Create a record from a real trial

1. Copy `templates/verified-print.md` into the project's working records. Give the trial an ID and freeze the source model, exported geometry, slicer project, and generated job separately. Record hashes when available, dimensions/units, and the intended use. If an upstream CAD source or application export is legitimately unavailable, record that fact and reason instead of inventing it. Preserve the actual inspected geometry and available job identity; missing required physical observations still prevent verification. Define pass/fail criteria before printing.
2. Record the actual machine/nozzle, material product and condition, build surface, orientation, profile, and any delivered setting that affects the test. Link the relevant current official guidance with its access date. Preserve the settings export when supported; do not treat a screenshot of a preset name as the entire configuration.
3. Record each attempt, including failures and changes. Identify the exact job accepted by the machine. After safe removal, capture the applicable visual, dimensional, fit, assembly, and functional evidence with units, measurement tools, and conditions. Name evidence sources as direct observation or operator report. Photos support visible features, not hidden geometry or numerical tolerance by themselves.
4. Compare observations with the predeclared criteria. Leave the result unverified if a required observation is missing or inconclusive. A reviewer records the accepted use, proof limits, date, and evidence references; software can check record completeness but cannot attest that a physical test occurred.
5. For a shareable entry, obtain permission for the model, photos, measurements, and settings. Remove personal identifiers, credentials, network details, and irrelevant proprietary information. Copy the reviewable record and permitted evidence into a versioned folder under `assets/verified-prints/`, then append its row to `catalog.csv`. Relative paths in the record must resolve within the shared evidence bundle. Do not publish a link to inaccessible private evidence as if another maker could audit it.

A useful entry lets another maker answer: what was made, under which conditions, what failed, what passed, and what they still need to test. A claimed setting with no accessible supporting evidence remains an unverified comparison.

## Reuse without transferring approval blindly

Compare the current use, mating parts, geometry revision, machine/nozzle, material, surface, and orientation with the record. Name the differences that affect the relevant risk. Use the closest verified result as a starting comparison, then rerun the smallest affected test. Do not call a new machine/material combination verified merely because the model is unchanged.

Record reliability as raw counts and conditions, such as accepted parts out of attempts and the observed number of handling cycles. Avoid broad success percentages from one print. A fit pass does not establish fatigue, heat resistance, long-term creep, or batch yield.

## Corrections and retirement

Do not erase a failure or overwrite the evidence behind a prior result. Add a dated correction and preserve the original record. If later evidence contradicts its accepted use, change its catalog status to `withdrawn`, explain why, and identify which conclusions are affected. Use `superseded` when a newer record replaces it without disproving its original result. Keep these rows discoverable so an outdated recommendation cannot silently return.

Use catalog-directory-relative POSIX paths for `record_path`, for example `tray-001/v1/record.md` relative to `assets/verified-prints/`. Evidence paths inside that record are relative to its own folder. Keep both inside the shared library bundle.

The catalog columns are `id`, `title`, `status`, `process`, `machine`, `material`, `model_revision`, and `record_path`. Status is `verified`, `withdrawn`, or `superseded`; candidate/untested models belong in the starter-model workflow rather than this catalog. An empty catalog is an honest starting point, not a completed physical validation program.
