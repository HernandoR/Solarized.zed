# [Solarized](https://ethanschoonover.com/solarized/) for [Zed](https://zed.dev/)

> ☯️ Precision colors for machines and people

This is a fork of [harmtemolder/Solarized.zed](https://github.com/harmtemolder/Solarized.zed)
that fine-tunes the color system and expands the thematic (semantic) token
setup so highlighting can follow your LSP more closely — see
[Color & theme adjustments](#color--theme-adjustments) below.

## Issues

If you have any issues, no matter how small, please open an issue on
[GitHub](https://github.com/HernandoR/Solarized.zed/issues).

## Color & theme adjustments

This fork diverges from upstream in two main ways:

- **Refined color system.** The UI surface shades are computed from a CIELAB
  lightness ladder rather than a set of hand-tuned intermediate hex values, so
  the chrome reads as one uniform hierarchy instead of looking fragmented. The
  editor and current line stay canonical `base03`/`base02`, while panels,
  inputs, tabs and focus rings are derived on a held chroma; the light variant
  gains a matching surface hierarchy on a warm-cream base. See
  [`docs/plans/`](docs/plans/) for the ADRs behind these changes.
- **Expanded thematic token setup.** [`recommended-settings.json`](recommended-settings.json)
  maps LSP semantic token types (classes, namespaces, enums, decorators,
  parameters, properties, deprecated symbols, etc.) onto the Solarized syntax
  palette, so applying the recommended config gives you richer, more flexible
  highlighting that tracks the language server rather than tree-sitter alone.

## Recommended settings

For best results with LSP semantic tokens (class names, namespaces, decorators,
etc.), copy the relevant section from
[`recommended-settings.json`](recommended-settings.json) into your
`~/.config/zed/settings.json`.

## Develop

- (I used `schema.py` to generate a list of properties from `schema.json`, but as long as <https://zed.dev/schema/themes/v0.2.0.json> is used in `solarized.py`, you don't have to repeat this)
  - Note that `accents`, `players` and `syntax` should be a `list`, `list` and `dict` respectively
- This is a [`uv`](https://docs.astral.sh/uv/) project; run `uv sync` once to set up the environment (it pulls in `coloraide`, used to compute surface shades — see `docs/plans/adr-0003-computed-surface-ladder-2026-06-26.md`)
- Make changes to `solarized.py` as you see fit
- Then run it with `make` (which runs `uv run python solarized.py`) to generate `themes/leo-solarized-theme.jsonc`
- Don't forget to increment the version number in `extension.toml` before committing
- Then update [the `extensions` repo](https://github.com/zed-industries/extensions) (see [docs](https://zed.dev/docs/extensions/developing-extensions#updating-an-extension))
  - Fork the `extensions` repo
  - `cd extensions/extensions/leo-solarized-theme`
  - `git fetch`
  - `git pull`
  - Update the version number in `extensions/extensions.toml`
  - `git add`, `commit` and `push`
  - Then open a pull request

## Credits & upstream

- Based on [Ethan Schoonover's Solarized color palette](https://ethanschoonover.com/solarized/)
- Forked from [harmtemolder/Solarized.zed](https://github.com/harmtemolder/Solarized.zed),
  which is itself based on Carlo Caione's
  [NeoSolarized.zed](https://github.com/carlocaione/NeoSolarized.zed). Many thanks
  to the upstream authors for the foundation this builds on.
- This fork was created **before** upstream adopted its GNU license. Because the
  code adopted here predates that relicensing, this fork is distributed under the
  MIT license (see [License](#license)).

## License

Released under the [MIT License](LICENSE).
