#!/usr/bin/env python

"""
Constructs themes/leo-solarized-theme.json (packaged) and .jsonc (reference)

Notes:
- Transparency is supported, just append to hex (e.g. `80` for 50%)
- More info:
  - https://zed.dev/docs/themes
  - https://zed.dev/docs/extensions/themes
  - https://zed.dev/schema/themes/v0.2.0.json

This script uses the VSCode export (solarized.jsonc) as the reference for
color values — see docs/plans/adr-0001-adopt-vscode-export-2026-06-13.md.
"""

import json

from coloraide import Color

solarized = {
    "base03": "#002b36",  # dark background
    "base02": "#073642",  # dark background highlights
    "base01": "#586e75",  # dark comments / secondary content; light optional emphasized content
    "base00": "#657b83",  # light body text / default code / primary content
    "base0": "#839496",  # dark body text / default code / primary content
    "base1": "#93a1a1",  # dark optional emphasized content; light comments / secondary content
    "base2": "#eee8d5",  # light background highlights
    "base3": "#fdf6e3",  # light background
    "yellow": "#b58900",
    "orange": "#cb4b16",
    "red": "#dc322f",
    "magenta": "#d33682",
    "violet": "#6c71c4",
    "blue": "#268bd2",
    "cyan": "#2aa198",
    "green": "#859900",
}

# Canonical accent hexes, captured before the per-variant accent transform
# (ADR-0005) overwrites the working `solarized` accents.
_ACCENT_NAMES = (
    "yellow",
    "orange",
    "red",
    "magenta",
    "violet",
    "blue",
    "cyan",
    "green",
)
_CANONICAL_ACCENTS = {n: solarized[n] for n in _ACCENT_NAMES}

# ---------------------------------------------------------------------------
# Derived surface shades (ADR-0003)
#
# ADR-0001 introduced seven hand-tuned intermediate background hex values, which
# made the chrome look "fragmented" (too many near-identical surface tones).
# They are replaced by a computed ladder: every background surface shares ONE
# chroma (the variant's background hue) and differs only in CIELAB lightness, on
# a uniform step grid — so the contrast between any two surfaces is consistent.
# The 8 accents are cleaned up (chroma/lightness) per ADR-0005 and the content
# tones lifted for legibility; only the background surfaces are canonical here.
# ---------------------------------------------------------------------------


def _lab(hex_color):
    c = Color(hex_color).convert("lab")
    return c["lightness"], c["a"], c["b"]


def _from_lab(lightness, a, b):
    return Color("lab", [lightness, a, b]).convert("srgb").to_string(hex=True)


def _lch(hex_color):
    c = Color(hex_color).convert("lch")
    return c["lightness"], c["chroma"], c["hue"]


def _from_lch(lightness, chroma, hue):
    # Negative chroma is meaningless; the darkest surface can ask for a chroma
    # the very-dark end of sRGB can't hold, so let coloraide gamut-map on output.
    c = Color("lch", [lightness, max(chroma, 0.0), hue])
    return c.convert("srgb").to_string(hex=True)


# ---------------------------------------------------------------------------
# Cleaner, crisper accents + a legibility lift (ADR-0005)
#
# Canonical Solarized accents are deliberately low-chroma and mid-lightness, which
# reads "灰灰的、暗暗的" (grayish/dark). We trade some canonical fidelity for
# legibility: boost every accent's LCh chroma and shift its lightness away from
# the background — brighter on dark, darker on light — holding hue. The same
# LIGHT_LIFT also lifts the comment/emphasized text tones (below). Set the boost
# to 1.0 and the lift to 0 to restore canonical.
# ---------------------------------------------------------------------------
ACCENT_CHROMA_BOOST = 1.30  # ×chroma applied to all 8 accents (both variants)
LIGHT_LIFT = 8.0  # CIELAB L* shift away from bg: + on dark / − on light


