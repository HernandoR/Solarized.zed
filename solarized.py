#!/usr/bin/env python

"""
Constructs themes/solarized.json

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

solarized = {
    "base03": "#002b36",  # dark background
    "base02": "#073642",  # dark background highlights
    "base01": "#586e75",  # dark comments / secondary content; light optional emphasized content
    "base00": "#657b83",  # light body text / default code / primary content
    "base0": "#839496",   # dark body text / default code / primary content
    "base1": "#93a1a1",   # dark optional emphasized content; light comments / secondary content
    "base2": "#eee8d5",   # light background highlights
    "base3": "#fdf6e3",   # light background
    "yellow": "#b58900",
    "orange": "#cb4b16",
    "red": "#dc322f",
    "magenta": "#d33682",
    "violet": "#6c71c4",
    "blue": "#268bd2",
    "cyan": "#2aa198",
    "green": "#859900",
}

# VSCode export adds these intermediate shades based on the user's personal tweaks
# (adopted via ADR-0001)
vsc_intermediates = {
    "bg0":     "#00212b",  # even darker than base03 — sidebars, status bar, dropdowns
    "bg_input": "#003847",  # between base03 and base02 — input fields, activity bar
    "bg_tab":  "#004052",  # tab bar / inactive tab backgrounds
    "bg_focus": "#005a6f",  # active/focus list item backgrounds
    "bg_sel":  "#274642",   # selection background
    "bg_title": "#002c39",  # title bar
    "bg_tab_active": "#002b37",  # active tab (diff ~1 from base03)
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
    syntax = {
        "attribute": {"color": palette["blue"]},
        "boolean": {"color": palette["yellow"]},
        "comment": {"color": palette["fg2"], "font_style": "italic"},
        "comment.doc": {"color": palette["fg2"], "font_style": "italic"},
        "constant": {"color": palette["cyan"]},
        "constructor": {"color": palette["blue"]},
        "embedded": {"color": palette["fg1"]},
        "emphasis": {"color": palette["blue"]},
        "emphasis.strong": {"color": palette["blue"], "font_weight": 700},
        "enum": {"color": palette["orange"]},
        "function": {"color": palette["blue"]},
        "hint": {"color": "#4f8297ff", "font_weight": 700},
        "keyword": {"color": palette["green"]},
        "label": {"color": palette["blue"]},
        "link_text": {"color": palette["blue"], "font_style": "italic"},
        "link_uri": {"color": palette["violet"]},
        "number": {"color": palette["magenta"]},
        "operator": {"color": palette["green"]},
        "predictive": {
            "background_color": palette["bg1"],
            "color": palette["magenta"],
        },
        "preproc": {"color": palette["orange"]},
        "primary": {"color": palette["fg1"]},
        "property": {"color": palette["blue"]},
        "punctuation": {"color": palette["fg2"]},
        "punctuation.bracket": {"color": palette["fg2"]},
        "punctuation.delimiter": {"color": palette["fg2"]},
        "punctuation.list_marker": {"color": palette["fg2"]},
        "punctuation.special": {"color": palette["fg2"]},
        "string": {"color": palette["cyan"]},
        "string.escape": {"color": palette["fg2"]},
        "string.regex": {"color": palette["orange"]},
        "string.special": {"color": palette["orange"]},
        "string.special.symbol": {"color": palette["orange"]},
        "tag": {"color": palette["red"]},
        "text.literal": {"color": palette["cyan"]},
        "title": {"color": palette["orange"], "font_weight": 700},
        "type": {"color": palette["yellow"]},
        "variable": {"color": palette["fg1"]},
        "variant": {"color": palette["blue"]},
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
        "element.active": palette["bg_focus"] if "bg_focus" in palette else palette["bg2"],
        "element.background": palette["bg_input"] if "bg_input" in palette else palette["bg2"],
        "element.disabled": palette["bg2"],
        "element.hover": palette["bg2"],
        "element.selected": palette["blue"] + "66",
        "elevated_surface.background": palette.get("bg0", palette["bg1"]),
        "error": palette["red"],
        "error.background": palette["bg1"],
        "error.border": palette["red"],
        "ghost_element.active": palette["fg1"],
        "ghost_element.background": palette.get("bg_input", palette["bg2"]),
        "ghost_element.disabled": palette["fg2"],
        "ghost_element.hover": palette["blue"] + "66",
        "ghost_element.selected": palette["blue"] + "66",
        "hidden": palette["fg2"],
        "hidden.background": palette["bg1"],
        "hidden.border": palette["bg1"],
        "hint": palette["fg2"] + "AA",
        "hint.background": palette["bg1"] + "00",
        "hint.border": palette["fg2"],
        "icon": palette["fg1"],
        "icon.accent": accents[0],
        "icon.disabled": palette["fg2"],
        "icon.muted": palette["fg2"],
        "icon.placeholder": palette["fg2"],
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
        "panel.background": palette.get("bg0", palette["bg2"]),
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
        "status_bar.background": palette.get("bg0", palette["bg2"]),
        "success": palette["green"],
        "success.background": palette["bg1"] + "00",
        "success.border": palette["green"],
        "surface.background": palette["bg1"],
        "syntax": syntax,
        "tab.active_background": palette.get("bg_tab_active", palette["bg1"]),
        "tab.inactive_background": palette.get("bg_tab", palette["bg2"]),
        "tab_bar.background": palette.get("bg_tab", palette["bg2"]),
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
        "text": palette["fg1"],
        "text.accent": accents[0],
        "text.disabled": palette["fg2"],
        "text.muted": palette["fg2"],
        "text.placeholder": palette["fg2"],
        "title_bar.background": palette.get("bg_title", palette["bg2"]),
        "title_bar.inactive_background": palette.get("bg_title", palette["bg2"]),
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

solarized.update(
    {
        "bg1": solarized["base03"],  # background
        "bg2": solarized["base02"],  # background highlights
        "fg1": solarized["base0"],   # body text / default code / primary content
        "fg2": solarized["base01"],  # comments / secondary content
        "fg3": solarized["base1"],   # optional emphasized content
    }
)
# Merge VSCode intermediate shades for the dark variant
solarized.update(vsc_intermediates)

solarized_dark = {
    "appearance": "dark",
    "name": "Solarized Dark",
    "style": solarized_theme(solarized),
}
print("Added Solarized Dark")

# =========================================================================
# Light
# =========================================================================

solarized.update(
    {
        "bg1": solarized["base3"],   # background
        "bg2": solarized["base2"],   # background highlights
        "fg1": solarized["base00"],  # body text / default code / primary content
        "fg2": solarized["base1"],   # comments / secondary content
        "fg3": solarized["base01"],  # optional emphasized content
    }
)
# Remove VSCode-specific intermediate keys for the light variant
for k in vsc_intermediates:
    solarized.pop(k, None)

solarized_light = {
    "appearance": "light",
    "name": "Solarized Light",
    "style": solarized_theme(solarized),
}
print("Added Solarized Light")

solarized_dict = {
    "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
    "author": "harmtemolder",
    "name": "Solarized",
    "themes": [solarized_dark, solarized_light],
}

json_file = "themes/solarized.json"
with open(json_file, "w") as solarized_json:
    json.dump(solarized_dict, solarized_json, indent=2)
    print(f"Wrote to {json_file}")
