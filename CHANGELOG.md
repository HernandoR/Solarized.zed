# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
