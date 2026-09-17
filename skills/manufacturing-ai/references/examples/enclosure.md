# Worked example: small storage enclosure

This illustrative FDM project makes a box with a removable lid for small dry craft supplies. FDM builds a part by depositing layers of material. It is not an electrical, battery, food, or child-safety enclosure. Dimensions below demonstrate reasoning, not a validated design.

## Define and model

Suppose the contents occupy a measured 60 × 40 × 15 mm space. Choose a concept cavity of 64 × 44 × 20 mm so the contents can be lifted out. With illustrative 2 mm walls and a 2 mm floor, the outside box is 68 × 48 × 22 mm. Confirm the chosen wall can be represented by the intended nozzle/profile in Preview. Use a material compatible with the actual printer and indoor storage conditions.

In an available CAD tool, sketch the outside rectangle, extrude it to the outside height, and remove the inner rectangle from the top, leaving the floor. Make a separate flat lid with a shallow locating rim on its underside. The rim sits inside the opening; it does not need to snap in. Save the editable source and export a new print-file version. Check both bodies' dimensions after export.

Let g mean clearance **per side** between rim and opening. Rim outside dimensions are (64 − 2g) × (44 − 2g) mm. Select candidate values around any known successful local fit; if none exists, an illustrative test ladder might compare g = 0.15, 0.30, and 0.45 mm. These are experiments, not guaranteed allowances. Keep the rim wall and engagement depth identical to the planned lid.

## Test the uncertainty first

Print a shallow box-mouth frame and matching lid-rim samples with the actual opening size. Label the candidates. Preserve corner geometry, orientation, material, and profile. This tests closure fit while omitting most box height and lid area. Before printing, define success: the lid seats by hand without forcing, can be lifted off without tools, and does not rock noticeably on a level surface. If another retention behavior is needed, change the requirement first.

For the full box, place its floor on the bed with the cavity upward. For the lid, placing its flat exterior on the bed and the rim upward is a starting orientation to inspect. In Preview, check continuous floor and walls, all rim layers, bed contact, and unexpected gaps or supports. Confirm the exact job and material at the machine before running it.

## Accept and recover

After safe removal, inspect for sharp edges, cracks, lifted corners, and incomplete walls. Try the actual contents and repeat opening and closing. Record which rim candidate passed. The coupon proves only the tested fit; the full lid still needs a flatness and closure check.

If every rim is tight, measure the opening and rim before changing geometry. If only the bed-adjacent edge binds, investigate that local edge and first-layer expansion rather than globally scaling the box. If the full lid warps after the coupon passes, reopen flatness/process checks; do not discard the fit evidence automatically. Save the accepted file and setup only after full-part inspection.

Editable source: [`enclosure.scad`](../../assets/starter-models/enclosure.scad). Read [starter-model instructions](../starter-models.md) for part selections, parameter changes, export checks, and proof limits.
