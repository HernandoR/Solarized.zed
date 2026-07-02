# ADR-0005: Legibility-First Palette — Lift Text Tones and Vivify Accents

- Status: Accepted
- Date: 2026-07-02
- Amends: [ADR-0001](adr-0001-adopt-vscode-export-2026-06-13.md) and
  [ADR-0003](adr-0003-computed-surface-ladder-2026-06-26.md), which held the
  content tones and the eight accents at canonical Solarized values.

## Context

Canonical Solarized is intentionally low-contrast and low-chroma — that restraint
is its identity, but in the editor it read to the user as **"灰灰的、暗暗的"**
(grayish and dark): the text felt dim, and the colours felt muddy rather than
clean. Two forces compounded it:

1. **The palette is muted by design.** Content tones (`base0`/`base01`/`base1`)
   sit at mid CIELAB lightness with a faint tint, and the eight accents carry
   modest chroma (cyan C\*35, blue/violet C\*46, magenta/green/yellow/orange
   C\*65–75). On the dark canvas that yields body-text contrast ≈4.7 and several
   accents ≈3.3 — legible, but soft and easily read as "gray."
2. **ADR-0004 moved plain `variable` to body text.** Since identifiers are
   everywhere, more of the editor now renders in the neutral tone, amplifying the
   grayness.

Prior ADRs explicitly kept these canonical: ADR-0001 adopted canonical Solarized
colour values, and ADR-0003 stated "foreground/content tones and the 8 accents
stay canonical Solarized." This ADR revisits that trade-off for the accents and
content tones (the computed *surface* ladder from ADR-0003 is unaffected).

## Decision

> In the context of the editor palette reading as grayish and dark,
> facing the choice between staying faithful to canonical Solarized's muted tones
> or trading some fidelity for legibility,
> we decided to **push the palette off its canonical values via a few eye-tunable
> knobs — set the body foreground to a clean near-neutral, lift the comment and
> emphasized tones away from the background, and boost the eight accents in chroma
> and lightness — holding every accent hue**,
> and against leaving the palette canonical or hand-picking new hexes,
> to achieve a cleaner, crisper, more legible editor that still reads as
> Solarized in hue,
> accepting that this is a deliberate divergence from canonical Solarized and
> that the exact magnitudes are a matter of taste (hence knobs, not constants
> baked into the values).

Concretely, in `solarized.py` (all in LCh/Lab, so hue is preserved and out-of-gamut
requests are gamut-mapped on output):

1. **Body foreground → clean near-neutral.** The default text tone (`fg1`, used by
   `editor.foreground` and plain `variable`/`text`) is set by `clean_text()` to a
   crisp near-white on dark (`BODY_L` 74 → `#b2b7b8`, contrast ≈7.4) / near-ink on
   light (`BODY_L` 40 → `#595f62`), with its teal tint scaled toward neutral
   (`BODY_CHROMA_KEEP` 0.30). Because variables are the most frequent token, this
   fixes the "gray" feel *without* painting them an accent — which would let one
   colour dominate the screen; the vivid accents carry the colour, the frequent
   identifiers read clean-white. Comments (`fg2`) and emphasized/UI text (`fg3`)
   instead keep the `TEXT_CONTRAST_LIFT` (default **8** L\*) lift plus their teal
   tint, so they recede / stay distinct. Terminal ANSI and surfaces are untouched.

2. **Accent vivify** — `apply_accents()` rebuilds the eight accents per variant
   from the captured `_CANONICAL_ACCENTS` via `vivify()`:
   - `ACCENT_CHROMA_BOOST` (default **×1.50**) — shared by both variants; this is
     the lever that kills the "muddy/gray" feel. Note most accents are already at
     the sRGB gamut edge by ≈×1.30, so higher values gamut-map to the same output
     (×1.50 ≡ ×1.30 for blue/green/cyan/magenta/etc.) — the palette is effectively
     at maximum representable chroma for these hues.
   - `ACCENT_LIGHT_LIFT` (default **8** L\*) — directional like the text lift
     (+dark / −light) so the light variant doesn't wash out.
   On dark this yields e.g. blue `#268bd2 → #00a2f6`, cyan `#2aa198 → #00baaf`,
   green `#859900 → #95b000`; accent contrast rises ≈30 %.

3. **`red_muted` re-derived** — the muted red for classes/namespaces (ADR-0004)
   is now derived from the *vivified* red per variant, so it stays in the same
   cleaned-up family (dark `#d26e63`). Vivid `red` remains reserved for
   errors/diff.

4. **Restorable** — set `ACCENT_CHROMA_BOOST = 1.0`, `ACCENT_LIGHT_LIFT = 0`, and
   `TEXT_CONTRAST_LIFT = 0` to return to canonical Solarized. The knobs are
   expected to be tuned by eye in Zed (like `LIGHT_WARM` and the surface ladder).

## Consequences

### Positive
- The editor reads clean and crisp instead of gray/dim — the stated goal.
- Hue is preserved throughout, so it still reads as Solarized, not a different
  palette; the change is "cleaner Solarized," not a re-theme.
- Everything stays parametric: three knobs, tunable by eye, fully reversible.
- Accents are cleaned consistently across syntax, UI status colours, and terminal
  ANSI, so nothing looks half-canonical.

### Negative / Risks
- A deliberate break from canonical Solarized fidelity — purists will notice, and
  it supersedes the "accents stay canonical" stance of ADR-0001/0003.
- The chroma boost hits the sRGB gamut ceiling for most accents by ≈×1.30, so
  the knob saturates — turning it higher has no further effect (values are
  gamut-mapped). Pushing "cleaner" past this point would need a different lever
  (lightness, or a wider gamut like Display-P3, which Zed themes don't target).
- Magnitudes are subjective and set by eye; they may need further tuning per the
  user's display and ambient light.