def apply_accents(light_lift):
    """Rebuild the 8 accents in `solarized` for one variant — boost chroma and
    shift lightness, holding hue — then derive `red_muted` for classes/types
    (ADR-0004) as the vivified red with ~35% of its chroma removed. Vivid `red`
    itself stays reserved for errors/diff."""
    for name in _ACCENT_NAMES:
        lightness, chroma, hue = _lch(_CANONICAL_ACCENTS[name])
        solarized[name] = _from_lch(lightness + light_lift, chroma * ACCENT_CHROMA_BOOST, hue)
    r_l, r_c, r_h = _lch(solarized["red"])
    solarized["red_muted"] = _from_lch(r_l, r_c * 0.65, r_h)


# Light backgrounds run a touch warmer (more b*/yellow) than canonical so the
# base reads as warm cream, not stark white. +3 keeps every tone inside sRGB.
LIGHT_WARM = 3.0


def warm(hex_color):
    """Nudge a color warmer (more b*) — used to cream up the light base tones."""
    lightness, a, b = _lab(hex_color)
    return _from_lab(lightness, a, b + LIGHT_WARM)


def lighten(hex_color, delta_l):
    """Shift a color's CIELAB lightness by delta_l (negative darkens), holding a*/b*.
    Used with ±LIGHT_LIFT to lift the comment/emphasized tones off the background."""
    lightness, a, b = _lab(hex_color)
    return _from_lab(lightness + delta_l, a, b)


# Body foreground (editor text + plain variables) is set to a CLEAN near-neutral
# rather than the muddy teal-gray base0/base00 (ADR-0005, "clean near-white").
# Variables are the most frequent token, so painting them an accent would make
# that accent dominate; instead we brighten the default text toward a crisp
# near-white (dark) / near-ink (light) and scale its tint toward neutral, letting
# the vivid accents carry the colour. Comments (fg2) and emphasized (fg3) keep
# their lifted teal tint so they stay distinct. Both knobs are eye-tunable.
BODY_L = {"dark": 74.0, "light": 40.0}  # target CIELAB lightness of body text


def clean_text(hex_color, target_l):
    """Crisp near-neutral body foreground (ADR-0005): set CIELAB lightness to
    target_l and scale a*/b* toward neutral (keep 30% of the tint), so default
    text reads clean-white/clean-ink instead of teal-gray."""
    _, a, b = _lab(hex_color)
    return _from_lab(target_l, a * 0.30, b * 0.30)


# The canvas (editor) and highlight (current line) keep the canonical base03/
# base02 (dark) and base3/base2 (light). Only the three intermediate surface
# roles are derived: each holds the variant's background HUE and steps CIELAB
# lightness on a uniform ladder bracketing the canvas.
#
# Chroma is NOT held flat. The first ADR-0003 cut pinned absolute a*/b* and only
# moved L*, which left the lighter surfaces (field/emphasis) 25–40% less colorful
# than canonical at their lightness — they read "灰灰的", washed-out gray-blue.
# Canonical Solarized (and the ADR-0001 hand-tuned ladder it replaced) instead
# let chroma *rise* as lightness moves toward mid-gray (base03 C*16 → base02 C*17,
# the hand ladder ~+0.5 C* per L*). So chroma is now a signed linear function of
# the lightness step from the canvas anchor, restoring that richness. The slope
# is eye-tunable; dark +0.5 reproduces the hand-tuned ladder, light a gentle −0.2
# so deeper surfaces read as richer cream rather than gray.
_SURFACE_ANCHOR = {"dark": "#002b36", "light": "#fdf6e3"}
_SURFACE_L = {
    "dark": {"recede": 10, "field": 25, "emphasis": 32},
    "light": {"recede": 91, "field": 88, "emphasis": 82},
}
_SURFACE_CHROMA_SLOPE = {"dark": 0.5, "light": -0.2}  # C* gained per L* off the anchor


def surface_shades(variant):
    """Derived intermediate surfaces: held hue, lightness ladder, chroma rising toward mid-gray."""
    anchor = _SURFACE_ANCHOR[variant]
    if variant == "light":
        anchor = warm(anchor)
    l0, c0, hue = _lch(anchor)
    slope = _SURFACE_CHROMA_SLOPE[variant]
    return {
        role: _from_lch(level, c0 + slope * (level - l0), hue)
        for role, level in _SURFACE_L[variant].items()
    }


