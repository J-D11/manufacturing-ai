# Tool-aware execution

Use this when the task needs file inspection, CAD edits, slicing, or machine interaction. Discover only the capabilities needed for the next step. A simple fit calculation needs no application inventory.

## Establish what can actually be done

Inspect exposed tools or installed applications and their documented interfaces. Record a compact capability result for the active task: available and tested, available but untested, unavailable, or unknown. These are separate capabilities:

- Read source files and compute file identity.
- Inspect geometry and dimensions in a compatible parser or application.
- Edit native CAD, mesh, or planar artwork and export the requested format.
- Configure a slicer, generate the job, and inspect actual toolpaths.
- Observe printer state, send a job, or control a machine.

An application being installed does not prove an automation API works. Confirm a harmless read or inspection before relying on it. Do not infer CAD editing from image generation, geometry integrity from a renderer, or printer control from a slicer window. Do not install software, create accounts, or assume paid services merely to finish an advisory answer.

## Choose the strongest available route

1. Use a supported tool, CLI, or application interface for the exact operation. Read its current documentation when syntax, export behavior, profiles, or device support is uncertain. Verify results in the output artifact, not just a success message.
2. For basic file checks, use `scripts/inspect_asset.py` as described in `asset-inspection.md`. Treat its stated inspection limits as part of the result. Unsupported geometry still needs a compatible tool.
3. If only UI access works, use the actual observed controls and validate the resulting file or Preview. Do not guess menu names across versions or report clicks as completed without evidence.
4. If execution is unavailable, give a precise manual handoff: input file/revision, target application and known version, intended operation, expected visible result, and the evidence to return. Ask for the version or a view of the relevant controls when it changes the instructions. Keep preparing any independent dimensions, drawing, or test plan.

Respect the user's chosen tools when they can perform the job. For parametric CAD, preserve the editable source and units alongside a versioned export. A script or textual model specification that has not run is prepared source, not generated or inspected geometry. Do not rename a mesh extension to imply a CAD conversion.

## Verify a file handoff

Reopen the export in suitable tooling and compare critical bounds, dimensions, units, orientation, body/instance count, and interfaces against the design. In the slicer, confirm the correct printer, nozzle, physical plate, and material. Imported third-party profiles can replace settings, so inspect active values before generating a job. Review layers and relevant regions after slicing; a model screenshot cannot substitute for Preview.

Identify source, export, slicer project, and machine job separately. Record hashes when exact byte identity matters. Preserve originals and create a new output version. If an operation partially succeeds, inspect existing outputs before rerunning. For a timed-out send, reconcile queue and active-job identity before retrying; no response is not evidence of failure.

## Ground settings in the actual setup

Use current official guidance for the exact printer/nozzle, build surface, and material product when proposing temperature, drying, compatibility, or maintenance steps. Record source URL, product/version, and access date with the relevant recommendation. A generic polymer name or community profile is not proof of the exact product's limits. If authoritative guidance conflicts, identify the conflicting setup assumptions and resolve them before running the affected operation. Keep numerical examples explicitly illustrative unless backed by a matching recorded result.

Machine execution is a separate capability and evidence stage. Existing user authorization carries forward, but preparing a file does not itself authorize a send. Preserve the user's intended completion scope and any explicit machine-action constraints. Never claim continuous monitoring unless an actual observation mechanism is active; otherwise specify the next operator checkpoint.
