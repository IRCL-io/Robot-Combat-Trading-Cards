# IRCL TTDB (Bot Oblivion 2025)

```mmpdb
db_id: mmpdb:ircl:events:v0-1
db_name: "IRCL TTDB"
coord_increment:
  lat: 1
  lon: 1
collision_policy: southeast_step
timestamp_kind: unix_utc
umwelt:
  umwelt_id: umwelt:tte:agent:default:v1
  role: ai_shop_assistant
  perspective: "A maker-scale assistant that models only what can be sensed, stored, related, or acted on in this repo."
  scope: "Local project files, referenced devices, and the semantic links between artifacts, people, and actions."
  constraints:
    - "If it cannot be sensed, stored, related, or acted upon, it does not exist inside the TTE umwelt."
    - "No optimization for scale beyond human comprehension."
    - "No replacement of human judgment."
    - "No hiding uncertainty or ambiguity."
    - "No correctness over learnability."
    - "Unknowns are allowed; rough edges are acceptable."
    - "Curiosity outranks polish."
  globe:
    frame: "workspace_map"
    origin: "Repo root as the reference point for artifacts and actions."
    mapping: "Observations are projected into a lattice of files, devices, and story nodes."
    note: "Coordinates encode semantic relationships, not physical positions."
cursor_policy:
  max_preview_chars: 280
  max_nodes: 25
typed_edges:
  enabled: true
  syntax: "type>@TARGET_ID"
  note: "Types are free-form tokens; edges remain directional."
```

```cursor
selected:
  - @LAT0LON0
preview:
  @LAT0LON0: "Bot Oblivion 2025 event record with roster of robots and source URLs."
agent_note: "Cycle-01 event dataset for Bot Oblivion 2025."
```

---

@LAT0LON0 | created:1770743813 | updated:1770743813 | relates:has_bot>@LAT1LON1,has_bot>@LAT2LON1,has_bot>@LAT3LON1,has_bot>@LAT4LON1,has_bot>@LAT5LON1,has_bot>@LAT6LON1,has_bot>@LAT7LON1,has_bot>@LAT8LON1,has_bot>@LAT9LON1,has_bot>@LAT10LON1,has_bot>@LAT11LON1,has_bot>@LAT12LON1,has_bot>@LAT13LON1,has_bot>@LAT14LON1,has_bot>@LAT15LON1,has_bot>@LAT16LON1,has_bot>@LAT17LON1,has_bot>@LAT18LON1,has_bot>@LAT19LON1,has_bot>@LAT20LON1,has_bot>@LAT21LON1,has_bot>@LAT22LON1,has_bot>@LAT23LON1,has_bot>@LAT24LON1

## Bot Oblivion 2025 (Event)
- URL: https://www.robotcombatevents.com/events/4646
- Location: Gem State Gaming Convention
- Dates: Saturday, July 19, 2025 - Sunday, July 20, 2025
- Competitions:
  - Beetleweight: https://www.robotcombatevents.com/events/4646/competitions/5404

### Robots
- @LAT1LON1 BoomBox (Beetleweight)
- @LAT2LON1 SweeperKeeper (Beetleweight)
- @LAT3LON1 Virilade (Beetleweight)
- @LAT4LON1 Renegade (Beetleweight)
- @LAT5LON1 Gyro (Beetleweight)
- @LAT6LON1 Plan B (Beetleweight)
- @LAT7LON1 Under-Bite (Beetleweight)
- @LAT8LON1 Apple Monger (Beetleweight)
- @LAT9LON1 TENACITY! (Full Combat Antweight)
- @LAT10LON1 A is for Aardvark FC (Full Combat Antweight)
- @LAT11LON1 Triple A (Full Combat Antweight)
- @LAT12LON1 ICU2 (Full Combat Antweight)
- @LAT13LON1 JUMBO (Full Combat Antweight)
- @LAT14LON1 Anubis (Full Combat Antweight)
- @LAT15LON1 Cyclone (Full Combat Antweight)
- @LAT16LON1 Deadly Croissant (Plastic Antweight)
- @LAT17LON1 Schlagzeug (Plastic Antweight)
- @LAT18LON1 I Think I'm A Clone Now (Plastic Antweight)
- @LAT19LON1 Squatchy (Plastic Antweight)
- @LAT20LON1 WedgeMaster (Plastic Antweight)
- @LAT21LON1 Double A (Plastic Antweight)
- @LAT22LON1 Rickrolled (Plastic Antweight)
- @LAT23LON1 RUPTURE (Plastic Antweight)
- @LAT24LON1 Uhmerican Exxxpress (Plastic Antweight)

