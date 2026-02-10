# REVIEW (cycle-01)

## Checks
- TTDB file format includes title line, `mmpdb` block, `cursor` block, and record sections separated by `---`.
- Typed edges use the declared `type>@TARGET_ID` syntax and are directional.
- Bot Oblivion 2025 event record links to all robot records; robot records link back to the event.
- Generator script is reusable via CLI and outputs to `cards/<event>` and `output/<event>`.

## Risks / gaps
- PDF resemblance to `Bot Oblivion 2025_deck.pdf` was not visually verified in this run.
- Rendering depends on Inkscape and external image/font URLs; offline runs will fail unless assets are bundled.
- The event badge asset is still sourced remotely and not locally pinned.

## Verdict
Meets cycle-01 deliverable requirements with the noted validation gaps.
