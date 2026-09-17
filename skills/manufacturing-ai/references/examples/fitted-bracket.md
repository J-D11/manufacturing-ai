# Worked example: fitted desk cable-guide bracket

This illustrative FDM bracket slips over a desk edge and locates a lightweight cable guide. It supports no shelf, person, expensive equipment, or structural load. It is not a clamp for safety-critical use. A heavy or tightly tensioned cable changes the requirements.

## Define and model

Measure the desk thickness in several places where the bracket will sit. For an illustrative desk measured at 20.0 mm, create a C-shaped section with top and bottom arms that fit around that thickness. Identify any bevel or rounded edge; an otherwise correct gap may still bind there. Check the underside for an obstruction. Define whether the bracket should slide freely or gently resist movement, and require removal without marking the desk.

Use a dimensioned CAD sketch of the C section, then extrude it to make the bracket width. Illustrative starting geometry: 25 mm width, 15 mm engagement onto the desk, and 3 mm arm/back thickness. These are prototype dimensions, not strength ratings. Add an open cable notch that permits insertion without forcing a connector through a closed hole. Round exposed contact edges and preserve enough material around the notch.

For an opening H and measured desk thickness S, total clearance C = H − S. A test using H = 20.2, 20.4, and 20.6 mm around S = 20.0 mm compares total clearances of 0.2, 0.4, and 0.6 mm. Do not mistake these for per-side values or universal fits. Account for measurement uncertainty, desk surface finish, and the intended behavior.

## Test fit and orientation

Create labeled bracket samples at the candidate openings. A narrower sample can reduce material, but its flexibility changes: use it only to assess initial clearance, not retention or strength. Preserve arm thickness, engagement depth, and printing orientation. Choose orientation deliberately because deposited layers can separate under stress. Printing the C profile flat is a candidate that avoids spanning the opening horizontally during printing; inspect the resulting toolpaths and contact finish before accepting it.

In the slicer, confirm scale, continuous arms and back, notch detail, bed contact, and any support material required. Supports are temporary printed structures under otherwise unsupported regions; make sure they can be removed without damaging the fit surfaces. Use the verified printer/material profile rather than copying a setting from this example.

## Accept and recover

After safe removal, test at the actual desk location gently. Stop if it requires force or leaves a mark. For the full-width bracket, require complete seating, tool-free removal, no cracking, and stable position during the intended cable movement. Agree on a representative observation period before accepting ongoing use; a momentary fit does not establish long-term retention.

If it binds, locate the contact and compare actual dimensions before widening everything. If it fits but slips, changing material, geometry, or retention needs a new controlled trial. If it cracks, stop using it and review orientation, stress concentration, and section size. Increasing infill alone is not a diagnosis. Record the accepted scope as this lightweight cable-guide use only.

Editable source: [`fitted-bracket.scad`](../../assets/starter-models/fitted-bracket.scad). Read [starter-model instructions](../starter-models.md) for part selections, parameter changes, export checks, and proof limits.
