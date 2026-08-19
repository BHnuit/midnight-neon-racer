---
name: ai-game-art-pipeline
description: "Plan and execute an AI-assisted game-art asset pipeline from real-world or visual references to engine-ready sprites, layers, UI, effects, and backgrounds. Use when an asset needs controlled camera angle, silhouette, scale, placement, model/prompt calibration, style transfer, pixel or dot-matrix treatment, background removal, alpha/format conversion, sprite-sheet export, manifest metadata, or game-engine import; also use when reviewing AI-generated art for consistency, provenance, reproducibility, and runtime readiness."
---

# AI Game Art Pipeline

Treat image generation as a controlled asset-production pipeline, not a one-shot prompt. Preserve gameplay-readable geometry first, apply the project's art direction second, enforce pixel and file constraints third, then export and validate the exact runtime artifact.

## Load Context First

Read only the sources relevant to the requested asset, in this order:

1. Project brief, art bible, target screen/layer contract, and engine architecture.
2. Existing approved anchor assets and their manifests.
3. [`references/asset-brief-template.md`](references/asset-brief-template.md), [`references/style-calibration-template.md`](references/style-calibration-template.md), and [`references/asset-manifest-template.json`](references/asset-manifest-template.json).
4. [`docs/ai-game-art-pipeline-research.md`](../../../docs/ai-game-art-pipeline-research.md) when the task needs the research rationale or source links.
5. Existing specialist skills only when their scope matches: `mayonaka-art` for this project's art direction, `pixel-asset-master` for strict pixel generation/post-processing, `imagegen` for raster generation/editing, and `tait-crt-interface-skill` for menu CRT artwork. Do not invoke every art skill by default.

If a referenced project document is missing, stop and report the missing contract before generating a batch.

Resolve every production value by this authority order:

1. Exact accepted asset/screen specification.
2. Approved asset-family manifest or anchor.
3. Project art bible and runtime architecture.
4. Tool defaults and general workflow guidance.

Never let a lower source override a higher one. Mark an unresolved value as `TBD` with its decision owner and blocking gate; do not turn an example, safe frame, tool default, or convenient integer scale into a production contract.

## Pipeline

Run the stages serially. Each stage produces an artifact that becomes the next stage's input. Do not batch across an unresolved human gate.

### 0. Intake, scope, and provenance

- Classify the asset: player/traffic sprite, title view, background layer, tile, UI, effect, weather, or animation.
- Classify both the asset itself and its containing surface. A vehicle shown inside a CRT menu remains a vehicle asset unless the art bible explicitly assigns the menu palette/effects to the vehicle.
- Record the intended screen, layer/pass, runtime size, animation frames, anchor/pivot, collision silhouette, and minimum readable size. Keep the container frame, subject safe bounds, source canvas, logical pixel canvas, and runtime PNG size as separate fields.
- Record every external reference's source, license or permission status, URL, and what is being observed. Do not copy a reference image into the game or claim its license from appearance alone.
- Decide whether the reference may be used for geometry, palette, lighting, material, or general mood. Keep those roles separate.
- Do not start generation until the asset brief is complete enough to reject a bad result.

**Gate G0:** approve scope, authority references, provenance, and all values that would change asset count, camera, dimensions, palette, layer ownership, or runtime behavior. Leave the rest `TBD`; do not infer it.

### 1. Lock the construction master

Use a photo, turnaround, line drawing, 3D blockout, or other suitable reference to establish the thing's **camera and geometry**, before style.

- Generate or edit a neutral construction sheet with the requested view(s): front, rear, side, three-quarter, top, or orthographic. Prefer a reference-controlled edit or a 3D/blockout render when exact perspective, scale, or placement matters.
- State the camera, horizon/vanishing point, object bounding box, bottom/center anchor, visible faces, and negative space in pixels or normalized coordinates.
- Keep the subject on a plain contrasting background or a separate mask. Do not bake UI, text, HUD, road markings, glow, shadows, or other layers that the runtime must control.
- Create a small candidate set only for exploration. Select one anchor, then freeze the camera, crop, aspect ratio, and reference before style work.
- For multiple views, validate silhouette, wheelbase/proportions, feature placement, and scale across the sheet. A style-consistent but geometrically inconsistent set is a failure.

**Gate G1:** approve the construction master and its mask/anchor. If the angle, size, placement, or silhouette is wrong, return to this stage; do not fix geometry with style prompts.

### 1.5 Calibrate the production recipe

Use one approved construction master to determine how this asset family will be rendered. Treat this as a controlled bake-off, not as production.

