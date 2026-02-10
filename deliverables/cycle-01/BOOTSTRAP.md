# BOOTSTRAP (cycle-01)

## Prompt interpretation
We need a production-ready IRCL TTE factory that can maintain a complete TTDB of IRCL events and produce print-ready PDFs of event card decks. Cycle-01 deliverables are specific: TTDB data for Bot Oblivion 2025, a cards folder populated with card images or generation code, and a reusable Python tool that outputs a PDF resembling `Bot Oblivion 2025_deck.pdf`.

## Team composition
- Bootstrap: Frame objectives, risks, and plan adjustments for cycle-01.
- Storyteller: Define the narrative/visual throughline for cards and event identity.
- SVG engineer: Document SVG constraints and coordinate with Storyteller on card layout/style.
- Orchestrator: Update `PLAN.md`, inputs, and critical path for a production pipeline.
- Core worker: Build TTDB data, card generation pipeline, and PDF assembly.
- Reviewer: Validate TTDB completeness and PDF resemblance to the reference deck.
- Delivery packager: Assemble delivery notes and update release artifacts.
- Retrospective: Recommend process improvements for the next cycle.

## Objectives for cycle-01
- Create a new IRCL TTDB dataset with Bot Oblivion 2025 event + card records.
- Provide a `cards/` folder containing generated card images or the Python generator to create them.
- Deliver a reusable Python tool to assemble a print-ready PDF that visually matches `Bot Oblivion 2025_deck.pdf`.
- Document how to run the pipeline and validate output parity.

## Risks and assumptions
- Bot Oblivion 2025 source data may be incomplete or split across files; we will inventory and normalize inputs.
- The reference PDF defines layout/print specs; we should match page size, card grid, and margins.
- TTDB file format must align with TTDB RFCs; any deviations will be logged.

## Recommended plan adjustments
- Add explicit data-audit and TTDB schema validation tasks before asset generation.
- Add a pipeline checkpoint that compares PDF output against the reference deck (layout, counts, ordering).
- Include RFCs and TTAI specs in `PLAN.md` inputs for this cycle.
- Ensure `cards/` is either generated deterministically by the pipeline or committed as artifacts with provenance.

## Suggested next-cycle prompts (choose one)
1. Expand the TTDB to include a second IRCL event and generate its deck with the same pipeline.
2. Add a data import workflow that pulls event entries from a structured source and updates the TTDB safely.
3. Improve card visual design with alternate themes and export a style guide for future events.

## Retrospective updates (cycle-01)
### Recommended plan changes
- Add an explicit dependency check step that verifies `inkscape`, `pypdf`, and `img2pdf` before any render attempt.
- Add an asset-pinning step to localize fonts and event badge images for offline rendering.
- Add a validation step that compares generated PDF metadata (page size, page count) to the reference deck.

### Offer to implement and reset plan
If you select a next-cycle prompt, I can apply these plan changes and reset `PLAN.md` for the new cycle.

### Updated next-cycle prompts (choose one)
1. Close the delivery gate by bundling local assets and rendering a verified Bot Oblivion 2025 PDF deck.
2. Extend the TTDB to include Spring Bot Breaker 2025 and generate its deck with the same pipeline.
3. Build a safe import tool that converts RobotCombatEvents data into TTDB records and JSON card inputs.
