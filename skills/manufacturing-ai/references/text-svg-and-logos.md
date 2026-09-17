# Text, SVGs, and Logos

Choose raised, recessed, engraved, flush, cut-through, multicolor, separate, inlaid, painted, or post-applied treatment based on material and process. Inspect stroke width, font weight, spacing, minimum feature, emboss height or engrave depth, Boolean result, Z position, bed contact, color assignment, curvature, and orientation.

Always inspect text and logos in slicer Preview, not only Prepare view. If text is buried, confirm its top face clears the model surface before recommending a test plaque.


## Reconstruct from a supplied image

Prefer an available vector original. Otherwise trace the silhouette and symbol from the supplied reference, preserving proportions and topology; treat raster shading/highlights as lighting, not geometry. Compare a front-view CAD render against the reference before approving the outline. Label a hand-built approximation as stylized and get appearance feedback before production. Measure minimum strokes and gaps at final physical scale. A generated illustration is not a dimensionally accurate CAD trace.

For two-color raised logos, keep base and detail in a shared coordinate system and import as parts of one object. Do not drop raised detail independently onto the bed. Verify part Z ranges, contact with the base, and the intended shared transform. Assign both the filament profile and color; color swatches alone do not establish the material or physical AMS slot. Recheck the mapping in the send dialog, especially black versus dark gray and white versus cream.

Prefer native Bambu save/export. If accessibility reads corrupt tree labels or edits behave unpredictably, stop repeating them. Save a separate copy, inspect native metadata, and correct only known labels/material assignments if necessary, preserving meshes, transforms and IDs. Reopen and visually verify the result. Any metadata change invalidates the previous slice; reslice before sending. Never infer success from a patched XML field alone.

Check Preview confirms the base and symbol colors, shared placement, layer count and expected color changes. Remove inherited magnet pauses for projects without inserts. Keep manual filament changes distinct from AMS changes and insertion pauses.
