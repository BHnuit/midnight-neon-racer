# Style Calibration Template

Run this after G1 approves one construction master and before G2 production. Use it to select a reproducible recipe for one asset family; do not use the bake-off candidates as runtime assets.

## Fixed inputs

- `asset_family`: vehicle / traffic / background / UI / FX / other
- `construction_master_id` and hash
- `mask_or_control_inputs` and hashes
- `style_anchor_id`
- `review_canvas`, crop, subject bounds, and anchor
- `palette_target` and authority
- `target_display_size`
- `evaluation_criteria`

## Candidate matrix

Keep fixed inputs unchanged. Record one row per candidate:

| candidate | provider/model version | prompt template/version | language | control type/weight | strength/denoise | seed policy | post-process | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `c01` | TBD | TBD | TBD | TBD | TBD | TBD | TBD | pending |

Four to eight candidates is a practical initial range, not a mandatory count. Change one variable at a time when the goal is to identify why results differ. Use a separate profile when an asset family genuinely requires a different model or workflow.

Do not invent numeric values for labels such as `low`, `high`, `soft`, or `strong`. Record them as `TBD-low` / `TBD-high` until an approved model profile, official tool documentation, or a human decision supplies native values. Similarly named controls may have different ranges and meanings across models; never normalize or compare their numbers without an accepted mapping. Keep non-tested native settings fixed within each model and record them explicitly.

## Comparison board

Render all candidates with identical labels and backgrounds at:

1. 1:1 working pixels.
2. Exact target display size.
3. Grayscale, when checking value grouping and silhouette.

Score observable properties rather than general preference:

- camera and silhouette preservation
- feature/identity consistency
- palette and value grouping
- outline and edge behavior
- detail density at minimum readable size
- material and lighting language
- pixel/dither compatibility
- absence of baked text, UI, background, FX, and watermark
- reproducibility from the recorded recipe

Apply hard rejection rules before optional scoring. If weights are useful, record them as a proposed rubric and obtain G1.5 approval before using the weighted total to select a recipe.

Test prompt language as a matrix variable. Keep whichever language/template works for the selected model and asset family; do not assume one language is universally more stable.

## Approved style profile

Record the selected recipe:

```json
{
  "id": "style-profile/asset-family-v01",
  "status": "draft",
  "asset_family": null,
  "approved_candidate": null,
  "approved_anchor": null,
  "construction_master_hash": null,
  "provider": null,
  "model_version": null,
  "workflow_or_config_hash": null,
  "prompt_template_version": null,
  "prompt_language": null,
  "control": {
    "type": null,
    "weight": null
  },
  "parameter_authority": null,
  "cross_model_parameter_mapping": null,
  "strength_or_denoise": null,
  "seed_policy": null,
  "palette_and_color_budget": null,
  "outline_rule": null,
  "detail_density": null,
  "lighting_and_material_rule": null,
  "dither_rule": null,
  "negative_constraints": [],
  "post_process_recipe": null,
  "comparison_board": null,
  "reviewer": null,
  "approved_at": null
}
```

Set `status` to `approved` only after another run can reproduce the chosen visual direction from the saved inputs and recipe. Re-run G1.5 when a material profile field changes; do not hide a recipe change inside an asset revision.
