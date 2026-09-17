# Reuse what physical printing taught us

## Keep the current version unambiguous

Maintain a project-local `release.json`: revision, status (candidate, sliced, sent, operator-tested), source/export/project/job paths and SHA256 hashes, machine/nozzle/material/plate, color-to-AMS mapping, expected pauses, and dated evidence. Keep immutable prior revisions in an archive; update the current pointer only after verifying its targets. Do not remove the last working version. Opening a project does not authorize printing it. A timeout during send requires checking the device before retrying.

## Capture scoped physical results

After operator feedback, record exact wording, which artifact was tested, hardware present or omitted, configuration, and what remains unknown. Store private project records locally; do not automatically publish them in the shared verified-print catalog. Unknown job identity or missing measurements stay explicit. Use `verified-print-library.md` before promoting a record into that catalog.

Example from badge development: operator-reported success for a P1S 0.4 mm PLA coupon with an 8.2 mm diameter, 2.2 mm deep cavity for an 8 x 2 mm magnet, 0.2 mm floor, 0.6 mm roof, 0.1 mm layers, and pause before layer 25. The first test omitted the magnet; a second included it and was reported successful. This supports reusing the pocket as a starting point on that setup. It does not establish pull force, fatigue life, or fit on other machines. A separately successful gate coupon does not certify a full thinner holder with additional magnets.

## Preserve interfaces when dimensions change

Express attached features relative to functional datums, not independent absolute heights. For example, gate recess Z = badge-seat Z + recess offset. Lowering the base must move the gate, nibs, recesses and grip together while preserving their relative clearances. Store intended dimensions and tolerances alongside CAD.

Before export, assert pocket floor/depth/roof sums, magnet count and matching centers, roof coverage, minimum wall thickness, seated gate clearance, and print-bed contact. Compare old/new exported bounds and intended changed dimensions. Use CAD Boolean checks for unintended interference; exclude and explicitly document intentional detent interference. Check insertion travel as well as seated fit. Mesh manifold checks cannot prove these functional relationships.

## Preflight the actual job

Run existing `inspect_asset.py` checks on geometry. For native Bambu sliced packages use `scripts/check_print_job.py JOB --pauses 25 --printer 'Bambu Lab P1S' --nozzle 0.4` (omit pause arguments to require zero insertion pauses). Inspect its limits before treating results as complete.

Also inspect Preview for open pockets at the hold point, first closing layer, support inside cavities, part spacing including brim/prime tower, unsupported details, correct size and material assignment. Compare the current file hash with the reviewed file before send. The checker does not detect collisions or verify hardware on the printer.

A pause belongs immediately before the first sealing extrusion, not simply at a magnet's nominal thickness. Recompute from actual sliced layers when first-layer height, adaptive layers, pocket height or orientation changes. Do not count a commented `machine_pause_gcode` setting as an executable pause.

For repeatable dimension contracts, export measured values from the current CAD/mesh and run `python3 scripts/check_dimensions.py measurements.json`. Its JSON schema is in the script docstring. Checks can enforce floor + pocket + roof = base, base + detent offset = recess Z, minimum edge clearance, or old/new mating offsets. It checks supplied values, not geometry itself; copying intended values into the input is not independent verification. Preserve the extraction method and artifact hash. Run a regression with a deliberately unmoved recess to ensure the check detects the original class of error.