def solarized_theme(palette):
    accents = [palette["blue"]]
    players = [
        {
            "background": palette[color],
            "cursor": palette[color],
            "selection": palette[color] + "66",
        }
        for color in [
            "blue",
            "cyan",
            "green",
            "magenta",
            "orange",
            "red",
            "violet",
            "yellow",
        ]
    ]
    # Syntax highlighting — see docs/plans/adr-0004-theme-native-syntax-
    # differentiation-2026-07-02.md. Differentiation is hue-first across all
    # eight Solarized accents (Zed maps these tree-sitter capture names directly,
    # always-on, with no LSP or user settings required). Bold/italic are
    # deliberately minimized: bold ONLY on named immutable values (constants and
    # enum variants), italic ONLY on interfaces — plus the pre-existing markup/
    # convention uses (comments, Markdown emphasis/strong/title, links) where the
    # style IS the meaning. Plain locals fall to body text so accents mark only
    # semantically meaningful tokens.
    syntax = {
        # --- Comments (muted; italic is the one kept Solarized convention) ---
        "comment": {"color": palette["fg2"], "font_style": "italic"},
        "comment.doc": {"color": palette["fg2"], "font_style": "italic"},
        "comment.documentation": {"color": palette["fg2"], "font_style": "italic"},
        "comment.todo": {"color": palette["yellow"], "font_style": "italic"},
        "comment.note": {"color": palette["blue"], "font_style": "italic"},
        "comment.info": {"color": palette["blue"], "font_style": "italic"},
        "comment.hint": {"color": palette["cyan"], "font_style": "italic"},
        "comment.warning": {"color": palette["orange"], "font_style": "italic"},
        "comment.warn": {"color": palette["orange"], "font_style": "italic"},
        "comment.error": {"color": palette["red"], "font_style": "italic"},
        # --- Keywords & operators (green) ---
        "keyword": {"color": palette["green"]},
        "keyword.conditional": {"color": palette["green"]},
        "keyword.conditional.ternary": {"color": palette["green"]},
        "keyword.repeat": {"color": palette["green"]},
        "keyword.return": {"color": palette["green"]},
        "keyword.exception": {"color": palette["green"]},
        "keyword.coroutine": {"color": palette["green"]},
        "keyword.debug": {"color": palette["green"]},
        "keyword.function": {"color": palette["green"]},
        "keyword.operator": {"color": palette["green"]},
        "keyword.modifier": {"color": palette["green"]},
        "keyword.import": {"color": palette["green"]},
        "keyword.export": {"color": palette["green"]},
        "keyword.type": {"color": palette["green"]},
        "keyword.directive": {"color": palette["orange"]},
        "keyword.directive.define": {"color": palette["orange"]},
        "operator": {"color": palette["green"]},
        # --- Punctuation (muted; interpolation/markup specials violet) ---
        "punctuation": {"color": palette["fg2"]},
        "punctuation.bracket": {"color": palette["fg2"]},
        "punctuation.delimiter": {"color": palette["fg2"]},
        "punctuation.list_marker": {"color": palette["orange"]},
        "punctuation.special": {"color": palette["violet"]},
        "punctuation.markup": {"color": palette["violet"]},
        # --- Functions & callables (blue; builtins cyan, macros orange) ---
        "function": {"color": palette["blue"]},
        "function.call": {"color": palette["blue"]},
        "function.method": {"color": palette["blue"]},
        "function.method.call": {"color": palette["blue"]},
        "method": {"color": palette["blue"]},
        "function.builtin": {"color": palette["cyan"]},
        "function.macro": {"color": palette["orange"]},
        "macro": {"color": palette["orange"]},
        "function.decorator": {"color": palette["violet"]},
        "constructor": {"color": palette["blue"]},
        # --- Types, classes, namespaces (muted red; interfaces italic) ---
        # Classes/types are plain `red_muted`; namespaces/modules use the same
        # muted red but bold, so the scope reads as a bolder member of the family.
        # Vivid `red` stays reserved for errors/diff.
        "type": {"color": palette["red_muted"]},
        "type.definition": {"color": palette["red_muted"]},
        "type.class.definition": {"color": palette["red_muted"]},
        "type.super": {"color": palette["red_muted"]},
        "type.interface": {"color": palette["red_muted"], "font_style": "italic"},
        "interface": {"color": palette["red_muted"], "font_style": "italic"},
        "namespace": {"color": palette["red_muted"], "font_weight": 700},
        "module": {"color": palette["red_muted"], "font_weight": 700},
        "concept": {"color": palette["red_muted"]},
        "type.builtin": {
            "color": palette["yellow"]
        },  # builtin/primitive types stay apart
        "enum": {"color": palette["orange"]},  # enums kept distinct from classes
        "label": {"color": palette["violet"]},
        # --- Literal values. Bold marks NAMED immutable values only:
        #     user constants and enum variants (not anonymous number/bool literals).
        "number": {"color": palette["magenta"]},
        "number.float": {"color": palette["magenta"]},
        "float": {"color": palette["magenta"]},
        "integer": {"color": palette["magenta"]},
        "boolean": {"color": palette["yellow"]},
        "constant": {"color": palette["magenta"], "font_weight": 700},
        "constant.builtin": {"color": palette["yellow"], "font_weight": 700},
        "constant.macro": {"color": palette["orange"], "font_weight": 700},
        "variant": {"color": palette["magenta"], "font_weight": 700},
        "character": {"color": palette["cyan"]},
        "character.special": {"color": palette["cyan"]},
        # --- Variables, members, parameters ---
        "variable": {"color": palette["fg1"]},  # plain locals fall to body text
        "variable.builtin": {"color": palette["violet"]},  # self / this / super
        "variable.special": {"color": palette["violet"]},
        "variable.member": {"color": palette["cyan"]},
        "property": {"color": palette["cyan"]},
        "field": {"color": palette["cyan"]},
        "parameter": {"color": palette["violet"]},
        "variable.parameter": {"color": palette["violet"]},
        # --- Strings (cyan; escapes/regex/special orange) ---
        "string": {"color": palette["cyan"]},
        "string.doc": {"color": palette["cyan"]},
        "string.documentation": {"color": palette["cyan"]},
        "string.escape": {"color": palette["orange"]},
        "string.regex": {"color": palette["orange"]},
        "string.regexp": {"color": palette["orange"]},
        "string.special": {"color": palette["orange"]},
        "string.special.symbol": {"color": palette["violet"]},
        "string.special.path": {"color": palette["cyan"]},
        "string.special.url": {"color": palette["blue"]},
        "symbol": {"color": palette["violet"]},
        "preproc": {"color": palette["orange"]},
        # --- Markup (semantic; italic/bold kept because they ARE the meaning) ---
        "title": {"color": palette["orange"], "font_weight": 700},
        "emphasis": {"color": palette["fg1"], "font_style": "italic"},
        "emphasis.strong": {"color": palette["fg1"], "font_weight": 700},
        "link_text": {"color": palette["blue"], "font_style": "italic"},
        "link_uri": {"color": palette["violet"]},
        "text": {"color": palette["fg1"]},
        "text.literal": {"color": palette["cyan"]},
        "primary": {"color": palette["fg1"]},
        "embedded": {"color": palette["fg1"]},
        # --- Tags / markup structure (HTML, JSX) ---
        "tag": {"color": palette["blue"]},
        "tag.attribute": {"color": palette["cyan"]},
        "tag.delimiter": {"color": palette["fg2"]},
        "tag.doctype": {"color": palette["green"]},
        # --- CSS selectors ---
        "selector": {"color": palette["green"]},
        "selector.pseudo": {"color": palette["blue"]},
        # --- Attributes / decorators / annotations (violet) ---
        "attribute": {"color": palette["violet"]},
        "decorator": {"color": palette["violet"]},
        # --- Diff ---
        "diff.plus": {"color": palette["green"]},
        "diff.minus": {"color": palette["red"]},
        # --- Zed runtime keys (not tree-sitter captures) ---
        # Inlay hints read both fg and bg from syntax.hint (Zed PR #36219 moved
        # them off the top-level hint.* status keys). background_color is what
        # the inlay_hints.show_background setting renders. It is a semi-transparent
        # fg3 tint (not an opaque color) so the chip stays distinguishable over
        # ANY line background — including the active line and selections, where an
        # opaque shade would blend in. fg3 lightens on dark / darkens on light.
        "hint": {
            "color": palette["fg2"],
            "background_color": palette["fg3"] + "20",
        },
        "predictive": {
            "background_color": palette["bg1"],
            "color": palette["magenta"],
        },
    }

    theme = {
        "accents": accents,
        "background": palette["bg1"],
        "background.appearance": "transparent",
        "border": palette["fg2"],
        "border.disabled": None,
        "border.focused": palette["fg1"],
        "border.selected": palette["blue"],
        "border.transparent": None,
        "border.variant": None,
        "conflict": palette["red"],
        "conflict.background": palette["bg1"],
        "conflict.border": palette["red"],
        "created": palette["green"],
        "created.background": palette["bg1"],
        "created.border": palette["green"],
        "deleted": palette["orange"],
        "deleted.background": palette["bg1"],
        "deleted.border": palette["orange"],
        "drop_target.background": palette["bg2"],
        "editor.active_line.background": palette["bg2"],
        "editor.active_line_number": palette["fg1"],
        "editor.active_wrap_guide": palette["fg2"],
        "editor.background": palette["bg1"],
        "editor.document_highlight.bracket_background": palette["blue"] + "66",
        "editor.document_highlight.read_background": palette["blue"] + "33",
        "editor.document_highlight.write_background": palette["blue"] + "33",
        "editor.foreground": palette["fg1"],
        "editor.gutter.background": palette["bg1"],
        "editor.highlighted_line.background": palette["bg1"],
        "editor.indent_guide": palette["bg2"],
        "editor.indent_guide_active": palette["fg2"],
        "editor.invisible": palette["bg2"],
        "editor.line_number": palette["fg2"],
        "editor.subheader.background": palette["bg1"],
        "editor.wrap_guide": palette["bg2"],
        "element.active": palette["surf_emphasis"],
        "element.background": palette["surf_field"],
        "element.disabled": palette["bg2"],
        "element.hover": palette["bg2"],
        "element.selected": palette["blue"] + "66",
        "elevated_surface.background": palette["surf_recede"],
        "error": palette["red"],
        "error.background": palette["bg1"],
        "error.border": palette["red"],
        # Ghost elements (icon buttons in tabs/toolbars/panels) must be
        # transparent at rest so they don't float a filled box over the
        # surface they sit on; they only show a tint on hover/active/select.
        # (Filled controls — inputs, activity bar — use element.* instead.)
        "ghost_element.active": palette["blue"] + "99",
        "ghost_element.background": palette["bg1"] + "00",
        "ghost_element.disabled": palette["bg1"] + "00",
        "ghost_element.hover": palette["blue"] + "66",
        "ghost_element.selected": palette["blue"] + "66",
        "hidden": palette["fg2"],
        "hidden.background": palette["bg1"],
        "hidden.border": palette["bg1"],
        "hint": palette["fg2"] + "AA",
        "hint.background": palette["bg1"] + "00",
        "hint.border": palette["fg2"],
        # UI chrome icons use the brighter emphasized shade (fg3) for primary
        # and fg1 for muted/placeholder, so file tree / tab icons stand out more
        # against the background. Editor content uses its own keys and is unaffected.
        "icon": palette["fg3"],
        "icon.accent": accents[0],
        "icon.disabled": palette["fg2"],
        "icon.muted": palette["fg1"],
        "icon.placeholder": palette["fg1"],
        "ignored": palette["fg2"],
        "ignored.background": palette["bg1"],
        "ignored.border": palette["fg2"],
        "info": palette["blue"],
        "info.background": palette["bg1"],
        "info.border": palette["blue"],
        "link_text.hover": palette["blue"],
        "modified": palette["yellow"],
        "modified.background": palette["bg1"],
        "modified.border": palette["yellow"],
        "pane.focused_border": palette["blue"],
        "pane_group.border": palette["fg1"],
        "panel.background": palette["surf_recede"],
        "panel.focused_border": palette["blue"],
        "panel.indent_guide": palette["fg2"],
        "panel.indent_guide_active": palette["fg1"],
        "panel.indent_guide_hover": palette["fg3"],
        "players": players,
        "predictive": palette["magenta"],
        "predictive.background": palette["bg1"] + "00",
        "predictive.border": palette["magenta"],
        "renamed": palette["magenta"],
        "renamed.background": palette["bg1"] + "00",
        "renamed.border": palette["magenta"],
        "scrollbar.thumb.background": palette["bg2"] + "BB",
        "scrollbar.thumb.border": None,
        "scrollbar.thumb.hover_background": palette["bg2"],
        "scrollbar.track.background": None,
        "scrollbar.track.border": palette["bg2"],
        "search.match_background": palette["yellow"] + "99",
        "status_bar.background": palette["surf_recede"],
        "success": palette["green"],
        "success.background": palette["bg1"] + "00",
        "success.border": palette["green"],
        "surface.background": palette["bg1"],
        "syntax": syntax,
        "tab.active_background": palette["bg1"],
        "tab.inactive_background": palette["surf_field"],
        "tab_bar.background": palette["surf_field"],
        "terminal.ansi.background": palette["bg1"],
        "terminal.ansi.black": palette["base02"],
        "terminal.ansi.blue": palette["blue"],
        "terminal.ansi.bright_black": palette["base03"],
        "terminal.ansi.bright_blue": palette["base0"],
        "terminal.ansi.bright_cyan": palette["base1"],
        "terminal.ansi.bright_green": palette["base01"],
        "terminal.ansi.bright_magenta": palette["violet"],
        "terminal.ansi.bright_red": palette["orange"],
        "terminal.ansi.bright_white": palette["base3"],
        "terminal.ansi.bright_yellow": palette["base00"],
        "terminal.ansi.cyan": palette["cyan"],
        "terminal.ansi.dim_black": palette["base02"],
        "terminal.ansi.dim_blue": palette["blue"],
        "terminal.ansi.dim_cyan": palette["cyan"],
        "terminal.ansi.dim_green": palette["green"],
        "terminal.ansi.dim_magenta": palette["magenta"],
        "terminal.ansi.dim_red": palette["red"],
        "terminal.ansi.dim_white": palette["base2"],
        "terminal.ansi.dim_yellow": palette["yellow"],
        "terminal.ansi.green": palette["green"],
        "terminal.ansi.magenta": palette["magenta"],
        "terminal.ansi.red": palette["red"],
        "terminal.ansi.white": palette["base2"],
        "terminal.ansi.yellow": palette["yellow"],
        "terminal.background": palette["bg1"],
        "terminal.bright_foreground": palette["fg3"],
        "terminal.dim_foreground": palette["fg2"],
        "terminal.foreground": palette["fg1"],
        # UI chrome text (tab labels, panels, file tree, status bar) is brightened
        # one notch for higher contrast: primary -> fg3, muted/placeholder -> fg1.
        # Editor code uses "editor.foreground" and is left at the Solarized default.
        "text": palette["fg3"],
        "text.accent": accents[0],
        "text.disabled": palette["fg2"],
        "text.muted": palette["fg1"],
        "text.placeholder": palette["fg1"],
        "title_bar.background": palette["bg1"],
        "title_bar.inactive_background": palette["bg1"],
        "toolbar.background": palette["bg1"],
        "unreachable": palette["violet"],
        "unreachable.background": palette["bg1"],
        "unreachable.border": palette["violet"],
        "warning": palette["orange"],
        "warning.background": palette["bg1"],
        "warning.border": palette["orange"],
    }
    return theme


