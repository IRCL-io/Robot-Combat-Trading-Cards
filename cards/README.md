# Cards Output

This folder is the default output target for generated card images.

## Generate cards for Bot Oblivion 2025
```bash
python Generate_Robot_Combat_Card_Deck.py --input "Bot Oblivion 2025.json"
```

## Generate cards for another event JSON
```bash
python Generate_Robot_Combat_Card_Deck.py --input "path/to/event.json" --event-name "Event Name"
```

The generator will create a subfolder per event (slugged name) and place
card PNGs there. PDFs are written to `output/<event-slug>/`.
