# SVG_ENGINEER (cycle-01)

## SVG constraints and guidance
- **Render path:** Cards are authored as SVG pages and rasterized via Inkscape. Remote image URLs must be reachable at render time.
- **Fonts:** The current pipeline embeds Roboto via remote `@font-face` URLs. If offline rendering is required, bundle fonts locally or swap to installed fonts.
- **Sizing:** Page is US Letter at 300 dpi (2550x3300). Card grid is 3x3 with 1/8" spacing. Keep card dimensions consistent to preserve print alignment.
- **Image fill:** Robot images are placed as `<image>` elements sized to the card width. Ensure aspect ratio is maintained or cropping looks intentional.
- **Safe text zones:** Name band and footer bands should stay clear of the image area to avoid overlaps and to keep print-safe margins.

## Collaboration notes for Storyteller
- The documentary tone is supported by clean bands and a consistent visual cadence.
- Emphasize a repeatable event badge or footer mark on every card to anchor the event identity.

## Implementation notes
- Prefer a single SVG template for all cards with param-driven inserts.
- Keep SVGs deterministic so regeneration yields identical layouts.
