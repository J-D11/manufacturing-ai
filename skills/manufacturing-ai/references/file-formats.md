# File Formats and Preservation

Support STL, 3MF, STEP/STP, OBJ, GLB/GLTF, SVG, DXF, native CAD projects, mesh files, slicer projects, machine files, tracing images, and dimensioned PDFs. Capabilities depend on the installed application; inspect rather than assume conversion or editing support.

For every file, preserve the original and record path, format, size, units, dimensions, object/body/plate count, embedded profiles, warnings, and modifications. Use clear versions such as `project_original.stl`, `project_repaired_v1.stl`, `project_fit-test_v2.step`, and `project_production_v3.3mf`. Never overwrite silently.


## Format-specific inspection

- STL: do not infer units from the extension. Confirm an external dimension or explicit source units before scaling. Record bounding box and disconnected shells; shells are not necessarily intentional CAD bodies.
- 3MF: distinguish a model package, slicer project, and generated-job package by inspecting contents in compatible tooling. Check units, transforms, instances, plate layout, and embedded profiles. A filename or thumbnail does not prove the active settings or job identity.
- STEP/native CAD: check imported units, solids versus surfaces, assembly placement, and critical feature dimensions. A mesh conversion loses editable design information; retain the CAD source.
- OBJ/GLTF/GLB: inspect transforms, instances, scale, and referenced assets. Rendered color or texture does not create printable material assignments or watertight solids.
- SVG/DXF: confirm document units, view box or insertion scale, closed contours, duplicate paths, strokes versus filled outlines, and text/font dependencies. Verify the final toolpath does not cut shared edges twice.
- Generated machine files: identify target machine, dialect, tooling, coordinate assumptions, and embedded start/end commands. Do not send an unknown downloaded job because its model looks correct; regenerate with the verified setup when possible.

## Before/after evidence

Record source and output hashes when files feed a machine or several revisions could be confused. Compare bounds, critical dimensions, body/instance count, orientation, openings, mating faces, and intended regions in suitable tools. State which checks could not be performed. Hash identity proves bytes, not manufacturability. A parser failure or unsupported format is an inspection limitation, not a clean result.

For supported read-only STL and partial 3MF checks, see `asset-inspection.md`. A partial package report does not establish assembled bounds, extension semantics, active slicer settings, or print readiness.
