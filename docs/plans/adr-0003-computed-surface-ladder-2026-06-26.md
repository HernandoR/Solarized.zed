# ADR-0003: Compute UI Surface Shades from a CIELAB Lightness Ladder

- Status: Proposed
- Date: 2026-06-26

## Context

[ADR-0001](adr-0001-adopt-vscode-export-2026-06-13.md) introduced seven
hand-tuned intermediate background hex values (`bg0`, `bg_input`, `bg_tab`,
`bg_focus`, `bg_sel`, `bg_title`, `bg_tab_active`). In use this read as
**"fragmented" (太碎)**: many near-identical surface tones at irregular CIELAB
lightness (≈ L\* 10.8 / 15.3 / 15.8 / 20.9 / 24.3 / 34.6) with hand-pushed,
inconsistent chroma. The complaint was never about hue — the syntax/accent
colors are fine — but about too many ad-hoc shades whose relationships were not
consistent.

The guiding insight: canonical Solarized is itself a **lightness ladder** —
Ethan Schoonover defined the eight monotones at fixed CIELAB L\* stops sharing a
hue family. So instead of hardcoding intermediate surfaces, they can be
*computed* by stepping lightness on a held chroma, which makes every
surface-to-surface contrast step uniform — directly satisfying the goal of
keeping colour relationships consistent.

This is a follow-on to ADR-0001 (its syntax/hue mapping stands; its surface-shade
hardcoding is replaced) and supersedes the earlier reverted two-tone attempt.

## Decision

> In the context of fragmented, hand-tuned surface shades with inconsistent
> relationships,
> facing the choice between more hand-picked hex values and a computed colour
> system,
> we decided to derive intermediate UI surfaces by CIELAB lightness on a held
> chroma — one uniform ladder per variant — keeping only the canonical anchors
> and the eight accents hardcoded,
> and against keeping ad-hoc intermediates or collapsing to a flat two-tone,
> to achieve consistent contrast steps and a recognizably-Solarized chrome with
> minimal hardcoding,
> accepting a runtime dependency on a colour library and that derived surfaces
> read more uniformly teal/cream than the previous hand-saturated shades.

Concretely, in `solarized.py` (now run under `uv`, with `coloraide`):

1. **Anchors only** are hardcoded: the canonical 16 Solarized colours (8
   monotones + 8 accents). The monotones serve as terminal ANSI colours, the
   editor/highlight surfaces, and the ramp anchors.

2. **`warm()`** nudges a colour's CIELAB b\* by `LIGHT_WARM = 3.0`. The light
   variant's editor (`base3`) and highlight (`base2`) are warmed so the base
   reads as warm cream (`#fff6dd`), not stark white — `+3` keeps every tone
   inside sRGB.

3. **`surface_shades(variant)`** derives the three intermediate surface roles —
   `recede` (panels, status bar, popovers), `field` (inputs, tab bar, inactive
   tabs), `emphasis` (active/focused item) — by holding the variant's background
   chroma and setting CIELAB lightness from a uniform grid:
   - dark: recede 10, (canvas 15, highlight 20 = canonical base03/base02), field 25, emphasis 32
   - light: (canvas 97, highlight ≈92 = warmed base3/base2), recede 91, field 88, emphasis 82

4. **Canvas and highlight stay canonical** (dark `base03`/`base02`; light warmed
   `base3`/`base2`) so the two most-visible surfaces are exact; only the three
   intermediates are computed.

5. **Tabs / title bar:** active tab and title bar = canvas (`bg1`); inactive
   tabs and tab bar = `field`.

6. **Tooling:** the project is now a `uv` project (`pyproject.toml`, `uv.lock`);
   `make` runs `uv run python solarized.py`; `coloraide` is the one runtime
   dependency.

**Status is `proposed`:** the lightness grid, `LIGHT_WARM`, and per-surface role
assignments are expected to be tuned by eye in Zed before this is accepted.

## Consequences

### Positive
- Surface contrast steps are uniform (equal CIELAB lightness deltas), so the
  chrome no longer looks fragmented.
- Hardcoding drops to the canonical 16 + a handful of lightness numbers; new
  surface tones are a one-line lightness target, not a hand-mixed hex.
- The same engine drives light, which now has a real surface hierarchy (it
  previously fell back to a single tone) and a warm-cream base.
- Tuning is now parametric: change one `LIGHT_WARM` or one L\* value.

### Negative / Risks
- Adds a runtime dependency (`coloraide`) and a `uv` environment to build.
- Derived surfaces are more uniformly teal (dark) / cream (light) than the old
  hand-saturated intermediates; this is a visible change pending sign-off.
- Holding chroma means surfaces don't reproduce Solarized's natural toward-mid
  desaturation; chosen deliberately for consistency, but is a departure from a
  strictly canonical monotone ramp.
- `LIGHT_WARM` is capped near +3 b\* before tones leave sRGB; more cream than
  that needs gamut mapping and may shift hue.
