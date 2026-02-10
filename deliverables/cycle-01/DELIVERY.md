# DELIVERY (cycle-01)

## What shipped
- Bot Oblivion 2025 TTDB dataset in TTDB RFC format.
- Reusable card/PDF generator with CLI arguments and organized output paths.
- Cards output scaffolding with a wrapper generator script.

## Primary artifacts
- `deliverables/cycle-01/IRCL_TTDB_Bot_Oblivion_2025-cycle.md`
- `library/IRCL_TTDB_v0-1.md`
- `Generate_Robot_Combat_Card_Deck.py`
- `cards/README.md`
- `cards/generate_cards.py`

## How to run
```bash
python Generate_Robot_Combat_Card_Deck.py --input "Bot Oblivion 2025.json"
```

## Output locations
- Card PNGs: `cards/Bot_Oblivion_2025/`
- PDF deck: `output/Bot_Oblivion_2025/Bot_Oblivion_2025_deck.pdf`

## Dependencies
- `inkscape` (SVG to PNG conversion)
- `pypdf` and `img2pdf`
- Network access for remote images/fonts (or replace with local assets)

## Validation status
- PDF resemblance to `Bot Oblivion 2025_deck.pdf` is unverified in this run because `inkscape` is not available in the environment.