# =========================================================================
# Dark
# =========================================================================

_dark = surface_shades("dark")
solarized.update(
    {
        "bg1": solarized["base03"],  # editor / canvas
        "bg2": solarized["base02"],  # active line / hover highlight
        "fg1": clean_text(
            solarized["base0"], BODY_L["dark"]
        ),  # body text / vars — clean near-white
        "fg2": lighten(
            solarized["base01"], LIGHT_LIFT
        ),  # comments / secondary content
        "fg3": lighten(
            solarized["base1"], LIGHT_LIFT
        ),  # optional emphasized content
        "surf_recede": _dark["recede"],  # panels, status bar, popovers (sunken)
        "surf_field": _dark["field"],  # inputs, tab bar, inactive tabs
        "surf_emphasis": _dark["emphasis"],  # active / focused list item
    }
)
apply_accents(LIGHT_LIFT)  # cleaner, brighter accents on dark (ADR-0005)

solarized_dark = {
    "appearance": "dark",
    # Prefixed with the family name so these variants don't collide with the
    # separate `solarized` extension, which also ships "Solarized Dark"/"Light".
    # Zed selects themes by this name string, so a shared name would make the
    # two extensions indistinguishable once both are installed.
    "name": "Leo-Solarized Dark",
    "style": solarized_theme(solarized),
}
print("Added Leo-Solarized Dark")

