# Worked example: two-color desk sign

This illustrative FDM project makes a small flat plaque with raised lettering. It can use a compatible automatic material system or a verified manual color-change workflow. If neither is available, a single-color print is still a useful prototype. No particular printer feature is assumed.

## Choose the design and color route

Agree on the exact text and intended viewing distance. An illustrative plaque is 100 × 35 × 3 mm, with raised letters 1 mm above the top. These dimensions are starting geometry, not validated minimums. Use text or graphics the user has permission to reproduce. Start with a plain, bold typeface and short text; narrow strokes may disappear in slicing.

Model the base and text in a CAD tool or supported text workflow. Check that letters meet the base and that enclosed letter spaces remain open. Export a version that preserves any separate-body information required by the chosen color workflow. Preserve the editable source and inspect the exported dimensions.

If all lettering begins above the top of the base, a supported layer-based color change may suit the design. Do not promise an automatic pause or safe manual swap until the actual slicer and printer workflow is verified. A design with two colors on the same layer generally needs a different supported workflow, such as compatible automatic switching or separately printed inserts. Do not instruct a user to manipulate moving or hot machine parts.

## Print a representative fragment

Select the smallest plaque fragment containing the narrowest stroke, an enclosed letter space, and the actual color transition. Keep letter size, height, base thickness, orientation, and material combination unchanged. Do not shrink the whole sign, since that tests different text geometry.

In Preview, follow the layers from base through letters. Confirm that every intended stroke has a toolpath, the letter interiors remain open, the base is continuous, and the color change occurs where expected. Inspect switching or purge behavior if used; purge is material expelled during a change to clear the previous color. Treat the displayed time and material as estimates, and check the actual loaded colors and materials against the job before printing.

## Accept and recover

After safe removal, require readable text at the agreed distance, continuous strokes, acceptable color separation, attached lettering, and a plaque that rests as intended. A fragment pass approves the tested detail and transition, not the full plaque's flatness. Inspect the completed full-size sign before declaring it finished.

If strokes are missing in Preview, enlarge or thicken the text and inspect again before printing. If letters appear in the model but not Preview, check their height and contact with the base. If color is contaminated, review the actual transition and compatible machine guidance before changing purge settings. If lettering separates physically, investigate material compatibility and bonding conditions. Do not relabel a readable but detached letter as a successful sign.

Editable source: [`multicolor-sign.scad`](../../assets/starter-models/multicolor-sign.scad). Read [starter-model instructions](../starter-models.md) for part selections, parameter changes, export checks, and proof limits.
