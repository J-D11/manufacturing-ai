# Bambu TPU First Article

Use this reference for standard TPU on an enclosed Bambu printer, especially an open-web, fit-critical, or travel-heavy part.

## Freeze identity first

Record the exact TPU product and distinguish standard TPU from high-speed or AMS-specific TPU. Prefer the product technical data sheet over a generic or downloadable profile when their temperature or flow limits conflict. Treat every starting profile as spool-, machine-, nozzle-, plate-, and geometry-specific until physically tested.

For standard TPU that is not explicitly AMS-compatible:

- Dry it according to the manufacturer before printing.
- Feed from an external dry box through the shortest practical low-friction path.
- Bypass the AMS and verify that the spool unwinds without tugging.
- On an enclosed P1/X printer, start with the front door open and the top removed or safely vented unless current manufacturer guidance for that exact material says otherwise.

## Smooth PEI and third-party plates

Match the physical surface, not the plate brand, to the closest slicer plate profile. A third-party smooth PEI sheet normally uses the Smooth PEI or legacy High Temp Plate proxy. Do not enlarge the printer's configured build area to the plate's advertised physical dimensions.

Before printing:

1. Remove any protective film.
2. Confirm the plate seats against the locators, lies flat, and clears the wiping region.
3. Wash with mild dish detergent and water, rinse, and dry fully.
4. Apply a thin, continuous water-soluble glue layer when TPU may overbond. Treat it primarily as a release barrier.
5. Let the plate cool to room temperature before flexing it. Do not peel thin TPU ribs upward while warm or use acetone on PEI.

Do not bypass a plate or localization warning. Stop and identify the mismatch.

## Conservative starting example

For standard Overture TPU 95A on a P1S with a 0.4 mm nozzle and smooth PEI, the following historical starting example has no supporting validation artifact attached here. It is not a validated preset. Use it only as a comparison after checking current official product and machine guidance:

- Nozzle: 225 C
- Bed: 35 C
- Flow ratio: 1.02
- Maximum volumetric speed: 3.0 mm3/s
- Retraction: 0.40 mm at 20 mm/s
- Layer height: 0.20 mm
- Arachne, 3 wall loops, 0 percent sparse infill
- Supports and prime tower off when geometry permits
- First layer 20 mm/s, outer wall 30 mm/s, inner wall 35 mm/s, bridge 20 mm/s
- Part fan off for layer 1, then 100 percent; auxiliary fan 70 percent
- Elephant-foot compensation: 0.10 mm for thin, fit-sensitive ribs

This example is not a universal TPU profile or physical approval. Verify the current technical sheet, exact plate, and emitted toolpaths before use.

## Stage the physical proof

Use the smallest test that preserves each risk:

1. Adhesion swatch: prove continuous first-layer extrusion, no lift, and safe room-temperature release without coating transfer.
2. Vertical web coupon: prove dry extrusion, feed stability, rib fusion, openings, bridge or crown behavior, and tolerable stringing.
3. Fit-band coupon: prove installation, removal, retention, permanent stretch, alignment, and device safety across repeated cycles.
4. Full first article: print only after every dependent coupon passes under the same recorded configuration.

When a coupon fails, hold all unrelated variables constant. Verify dryness and feed drag before changing temperature or retraction. Change one meaningful variable and rerun only the failed gate.

## Monitor an active print

Keep `actively manufacturing` separate from `finished`, `inspected`, `fit-tested`, and `approved`. A print that looks good so far is not a completed gate.

Stop immediately for:

- Extruder clicking, grinding, repeated skipping, or stopped extrusion
- Missing or transparent layers, widening gaps, or a rib no longer being deposited
- Filament stretching, kinking, buckling, or dry-box feed binding
- Base, lid, coupon, or brim lifting or moving
- A strand nest or blob growing into a nozzle-collision risk
- Nozzle dragging, collision, or layer displacement
- Thermal or fan errors, smoke, burning odor, or another electrical or mechanical abnormality

Fine hair-like stringing alone is not an immediate stop condition unless it accumulates into a collision risk. After completion, cool fully, remove safely, and inspect adhesion, surface, dimensions, fit, function, and repeated handling before approval.
