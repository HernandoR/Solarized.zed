# ADR-0004: Theme-Native Syntax Differentiation over LSP Semantic-Token Rules

- Status: Accepted
- Date: 2026-07-02

## Context

The fork advertised (README, `recommended-settings.json`) an "expanded thematic
token setup": ~30 `global_lsp_settings.semantic_token_rules` mapping LSP semantic
token *types* (class, namespace, enum, decorator, parameter, property, …) onto a
handful of theme syntax keys, so highlighting could "track the language server."

Reviewing this against how Zed actually resolves colour surfaced three problems:

1. **Two layers, and we were leaning on the wrong one.** Zed highlights in two
   independent passes: **tree-sitter captures** → the theme's `syntax` map
   (always on, no LSP, no user settings), and **LSP semantic tokens** →
   `semantic_token_rules` (an *opt-in overlay*). The overlay only fires when the
   user (a) copies the config into `settings.json`, (b) sets
   `"semantic_tokens": "combined"` (or `"full"`), **and** (c) is editing a file
   whose language server actually emits semantic tokens. The always-on
   tree-sitter layer needs none of that.

2. **The recommended config was effectively dead.** `recommended-settings.json`
   defined `semantic_token_rules` but **never set `semantic_tokens`**, which is
   not enabled by default — so for most users the rules did nothing at all.

3. **Even when it fired, it barely differentiated.** The theme declared only 38
   syntax keys, many collapsed onto one accent (blue = function / constructor /
   variable / property / tag / label / variant; orange = type / enum / preproc /
   string.special). The LSP rules mapped six semantic types back onto those same
   collapsed keys, so class / namespace / interface / struct / type all rendered
   identically anyway.

The sibling project **Ayu-in-Zed** solves the same problem the other way: it
declares ~104 fine-grained tree-sitter capture keys (`keyword.return`,
`type.builtin`, `variable.member`, `function.method`, `variable.parameter`,
`constant.builtin`, …) directly in the theme and ships **no** settings at all.
The differentiation the user wants is available for free on the always-on layer.

This is a follow-on to [ADR-0001](adr-0001-adopt-vscode-export-2026-06-13.md):
its palette/hue mapping stands; this ADR expands *which* token classes are
mapped and moves the differentiation off the LSP overlay.

## Decision

> In the context of wanting syntax token classes to be visibly distinguishable,
> facing the choice between enriching the LSP `semantic_token_rules` overlay or
> enriching the always-on tree-sitter `syntax` map,
> we decided to **expand the theme's `syntax` map to a fine-grained tree-sitter
> capture set and differentiate primarily by hue across the eight Solarized
> accents (plus one derived muted red for classes/namespaces)**, and to reduce
> `semantic_token_rules` to only what tree-sitter genuinely cannot express,
> and against replicating Ayu's liberal bold/italic or keeping the coarse
> 38-key map behind an opt-in LSP overlay,
> to achieve rich, config-free, LSP-independent highlighting that still reads as
> canonical, low-decoration Solarized,
> accepting that eight accents cannot give every one of ~100 token classes a
> unique colour (deliberate family sharing), and that a few LSP-only niceties
> (deprecated dimming) now require the user to opt in.

### 1. Differentiation is hue-first (all eight accents)

Token families map to Solarized accents by role. Where two families must differ
but share a natural accent, they are pushed onto an under-used accent rather than
onto a weight/italic variation. One accent is *derived*, not canonical:
`red_muted` = Solarized `red` with ~45% of its chroma removed (a dusty brick-red,
`#b45c4f`), so classes/namespaces read as a calm red family while vivid `red`
stays reserved for errors and diff-minus.

| Accent | Role / families |
|---|---|
| **green** | keywords (all `keyword.*`), operators, CSS selector, `tag.doctype`, `diff.plus` |
| **blue** | functions / methods / constructors / calls, `tag`, `selector.pseudo`, `string.special.url`, `link_text` |
| **red_muted** *(derived)* | **classes / types** (`type`, `type.definition`, `type.class.definition`, `type.super`), **interfaces** (`type.interface`, `interface`; italic), **namespaces / modules / concepts** |
| **orange** | `enum`, preproc / macros / directives, `string.escape` / `.regex` / `.special`, `punctuation.list_marker`, `title` |
| **cyan** | strings, object members / `property` / `field`, `function.builtin`, characters, `text.literal`, `tag.attribute` |
| **magenta** | numbers, **named constants (bold)**, **enum variants (bold)** |
| **yellow** | booleans, `constant.builtin` (bold), `type.builtin`, |
| **violet** | parameters, decorators / `attribute`, labels, symbols, `link_uri`, `punctuation.special`, `variable.builtin`/`.special` |
| **red** (vivid) | `comment.error`, `diff.minus` |
| **fg1** (body) | plain `variable`, `text`, `primary`, `embedded` |
| **fg2** (muted) | comments, ordinary punctuation, `tag.delimiter` |

Key consequences: **classes/types & namespaces share the muted red** (with
builtin types kept on yellow and enums on orange so they stay distinguishable
from user classes); **plain local variables render as body text**, so the
coloured accents mark only semantically meaningful tokens (a call site pops blue;
a member access pops cyan; a class reads muted-red; a local recedes).

### 2. Bold and italic are minimized to carry specific meaning

Not used as a general differentiation axis. Only:

- **Bold (700)** — *named immutable values*: `constant`, `constant.builtin`,
  `constant.macro`, `variant` (enum variants). Nothing else in code is bold.
- **Italic** — *interfaces*: `type.interface`, `interface`. Nothing else in code
  is italic.

Pre-existing **semantic markup / convention** uses are kept, because there the
bold/italic *is* the meaning, not decoration: `comment*` italic (canonical
Solarized), Markdown `emphasis` italic + `emphasis.strong` bold, `title` bold,
`link_text` italic. (The coloured comment sub-types `comment.todo/note/info/
hint/warning/error` are hue-differentiated but stay italic like all comments.)

### 3. `recommended-settings.json` trimmed to semantic-only, and fixed

- Reduced to the rules tree-sitter *cannot* express — the `deprecated` modifier
  (dimmed foreground). Optional `mutable`/`readonly` may be added later.
- Adds the previously-missing `"semantic_tokens": "combined"` so the remaining
  rules actually fire.
- README reframes it as an **optional** power-user enhancement, not the primary
  mechanism; the theme is self-sufficient without any settings.

### Known limitations

- Enum-variant bolding keys off the `@variant` capture. Grammars that tag
  variants as `@constructor` (some Rust queries) will render them plain blue, not
  bold magenta; revisit per-grammar if it matters.
- Members/properties share **cyan** with strings; quoting disambiguates them in
  practice.

## Consequences

### Positive
- Rich, differentiated highlighting **out of the box** — no `settings.json`, no
  LSP dependency, works in every file including ones with no language server.
- The differentiation is real: ~100 capture keys spread across eight accents,
  where before six semantic types collapsed onto two.
- Honest configuration story: the shipped recommended settings now actually work,
  and only claim the narrow thing (deprecated dimming) they uniquely provide.
- Stays recognizably Solarized — hue-first, low decoration; bold/italic mean
  something rather than being sprinkled.

### Negative / Risks
- Eight accents cannot uniquely colour ~100 classes; family sharing is
  deliberate but means, e.g., strings and members are both cyan.
- Moving `variable` to plain body text and `constant` to bold magenta is a
  visible change from the previous all-blue treatment; pending eye-tuning in Zed.
- Some intended distinctions depend on the grammar's capture choices (see
  limitations), so results vary by language.