- Keep geometry, crop, review size, palette target, and evaluation board fixed. Change only declared variables such as provider/model version, prompt-template version, prompt language, control type/weight, denoise or style strength, seed policy, and post-process settings.
- Resolve every numeric generation parameter from an approved tool profile, official model documentation, or a human decision. If a request says only “low/high,” record `TBD-low` and `TBD-high`; do not invent weights, steps, CFG, denoise, or a normalization formula.
- Do not assume similarly named parameters are numerically comparable across providers or model families. Pin all non-tested settings within each model, record native values, and compare outputs against shared visual criteria. Normalize parameters only when an accepted calibration method explicitly defines the mapping.
- Keep the matrix small enough to compare. Four to eight candidates is a practical starting range, not a project contract. Change one variable at a time when diagnosing a difference.
- Compare all candidates in one board at identical 1:1 and target-display sizes, plus grayscale when value grouping matters. Do not evaluate candidates in separate viewers or at different zoom levels.
- Use hard pass/fail gates first. Treat any weighted scoring formula as a proposal requiring G1.5 approval; do not invent authoritative weights inside the execution run.
- Test Chinese and English prompts empirically for the selected model. Do not encode “English is always better” or any other provider-specific observation as a universal rule.
- Select one recipe and record it as a versioned `style-profile`: approved anchor, provider/model version, prompt template/language, control workflow and weights, palette/color budget, outline rule, detail density, lighting/material simplification, dither rule, negative constraints, post-process recipe, and reviewer evidence.
- Allow different asset families to use different models or recipes when justified, but require every profile to satisfy the same project art bible and runtime output contract.
- Re-enter this calibration stage whenever the model version, prompt template, control workflow, palette policy, or material/detail language changes materially.

**Gate G1.5:** approve one reproducible style profile and its comparison board. Do not batch an asset family while the profile is missing, ambiguous, or only reproducible from an unrecorded chat.

### 2. Apply the project's style

Use the approved construction master and G1.5 style profile as the structural and rendering conditions for image-to-image, reference-guided generation, or manual paint-over.

- Specify style using observable rules: edge hardness, line treatment, value grouping, palette roles, material simplification, lighting direction, detail density, and allowed texture/dither.
- Preserve the construction silhouette, camera, crop, and anchor. Change rendering language, not the object identity or gameplay read.
- Use a single approved style anchor and a locked palette for a family of assets. Apply the recorded model/workflow settings, prompt template, seed policy, reference weight, and negative constraints; do not tune them silently per asset.
- Ask the model for shapes and materials, never for production text, Chinese characters, logos, numbers, or UI labels. Add text in the engine or a controlled font workflow.
- Keep menu CRT treatment separate from in-game flat pixel rendering when the art bible distinguishes them.

**Gate G2:** compare the production candidate against both the style anchor and the approved G1.5 profile at target display size and in grayscale. Reject accidental hue families, soft/anti-aliased edges, lost silhouette cues, baked background layers, unrecorded recipe drift, and style drift between views.

### 3. Convert to pixel or dot-matrix form

Treat pixelation as a deterministic finishing pass, not as a vague prompt adjective.

- Choose a logical working resolution and scale path from the asset brief. Downsample with nearest-neighbor or draw directly at the logical grid; upscale only with nearest-neighbor.
- Do not derive logical resolution from a display/safe frame unless the accepted spec explicitly defines that scale relationship. A 2 px base grid constrains coordinates, strokes, anchors, and output dimensions; it does not by itself mean that every asset is authored at half resolution and enlarged 2x.
- Quantize to the declared palette. Keep hard clusters, intentional ramps, and depth-aware dithering; remove anti-aliasing, blur, sub-pixel edges, and accidental gradient noise.
- Apply the palette for the asset's semantic class, not automatically the palette of its containing screen. Do not derive a maximum color count from the number of canonical palette swatches when same-hue ramps or an asset-family budget are separately allowed.
- Follow the project's grid rule (for this project, the shared base grid is 2 px) and preserve the declared silhouette after quantization.
- Make dot density respond to depth or material. Do not add uniform salt-and-pepper noise just to make an image look pixelated.
- Generate animation frames from the same locked spec. Check that anchors, palette, silhouette, and feature placement do not jump from frame to frame.

Use `pixel-asset-master`'s `palette_analyzer.py`, `asset_validator.py`, and `finalize_assets.py` when its project contract is active; do not silently replace a project's palette with a generic palette.

**Gate G3:** inspect the asset at 1:1 logical pixels and at the smallest in-game size. Reject unreadable silhouettes, broken grid alignment, palette violations, and frame-to-frame anchor drift.

### 4. Isolate and prepare the runtime image

- Create or refine a binary/graded mask according to the asset type. Remove background, halo, matte color, and fringe pixels; inspect high-contrast edges at 200% or higher.
- Use fully transparent or fully opaque alpha for standard sprites. Preserve partial alpha only for an explicitly approved glow, smoke, fog, or other effect layer.
- Keep runtime-controlled shadows, road contact, tail-light spill, particles, and CRT overlays in their own pass. Do not bake them into the subject sprite or background plate.
- Crop to the declared safe bounds without changing the semantic anchor. Store transparent padding and pivot explicitly; do not let an editor auto-crop move the vehicle or UI slot.
- Convert to the requested PNG mode/format and color profile. Use RGBA PNG for ordinary sprites unless the target engine contract explicitly calls for indexed PNG; never trade away alpha to reduce file size without checking the importer.

**Gate G4:** verify dimensions, aspect ratio, alpha behavior, transparent edges, color count/profile, and anchor metadata. A visually good image with a fringe or moved pivot is not ready.

