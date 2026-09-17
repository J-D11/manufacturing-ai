# Process-specific execution evidence

Read only the branch selected for the job. Obtain exact material and machine instructions when their compatibility, settings, or maintenance affect the decision. Record source/version and unresolved conflicts rather than inventing universal settings.

| Process | Before production | Smallest useful proof | Completion evidence |
| --- | --- | --- | --- |
| Resin | Exact resin and printer compatibility; orientation, supports, drainage and trapped volumes; wash/cure procedure and handling arrangements | Representative detail, support, wall, or fit section with the intended post-processing | Inspect after specified wash/cure and support removal; check cavities and critical dimensions in the finished state |
| CNC | Stock and datum; tool and holder; fixture/clamps; work offsets, reach and clearance; correct postprocessor and operation order | Appropriate simulation plus operator-controlled setup verification and first feature/part | Inspect dimensions, finish, burrs, and datum relationships; simulation alone does not validate workholding or machine offsets |
| Laser | Positively identified stock/coating, compatibility, extraction, focus, work area, and cut/engrave assignments | Material-specific kerf/fit or engraving coupon under the verified setup | Check cut-through, dimensions, edge quality, heat damage, and fit; unknown material remains unresolved before cutting |
| Molding/casting | Exact material system, tooling, draft/parting, undercuts, vents, shrinkage assumptions, demolding and cure procedure | Representative mold section or first article | Inspect after the required cure/conditioning; assess voids, fill, dimensions, demolding damage and function |
| Outsourcing | Revision-controlled drawing/model, units, material, tolerances, finish, quantity, inspection requirements, and quote scope | Supplier DFM feedback and first-article inspection when needed | Reconcile delivered revision, quantity, material documentation and inspection results; a quote or supplier promise is not acceptance |

For each branch, use the existing state, test, and inspection templates with process-appropriate fields. Do not apply FDM wall, infill, first-layer, or slicer checks to an unrelated process. If the necessary tooling or operator access is unavailable, finish the reviewable design/specification and identify the exact execution handoff.
