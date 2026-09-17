# Editable starter models

These OpenSCAD sources turn the worked projects into editable, dimensioned geometry. They are learning prototypes, not physically validated products or production profiles. OpenSCAD uses code to describe a model: edit the named values at the top, render, and export a new version. Source dimensions are millimeters; STL itself carries no authoritative unit declaration.

| Source | Default geometry | Part selections |
| --- | --- | --- |
| [enclosure.scad](../assets/starter-models/enclosure.scad) | Box outside 68 × 48 × 22 mm; cavity 64 × 44 × 20 mm; lid 68 × 48 × 5 mm including rim | `box`, `lid`, `mouth_coupon`, `rim_coupon` |
| [fitted-bracket.scad](../assets/starter-models/fitted-bracket.scad) | 20 mm desk plus 0.4 mm total gap; 3 mm arms/back; 15 mm engagement; 25 mm width | `bracket`, `fit_coupon` |
| [multicolor-sign.scad](../assets/starter-models/multicolor-sign.scad) | 100 × 35 × 3 mm base with 1 mm raised MAKE lettering | `sign`, `coupon` |

## Make a controlled revision

1. Preserve the starter and edit a copy. Discover a working OpenSCAD installation before promising to render it; the skill does not bundle the application.
2. Change only the dimensions needed for the test. The assertions reject several invalid parameter combinations, but do not establish printability or suitability.
3. Render the selected part, read warnings, and export a new STL. Inspect the exported bounds and geometry. A source file that has not rendered is prepared source only.
4. Import the export in millimeters into your verified slicer configuration and check actual layer Preview. Record the filename and parameter values with the test result.

Example commands, run from the skill directory after confirming `openscad` resolves to the intended executable:

```sh
openscad --version
openscad -o enclosure-box-v1.stl -D 'part="box"' assets/starter-models/enclosure.scad
openscad -o enclosure-rim-g030-v1.stl -D 'part="rim_coupon"' -D 'clearance_per_side=0.30' assets/starter-models/enclosure.scad
openscad -o bracket-c040-v1.stl -D 'part="fit_coupon"' -D 'clearance_total=0.4' assets/starter-models/fitted-bracket.scad
openscad -o sign-v1.stl -D 'label="MAKE"' assets/starter-models/multicolor-sign.scad
python3 scripts/inspect_asset.py enclosure-box-v1.stl --units mm
```

Use new output filenames; these commands can overwrite an existing output. On macOS the executable may live inside the application bundle instead of PATH. See the [official command-line documentation](https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html) and [official downloads](https://openscad.org/downloads.html). Runtime availability was checked against OpenSCAD 2026.09.03 on 2026-09-05; users should verify their own version.

## Interpret each test

For the enclosure, `clearance_per_side` is subtracted twice from each cavity dimension to obtain the rim outside dimension. The default 0.30 mm is an experiment. Export separate rim coupons for candidate clearances and label them physically or in a matching record before they become mixed. The mouth frame preserves the opening; the rim coupon has a perimeter backing instead of the full lid center. It tests initial fit, not full-lid flatness or closure flexibility. See [the enclosure guide](examples/enclosure.md).

For the bracket, `clearance_total` is added once to desk thickness. The rendered default bounds are 18 × 26.4 × 25 mm because the C section lies on the bed and bracket width grows vertically. The 8 mm-wide coupon omits the cable notch and tests clearance only; it cannot prove the full bracket's retention, notch printing, or strength. The notch and bed contact require slicer review. The source rounds edges of the C profile, but not every 3D edge or notch edge: inspect and finish sharp edges after removal. See [the bracket guide](examples/fitted-bracket.md).

For the sign, edit `label`, `font_name`, and `letter_size`. The requested font can resolve differently across machines. Inspect every glyph and enclosed letter space. Text is clipped to the plaque boundary, so oversized text can silently lose strokes even when the mesh is valid. Reduce text size or enlarge the base if that happens. The coupon crops the original at unchanged scale; move its center so it contains the critical strokes and enclosed spaces. An empty or unrepresentative crop proves nothing. STL exports contain no filament assignments, color changes, or pause commands. See [the sign guide](examples/multicolor-sign.md).

## Validation scope

The eight default part selections were actually rendered to binary STL with OpenSCAD 2026.09.03. Export inspection found expected outer bounds, finite geometry, no numeric zero-area triangles, and two incident triangles per undirected edge. The latter is a limited mesh check, not proof against self-intersections or a manufacturing gate pass. Nine invalid-parameter cases triggered assertions without producing STL outputs. Rendered images of the box, bracket, and sign were visually reviewed.

No slicer Preview, machine acceptance, physical print, fit, retention, or functional evidence is attached. Every customized revision needs renewed digital review and the relevant physical tests. Defaults are limited to dry craft storage, a lightweight cable guide, and a decorative sign as scoped in their guides.

The bundle includes default STL exports in `assets/starter-models/exports/`, render previews in `assets/starter-models/previews/`, and source/export hashes with basic mesh checks in `assets/starter-models/digital-validation.json`. These are digitally rendered starting files, not machine jobs or physically verified examples. Re-export after any parameter change; the included STL files will not update automatically.