### 5. Package, manifest, and import

- Name files by stable semantic IDs and versions, not by model prompts or dates alone. Keep source/construction/style/pixel masters outside the runtime import folder.
- Fill the manifest from [`references/asset-manifest-template.json`](references/asset-manifest-template.json). At minimum record `id`, `version`, source and runtime dimensions, anchor/pivot, pixel-grid check, atlas group, compositing pass, target screen/segment, minimum readable size, source/license, generator/model/workflow, seed or reproducibility note, and validation results.
- Keep `null`/`TBD` template values unresolved until an authoritative source supplies them. Never copy placeholder paths, sizes, pivots, color budgets, or validation commands into a real manifest.
- Keep references in the project's reference area and approved source assets in its contract asset area. Copy only explicitly approved runtime files into the formal engine project.
- For this project, do not hand-edit Cocos `.scene`, `.prefab`, `.anim`, or `.meta` files. Use the Cocos MCP/editor to import and configure assets, then let Creator generate metadata.
- Pack sprite sheets only after individual PNGs pass validation. Keep a machine-readable frame/anchor manifest beside the sheet.

**Gate G5:** import one representative asset into the real screen/layer first. Check filtering, scale, pivot, z-order, occlusion, batching/atlas behavior, and draw-call or memory impact before importing a family.

### 6. Runtime verification and handoff

- Capture the asset in its real screen and at target device scale. Verify silhouette, readability, alignment, layering, animation cadence, and interaction with collision/feedback rules.
- For Cocos/WeChat work, validate the Creator scene, export the package, then run the project's package preview/log workflow. A source PNG or editor screenshot is not evidence that the exported package is correct.
- Record failures as a new revision with the failed gate and reason. Do not overwrite the approved anchor to hide a regression.

**Gate G6:** only mark `approved` after both visual review and runtime/package verification pass.

## Tool Routing

Choose the smallest tool chain that satisfies the brief:

| Need | Route |
| --- | --- |
| New raster, edit, mask, or controlled variation | `imagegen` or the project's approved image tool |
| Project-specific cyber-pixel art direction | `mayonaka-art`; load the art bible first |
| Strict grid, palette, validation, finalization, sprite sheets | `pixel-asset-master` scripts |
| CRT menu/window treatment | `tait-crt-interface-skill`; keep it out of gameplay layers |
| Cocos asset import and serialized editor state | Cocos MCP/editor; never hand-edit serialized files |

If a tool cannot preserve camera or identity reliably, use a 3D/blockout or manual compositing step for construction and reserve AI for style/detail exploration.

## Project-Specific Guardrails

For `真夜中道路` / `midnightroad`:

- Treat `docs/art-bible.md`, `docs/art-bible-revision-01.md`, `docs/ui-art-production-spec.md`, `CONTEXT.md`, and the formal project's `docs/architecture.md` as the source of truth.
- Keep the contract repo's `assets/minigame/refs/`, `previews/`, `cars/`, and `layers/` roles distinct. References and previews never enter the package by implication.
- Preserve the locked 720×1280 design canvas, camera A, shared 2 px grid, separate layer stack, and car anchoring. Do not let a generation tool redraw a locked car into a background plate.
- Apply camera A only to the gameplay rear-view composition. Title three-quarter and selection side-view cars follow their own accepted screen specifications. Likewise, do not force a vehicle sprite to the five-color menu-chrome palette merely because it appears inside a menu window.
- Keep player/traffic sprites, road layers, FX back/front passes, and HUD separate so road theme, weather, nitro, feedback, and UI can change independently.
- Gate 6 was lifted 2026-08-19. Still run G0–G6 serially. Start with batch A0 (one title-screen TaiT style preview in `assets/minigame/previews/`). Do not batch an asset family before G1.5. Previews and signed TaiT masters never enter the WeChat package.

## Stop Conditions and Recovery

Stop and ask for a decision when a change would alter camera, silhouette, palette, art style, layer ownership, runtime dimensions, licensing status, or the amount of art in the accepted scope. Do not silently solve a contract conflict with a prompt.

When a result fails:

1. Identify the first failed gate (geometry, recipe calibration, style, pixel, alpha/export, import, or runtime).
2. Change only the variables owned by that gate.
3. Preserve the last approved upstream artifact and increment the version.
4. Re-run all downstream checks before calling the asset approved.

## Deliverables

For each asset family, hand off:

- Construction master and mask/reference record.
- Approved style profile, comparison board, and anchor link.
- Final individual PNG(s), and sprite sheet only when required.
- Manifest with provenance, reproducibility, dimensions, anchor, and validation evidence.
- A short review note listing unresolved visual issues, rejected variants, and the first runtime screen used for verification.

See [`references/asset-brief-template.md`](references/asset-brief-template.md) for the brief and prompt structure, [`references/style-calibration-template.md`](references/style-calibration-template.md) for the bake-off and style profile, [`references/asset-manifest-template.json`](references/asset-manifest-template.json) for metadata, and [`scripts/validate_asset.py`](scripts/validate_asset.py) for deterministic PNG checks.
