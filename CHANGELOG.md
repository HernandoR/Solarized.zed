# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.11.0] - 2026-07-02

### Changed

- Syntax highlighting is now differentiated directly by the theme. The `syntax`
  map grew from 38 to 107 fine-grained tree-sitter capture keys (classes,
  namespaces, enums, decorators, parameters, members, builtins, …), so rich
  highlighting works out of the box with no `settings.json` and no language
  server. Differentiation is hue-first across the eight Solarized accents plus a
  derived muted red (`#b45c4f`) for classes/types and namespaces; plain locals
  fall to body text. Bold/italic are minimized: bold on named constants and enum
  variants, italic on interfaces (comments and Markdown emphasis/strong keep
  their conventional styling). See ADR-0004.
- `recommended-settings.json` is now optional and trimmed to what tree-sitter
  cannot express: it enables `semantic_tokens` (previously missing, so the rules
  never fired) and dims `@deprecated` symbols. README reframed accordingly.
- Cleaner, more legible palette (ADR-0005). The editor previously read as
  grayish/dark; two eye-tunable knobs push it off canonical Solarized while
  holding every hue: the body foreground (editor text + plain variables) is set
  to a clean near-neutral instead of the muddy teal-gray base0 (dark `#b2b7b8`,
  light `#595f62`) so frequent identifiers read clean-white rather than gray;
  comments/emphasized tones are lifted `TEXT_CONTRAST_LIFT` (8 L\*) away from the
  background; and the eight accents are vivified — `ACCENT_CHROMA_BOOST` (×1.50, at the sRGB
  gamut ceiling) and `ACCENT_LIGHT_LIFT` (8 L\*, directional). E.g. dark blue
  `#268bd2 → #00a2f6`, cyan `#2aa198 → #00baaf`. Set the boosts to 1.0/0 to
  restore canonical. Surface ladder unchanged.

## [0.10.0] - 2026-06-26

### Changed

- Surface shades are now computed from a CIELAB lightness ladder instead of
  seven hand-tuned intermediate hex values, so the chrome no longer looks
  fragmented and every surface-to-surface contrast step is uniform. Editor and
  current-line stay canonical base03/base02; panels/inputs/tabs/focus are
  derived on a held chroma. The light variant gains a matching surface hierarchy
  and a warm-cream base (not stark white). See ADR-0003 (Proposed).

### Added

- Project is now managed with `uv` (`pyproject.toml`, `uv.lock`); `make` runs
  `uv run python solarized.py`. Runtime dependency: `coloraide` for color math.

## [0.9.0] - 2026-06-26

### Changed

- Inlay hint background is now a semi-transparent `fg3` tint instead of opaque
  `bg2`, so the chip stays distinguishable over every line background —
  including the active line (which is `bg2`) and selections

## [0.8.0] - 2026-06-26

### Fixed

- Inlay hint background now works again with `inlay_hints.show_background`. Zed
  reads the inlay hint background from `syntax.hint.background_color` (not the
  top-level `hint.background`), which was unset; added it (`bg2`)

## [0.7.0] - 2026-06-26

### Fixed

- Inlay hints are now muted gray and regular weight instead of bold light-blue.
  `syntax.hint` drove the bold/blue look (Zed styles inlay hints via the syntax
  `hint` key); set it to `fg2` with no `font_weight`

## [0.6.0] - 2026-06-26

### Fixed

- Ghost icon buttons (tabs, toolbars, panel headers) no longer float a filled
  box over their surface at rest — `ghost_element.background` is now transparent
  so icons only show a tint on hover/press; `ghost_element.active` is corrected
  from a foreground gray to a blue tint. Filled controls (`element.*`) unchanged

## [0.5.0] - 2026-06-26

### Changed

- Brightened UI chrome text and icons (tab labels, file tree, panels, status
  bar) for higher contrast against the background; editor/code colors unchanged

## [0.2.0] - 2025-06-26

### Added

- This changelog

### Changed

- Recolored predictions to be more subtle

### Fixed

- Fixed [Colors in minimap are hidden by scrollbar #1](https://github.com/harmtemolder/Solarized.zed/issues/1)

## [0.1.0] - 2025-03-11

### Changed

- Updated to match [schema v0.2.0](https://zed.dev/schema/themes/v0.2.0.json)

## [0.0.1] - 2025-03-11

- Forked from Carlo Caione's [NeoSolarized.zed](https://github.com/carlocaione/NeoSolarized.zed)
- Adapted to closer match [the original palette](https://ethanschoonover.com/solarized/), especially for syntax highlighting
- Added a Python script that generates the theme JSON

[0.2.0]: https://github.com/harmtemolder/Solarized.zed/releases/tag/0.2.0
[0.1.0]: https://github.com/harmtemolder/Solarized.zed/releases/tag/0.1.0
[0.0.1]: https://github.com/harmtemolder/Solarized.zed/releases/tag/0.0.1
[Unreleased]: https://github.com/harmtemolder/Solarized.zed
