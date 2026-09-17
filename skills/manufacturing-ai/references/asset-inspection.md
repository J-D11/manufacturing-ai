# Read-only asset inspection

Use `scripts/inspect_asset.py` when Python 3.8 or newer is available (the supported minimum). It requires only the standard library and opens the input read-only. Run from the skill directory, or replace the script path with its installed absolute path:

```sh
python3 scripts/inspect_asset.py '/path/to/part.stl'
python3 scripts/inspect_asset.py '/path/to/part.stl' --units mm
python3 scripts/inspect_asset.py '/path/to/design.3mf' --max-bytes 10485760
python3 -m unittest discover -s tests -p 'test_inspect_asset.py' -v
```

The CLI prints deterministic JSON to stdout. It does not create reports, alter source files, launch applications, repair geometry, send jobs, or approve a part. Capture output in a new report only when needed; ordinary shell `>` can overwrite files, including your source, so do not redirect to an existing path.

## Interpret results precisely

| Exit code | Meaning | Next action |
| --- | --- | --- |
| 0 | Supported STL geometry parsed; bounds and numeric zero-area count available | Read warnings, confirm units and dimensions, then inspect in CAD/slicer. This is not a file-integrity or production gate pass. |
| 2 | Invalid input, malformed or unsupported STL/3MF variant, read error, or size limit | Read `error`; no geometry verified. CLI argument errors instead use argparse stderr and may not emit JSON. |
| 3 | Partial 3MF inspection, or metadata-only for other unsupported formats | Read `status`, `geometry`, and gaps. Use a format-aware tool for remaining checks. |

`fingerprint` contains SHA256 and byte size of the captured bytes. 3MF receives the bounded partial inspection below. STEP, OBJ, GLB, SVG, and other unsupported extensions receive **metadata only**, with units unknown and not inspected. The STL-only `--units` option is rejected for these formats; it cannot stand in for parsing their embedded units. A filename extension is not format validation.

For STL, the parser selects binary when the declared triangle count exactly matches the file size, including a binary header that starts with `solid`. Otherwise it attempts a strict, single-solid, line-oriented ASCII STL parse. Whitespace-only lines are allowed. Each ASCII line is limited to 4096 bytes including its line ending; longer lines fail before decoding or tokenization. This conservative limit also applies to solid names and blank lines. Nonstandard variants, multiple ASCII solids, trailing data, empty meshes, truncated facets, and nonfinite numbers fail conservatively. No partial bounds are returned on failure.

STL `bounds` are axis-aligned minimum, maximum, and extent in **unknown model units** unless the user supplies `--units`. A units argument labels numbers as user asserted; it neither detects nor converts units. Confirm a known dimension in the source and slicer before interpreting them as physical measurements. Large extents that overflow numeric representation are rejected.

`numeric_zero_area_triangles` is a floating-point diagnostic, not a mesh validity result. It can miss near-degenerate triangles and can classify extreme dynamic-range geometry inaccurately. A zero count does not prove manifoldness, closed volume, consistent normals, strength, printable walls, correct scaling, or successful slicing. Normals are checked only for finite values.

## Resource and evidence limits

The maximum file snapshot is 64 MiB; `--max-bytes` may lower this limit, not raise it. Above-limit files fail before hashing. Parsing may use additional memory proportional to the bounded snapshot, and large valid meshes may take time. ASCII lines are read with the separate 4096-byte cap to bound tokenization memory. For larger files, use a suitable installed mesh tool and record its limits; do not silently omit geometry or claim this helper inspected it.

Only regular files are accepted. Binary mode is explicitly requested on Windows to preserve raw bytes for hashing and parsing. Symlinks to regular files inspect the opened target. Common concurrent size/time changes cause failure; this is not a filesystem snapshot or protection against hostile concurrent modification. Prefer frozen versioned inputs. The hash identifies captured bytes, and does not prove the current path or eventual machine job still contains them.