# =========================================================================
# Light
# =========================================================================

_light = surface_shades("light")
solarized.update(
    {
        "bg1": warm(solarized["base3"]),  # editor / canvas (warm cream, not white)
        "bg2": warm(solarized["base2"]),  # active line / hover highlight
        "fg1": clean_text(
            solarized["base00"], BODY_L["light"]
        ),  # body text / vars — clean near-ink
        "fg2": lighten(
            solarized["base1"], -LIGHT_LIFT
        ),  # comments / secondary content
        "fg3": lighten(
            solarized["base01"], -LIGHT_LIFT
        ),  # optional emphasized content
        "surf_recede": _light["recede"],  # panels, status bar, popovers
        "surf_field": _light["field"],  # inputs, tab bar, inactive tabs
        "surf_emphasis": _light["emphasis"],  # active / focused list item
    }
)
apply_accents(-LIGHT_LIFT)  # cleaner, darker accents on light (ADR-0005)

solarized_light = {
    "appearance": "light",
    "name": "Leo-Solarized Light",
    "style": solarized_theme(solarized),
}
print("Added Leo-Solarized Light")

solarized_dict = {
    "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
    "author": "HernandoR",
    "name": "Leo-Solarized",
    "themes": [solarized_dark, solarized_light],
}

# Emitted in two forms from the same data:
#   - themes/leo-solarized-theme.json  — strict JSON, no comments. This is the
#     file Zed's extension packaging tool discovers (it globs themes/*.json and
#     parses them strictly), so it must stay comment-free or the build reports
#     "extension does not provide any features".
#   - themes/leo-solarized-theme.jsonc — identical content with a provenance
#     header, kept for humans. Zed ignores non-.json files, so it is never
#     packaged.
# Both are generated — edit solarized.py, not these outputs.
_HEADER = (
    "// Generated by solarized.py — do not edit by hand.\n"
    "// Run `make` (uv run python solarized.py) to regenerate.\n"
)
_body = json.dumps(solarized_dict, indent=2) + "\n"

json_file = "themes/leo-solarized-theme.json"
with open(json_file, "w") as f:
    f.write(_body)
print(f"Wrote to {json_file}")

jsonc_file = "themes/leo-solarized-theme.jsonc"
with open(jsonc_file, "w") as f:
    f.write(_HEADER)
    f.write(_body)
print(f"Wrote to {jsonc_file}")
