# Asset Brief Template

Complete this before generation. Keep one brief per semantic asset family; split the brief when camera, layer, or runtime behavior changes.

For each concrete value, cite an authority source. Use `TBD (owner: ..., gate: ...)` when no accepted source defines it. Do not infer a logical canvas from a display frame, a color budget from palette length, or an asset palette from the screen that contains it.

## Identity

- `id`: stable runtime name, for example `cars/player/paoche-title-3q-rear`
- `version`: `v01`, `v02`, ...
- `category`: `player`, `traffic`, `background`, `tile`, `ui`, `fx`, `weather`, or `animation`
- `owner`: person or agent responsible for the gate decision
- `target_screen_or_layer`: exact screen and compositing pass
- `authority_sources`: accepted asset spec, approved family manifest/anchor, art bible, and runtime contract
- `containing_surface`: menu CRT / flat gameplay / other; describe the container separately from the asset

## Construction contract

- `reference_role`: geometry / camera / material / palette / mood
- `reference_sources`: URLs or local IDs, with license/permission notes
- `view`: front / rear / side / 3q-front / 3q-rear / top / orthographic
- `camera`: focal or orthographic note, horizon, vanishing point, and perspective constraints
- `container_frame`: screen slot dimensions; not automatically the PNG or logical canvas
- `subject_safe_bounds`: maximum on-screen subject bounds inside the container
- `canvas`: separate source, logical working, and runtime PNG sizes plus the authority for each
- `subject_bounds`: `x`, `y`, `width`, `height` in source pixels
- `anchor`: normalized or pixel coordinate, usually bottom-center for vehicles
- `negative_space`: required margins and occlusion rules
- `must_preserve`: silhouette, wheelbase, feature locations, visible faces, collision cues
- `must_not_bake`: text, logos, HUD, road, shadow, glow, particles, or other runtime-owned layers

## Style contract

- `style_anchor`: approved asset or art-bible section
- `palette`: named palette and allowed role colors
- `palette_authority`: rule for this asset class; do not inherit from the container without an explicit rule
- `edge_rule`: hard pixel edges, outline policy, or other explicit rule
- `detail_budget`: rough color/detail limit at logical resolution
- `color_budget`: explicit family budget or `TBD`; canonical swatch count is not automatically the budget
- `pixel_grid`: base grid and scale method
- `dither_or_dot_rule`: where and how pattern density changes
- `text_policy`: add text in engine/font pipeline; never rely on generated glyphs

## Calibration contract

- `style_profile_id/version`: approved G1.5 recipe for this asset family
- `construction_master_hash`: prove every candidate used the same geometry input
- `candidate_matrix`: provider/model version, prompt template/version, prompt language, control type/weight, strength/denoise, seed policy, and post-process per candidate
- `parameter_authority`: source for every numeric control value; unresolved labels remain `TBD-low` / `TBD-high`
- `cross_model_mapping`: approved mapping when native parameters differ, or `none`; never assume normalized equivalence
- `comparison_board`: identical 1:1, target-size, and optional grayscale views
- `selected_recipe`: exact model/workflow/prompt/control/post-process configuration
- `recalibration_triggers`: material changes to model, prompt template, control workflow, palette policy, or material/detail language

## Runtime contract

- `runtime_size`: exact PNG dimensions or scale range
- `alpha`: binary / partial-alpha approved for FX only
- `padding`: transparent safe padding in pixels
- `pivot`: engine pivot and anchor behavior
- `atlas_group`: sheet/group name, if any
- `animation`: frame count, frame duration, loop, and anchor lock
- `minimum_readable_size`: smallest in-game display size
- `import_settings`: filtering, mipmaps, compression, color-space, and engine-specific notes

## Unknown-value rules

- Preserve unknowns as `TBD`; attach the owner and gate that must resolve them.
- Treat numeric examples and tool presets as non-authoritative.
- Distinguish camera/composition by use: gameplay rear, title three-quarter, and selection side views are separate contracts.
- Distinguish a sprite's palette/effects from those of its parent window or background.
- Do not issue generation, quantization, packing, or import commands while a required value is `TBD`.

## Prompt blocks

Use the blocks as constraints, not as a substitute for the contract.

### Construction prompt

```text
Create a neutral construction master of [SUBJECT] in [VIEW].
Preserve [MUST_PRESERVE]. Use [CAMERA] and place the subject at
[SUBJECT_BOUNDS] with [ANCHOR] and [NEGATIVE_SPACE]. Use a plain
contrasting background and no text, logo, UI, baked shadow, glow, road,
or extra objects. This image is a geometry/camera reference, not a final style render.
```

### Style prompt

```text
Using the approved construction master, render [SUBJECT] in [STYLE_ANCHOR]
with [PALETTE], [EDGE_RULE], and [DETAIL_BUDGET]. Preserve the exact
silhouette, view, crop, anchor, and visible feature locations. Keep the
background separate and omit [MUST_NOT_BAKE]. Do not generate text, logos,
numbers, or UI labels.
```

### Pixel/post-process prompt

```text
Convert the approved style render to [LOGICAL_SIZE] pixel art on a [GRID]
grid. Use nearest-neighbor construction, hard edges, the declared palette,
and [DITHER_OR_DOT_RULE]. Remove anti-aliasing, blur, partial-alpha fringes,
and accidental colors. Preserve the silhouette and anchor at 1:1 logical pixels.
```

### Negative constraints

```text
no extra view, no camera drift, no altered wheelbase, no duplicate subject,
no cropped subject, no baked background, no perspective mismatch, no soft
shadow, no blur, no anti-aliasing, no gradient haze, no text, no logo, no watermark
```

## Review record

- `G0 authority/provenance`: pass/fail, owner, unresolved values, source/rights decision
- `G1 construction`: pass/fail, reviewer, rejected variants, reason
- `G1.5 calibration`: pass/fail, profile version, comparison board, reproducibility evidence
- `G2 style`: pass/fail, comparison asset, rejected variants, reason
- `G3 pixel`: pass/fail, validator output, target-size notes
- `G4 alpha/export`: pass/fail, dimensions, mode, fringe notes
- `G5 import`: pass/fail, engine screen/layer, pivot/filter notes
- `G6 runtime`: pass/fail, package/build evidence, remaining issues
