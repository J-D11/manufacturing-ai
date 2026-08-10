# Slicer Planning

Set printer, nozzle, plate, filament, layer height, line width, walls, top/bottom layers, infill, support/interface, brim/raft, seam, ironing, speed, cooling, temperature, flow, pressure advance, retraction, purge/prime strategy, and adaptive settings as a system.

Balance strength, quality, accuracy, time, cost, reliability, and waste. In Preview, inspect first layer, layer progression, islands, bridges, supports, gaps, thin walls, text, holes, seams, travel, purge, color changes, surfaces, time, and material. A slice that completes is only sliced, not production-ready.

Reconcile the generated job with both the source intent and the physical setup. Verify the actual workholding or plate identity, side, condition, and compatible profile rather than inferring it from appearance. For each object, confirm emitted first-layer extrusion at the expected position and height, including real path contact or clearance after compensation settings; a nominal setting label does not prove the emitted geometry.

For multi-material or multi-tool work, require separate intended regions, correct assignments, material use in slice statistics, actual transitions in the generated output, adequate purge or prime behavior, live execution of critical changes when warranted, and hand inspection of every colored or bonded region. Model-view colors alone are not evidence.
