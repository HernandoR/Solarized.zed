# ADR-0002: Tune UI Chrome Contrast and Ghost-Element Backgrounds

- Status: Accepted
- Date: 2026-06-26

## Context

Solarized is intentionally low-contrast: its dark foreground shades (base01
`#586e75`, base0 `#839496`, base1 `#93a1a1`) sit close to the dark backgrounds
(base03 `#002b36` and the VSCode-adopted darker surfaces — see
[ADR-0001](adr-0001-adopt-vscode-export-2026-06-13.md)). This is pleasant for
*code*, where syntax color carries most of the signal, but it makes the
editor's **UI chrome** — tab labels, file-tree entries, panel and status-bar
text, and their accompanying icons — hard to read. The user reported these
labels looking "grayish" and washed out against the background.

`solarized.py` is the single source of truth (`themes/solarized.json` is a
generated artifact). UI chrome and editor content are driven by *different*
theme keys: chrome uses `text.*` / `icon.*`, while editor code uses
`editor.foreground` and the `syntax` block. This separation means chrome
readability can be tuned without touching code colors.

Two distinct problems surfaced:

1. **Low chrome text/icon contrast.** Primary chrome used `fg1` (base0) and
   secondary/muted chrome used `fg2` (base01) — the darkest foreground shade,
   the main source of the washed-out look.

2. **Ghost icon buttons floated a filled box.** Icon buttons in tabs,
   toolbars, and panel headers are *ghost elements* in Zed's model — they
   should be transparent at rest and only tint on hover/press. But
   `ghost_element.background` was an opaque fill (`#003847`, the VSCode-adopted
   input shade) that sat *lighter* than the surfaces it appeared on (panel
   `#00212b`, editor/toolbar `#002b36`, status bar `#00212b`), so every icon
   looked like it carried its own box even when not hovered. Additionally,
   `ghost_element.active` was set to a *foreground* gray (`fg1`), which flashed
   a light box on press.

## Decision

### Decision 1 — Brighten UI chrome text and icons one notch

> In the context of UI chrome being hard to read against Solarized's dark
> surfaces,
> facing the choice between leaving it at the canonical low-contrast shades or
> increasing contrast,
> we decided to lift chrome text and icons one notch within the existing
> palette — primary `text` / `icon` from `fg1` to `fg3` (the "emphasized"
> shade), and `text.muted` / `text.placeholder` / `icon.muted` /
> `icon.placeholder` from `fg2` to `fg1`,
> and against introducing brighter non-Solarized colors or touching editor
> content keys,
> to achieve a clearly more legible UI without leaving the Solarized palette,
> accepting that the chrome is now slightly less "vanilla Solarized" and that
> `*.disabled` stays at `fg2` to preserve the dimmed-disabled semantic.

This works symmetrically in both variants because `fg3` is the "emphasized
content" shade in each: in dark it is brighter than `fg1` (base1 vs base0); in
light it is darker than `fg1` (base01 vs base00) — both directions *increase*
contrast against their respective backgrounds.

### Decision 2 — Make ghost elements transparent at rest

> In the context of ghost icon buttons floating an opaque box over the surfaces
> they sit on,
> facing the choice between picking a background color that matches a surface or
> making the resting state transparent,
> we decided to set `ghost_element.background` (and `ghost_element.disabled`) to
> fully transparent and correct `ghost_element.active` from a foreground gray to
> a blue tint (`blue` + `99`, one step stronger than the `66` hover/selected
> tint),
> and against assigning any opaque color,
> to achieve icons that blend into whatever surface they occupy and only tint on
> interaction — the intended "ghost" semantics,
> accepting that a single global background value cannot match the multiple
> surfaces (panel, tab bar, toolbar, title bar) where ghost buttons appear, so
> transparency is the only value that is correct everywhere.

Filled controls — inputs, the activity bar, dropdowns — use the separate
`element.*` keys and are deliberately left opaque (`element.background`
`#003847`), so they keep their fill.

## Consequences

### Positive
- UI chrome (tabs, file tree, panels, status bar) is noticeably more legible.
- Ghost icon buttons no longer carry a visible box at rest; hover/press
  feedback is now the only background signal, matching Zed's design intent.
- Both changes are confined to chrome keys; editor code colors are untouched.
- Changes stay within the Solarized palette (Decision 1) or use transparency
  (Decision 2) — no new ad-hoc colors introduced.

### Negative
- The chrome reads slightly less like canonical low-contrast Solarized.
- The brightest available chrome text is base1 (`#93a1a1`); anyone wanting
  *more* contrast than that would have to step outside the Solarized palette.

### Risks
- `element.background` and `ghost_element.background` were both `#003847`, so it
  is not possible to tell from color alone whether a given on-screen box is a
  ghost element or a filled `element`. Decision 2 targets ghosts; if a stray box
  remains in Zed after reload, it is an `element.*`-styled control and needs a
  separate decision. **This requires visual confirmation in Zed.**
- Decision 1's muted bump (`fg2` → `fg1`) reduces the visual gap between primary
  and muted chrome text; if they become too similar in practice, the muted shade
  may need its own intermediate value.