Pair this output with source revision, confirmed units, CAD/slicer inspection, warnings, orientation, and physical checks. Geometry inspection alone never authorizes manufacturing.


## Partial 3MF inspection

Keep `inspect_3mf.py` alongside `inspect_asset.py`. Run `python3 scripts/inspect_asset.py '/path/to/project.3mf'` without `--units`. Successful partial inspection returns exit 3, top-level `status: partial`, and schema version 2. STL retains schema version 1 and its existing exit behavior. Invalid packages or unsupported strict variants return exit 2 with an error. This helper is a conservative inspector, not a conforming 3MF implementation or schema validator.

The Consortium Core Specification 1.4.0 identifies the primary model using the package StartPart relationship. Model units default to millimeter. Component and build transforms contain 12 row-major affine values; translation occupies the last three. Required extensions affect whether an application can process the model. UTF-8 is required for core XML and DTDs are disallowed. These semantics were checked against the [3MF Consortium core specification](https://github.com/3MFConsortium/spec_core/blob/master/3MF%20Core%20Specification.md), sections 2.1, 2.3, 3.3, 3.4 and 4.2, accessed 2026-09-06.

Implementation output:

- `root_model_path` comes from the exact StartPart relationship, not an assumed filename.
- `inventory` hashes every bounded non-directory member without extracting it.
- `units` and `units_source` distinguish the model attribute from the core default. User `--units` is rejected for 3MF.
- Object IDs, mesh vertex/triangle counts, finite coordinates, triangle index ranges, local component/build references, and local cycles are checked. Numeric attributes permit surrounding XML whitespace; split numeric tokens and non-XML whitespace are not accepted. These checks do not validate topology, resource ordering, property/material references, or full XML schema semantics.
- Transforms retain their parsed XML attribute literal. XML attribute whitespace normalization may occur. Their 12 numeric values are checked, but transforms are never applied; no world-space bounds, determinant, invertibility, or physical dimensions are computed.
- `profile_candidates` lists filename-selected config/INI/JSON/profile/PrintTicket candidates with size and hash only. This does not establish format validity, active slicer settings, or delivered machine settings.
- Unknown extension namespaces and required-extension declarations produce explicit gaps. Cross-part component and build paths must exist, but referenced object IDs and assembly semantics in other model parts remain unverified. Opaque extension fields are not interpreted and never establish a complete assembly. Additional model XML is checked for bounded well-formedness only.

Conservative processing limits: 128 ZIP entries, 8 MiB per expanded member, 32 MiB total expanded bytes, compression ratio at most 200, and the existing 64 MiB input cap. ZIP directory records are counted before allocating archive entries, including bounded single-disk ZIP64 end metadata. ZIP64 extensible end sectors and unusual directory layouts remain unsupported. XML limits are 200,000 nodes per part, depth 64, 32 attributes per element, and 1024 characters per tag/attribute value. Root model limits are 256 objects, 2048 component references, 2048 build items, and 32 extension namespaces. Output is capped at 1 MiB. Large or unusually compressed legitimate packages can be rejected by these intentional limits.

Multipart archives, encryption, symlinks, unsafe or duplicate/case-colliding member paths, URI-escaped names, unsupported compression, missing relationship targets, external relationships, malformed XML, and DTD/entity declarations are rejected. Standard XML character escapes remain supported. Nothing is extracted or fetched. Only stored/Deflate ZIP and supported simple internal paths are accepted. Package content-type root syntax is checked, not complete content-type declarations. Non-XML embedded config contents are hashed without parsing. These limits are part of the result, never grounds to bypass the inspector or claim production readiness.

Regression fixture `tests/fixtures/openscad-enclosure-box.3mf` is a 2002-byte OpenSCAD 2026.09.03 export supplied by the root integration run, SHA256 `156096397311f660ddeea36d4b363d106c37e4be0e833d0240bb66a97843fa65`. It exercises ZIP64 metadata, 16 vertices and 28 triangles; it is digital inspection evidence, not a printed fit result.