---

@LAT1LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## BoomBox
- Weight class: Beetleweight
- Team: BoomBox
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/13551/inbound875028470751609531.png

---

@LAT2LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## SweeperKeeper
- Weight class: Beetleweight
- Team: BoomBox
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/21130/Screenshot_20250505_085650_Fusion.jpg

---

@LAT3LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Virilade
- Weight class: Beetleweight
- Team: Idiocracy
- Image: https://www.robotcombatevents.com/assets/RCELogo-3383ca77f76e5be2b7755ea9d0c464aea25a87d8c9f2a4cffd63643392f59fe7.png

---

@LAT4LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Renegade
- Weight class: Beetleweight
- Team: Bad Decisions Robotics
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/14013/IMG_1146-min.jpeg

---

@LAT5LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Gyro
- Weight class: Beetleweight
- Team: Geometrically Robotic
- Image: https://www.robotcombatevents.com/assets/RCELogo-3383ca77f76e5be2b7755ea9d0c464aea25a87d8c9f2a4cffd63643392f59fe7.png

---

@LAT6LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Plan B
- Weight class: Beetleweight
- Team: Something
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/18553/476064446_519674403912169_7897790394868896022_n.jpg

---

@LAT7LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Under-Bite
- Weight class: Beetleweight
- Team: BuhlerBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/21447/Image_1.jpeg

---

@LAT8LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Apple Monger
- Weight class: Beetleweight
- Team: Tele Present Tense
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/21623/apples_Medium.png

---

@LAT9LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## TENACITY!
- Weight class: Full Combat Antweight
- Team: Team HyperTech Robotics
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/18674/20250715_140123__1_.jpg

---

@LAT10LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## A is for Aardvark FC
- Weight class: Full Combat Antweight
- Team: Buhler's Bots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/20619/IMG_8658.JPG

---

@LAT11LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Triple A
- Weight class: Full Combat Antweight
- Team: Bad Decisions Robotics
- Image: https://www.robotcombatevents.com/assets/RCELogo-3383ca77f76e5be2b7755ea9d0c464aea25a87d8c9f2a4cffd63643392f59fe7.png

---

@LAT12LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## ICU2
- Weight class: Full Combat Antweight
- Team: Tele Present Tense
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/17217/ICU2_Medium_2.png

---

@LAT13LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## JUMBO
- Weight class: Full Combat Antweight
- Team: Something
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/11026/jumbo.jpg

---

@LAT14LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Anubis
- Weight class: Full Combat Antweight
- Team: BoomBox
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/13584/20250716_193414.jpg

---

@LAT15LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Cyclone
- Weight class: Full Combat Antweight
- Team: Bobbsey Twins
- Image: https://www.robotcombatevents.com/assets/RCELogo-3383ca77f76e5be2b7755ea9d0c464aea25a87d8c9f2a4cffd63643392f59fe7.png

---

@LAT16LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Deadly Croissant
- Weight class: Plastic Antweight
- Team: BoweBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/17486/PXL_20250505_042220639.jpg

---

@LAT17LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Schlagzeug
- Weight class: Plastic Antweight
- Team: BoweBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/17612/PXL_20250507_120441776.jpg

---

@LAT18LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## I Think I'm A Clone Now
- Weight class: Plastic Antweight
- Team: BoweBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/19596/PXL_20250314_020823711_2__1_.jpg

---

@LAT19LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Squatchy
- Weight class: Plastic Antweight
- Team: Team Squatch
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/16140/sqmk3.1.jpg

---

@LAT20LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## WedgeMaster
- Weight class: Plastic Antweight
- Team: BoweBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/20957/Wedgemaster.png

---

@LAT21LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Double A
- Weight class: Plastic Antweight
- Team: Bad Decisions Robotics
- Image: https://www.robotcombatevents.com/assets/RCELogo-3383ca77f76e5be2b7755ea9d0c464aea25a87d8c9f2a4cffd63643392f59fe7.png

---

@LAT22LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Rickrolled
- Weight class: Plastic Antweight
- Team: BoweBots
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/21313/Screenshot_2025-06-24_153703.png

---

@LAT23LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## RUPTURE
- Weight class: Plastic Antweight
- Team: Geometrically Robotic
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/21376/IMG_5078.jpg

---

@LAT24LON1 | created:1770743813 | updated:1770743813 | relates:competes_in>@LAT0LON0

## Uhmerican Exxxpress
- Weight class: Plastic Antweight
- Team: Idiocracy
- Image: https://robotcombatevents.s3.amazonaws.com/uploads/resource/photo/12284/UhmericanExxxpress.png
