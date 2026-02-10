# My Mental Palace DB
A single-file semantic story database. It stores records as markdown nodes in a network graph of semantic links. The ID of each record is a latitudinal and longitudinal point on a knowledge globe, defined by the librarian's umwelt.    
Agent note: users may refer to this DB and its actions (e.g., "select", "update", "insert", "delete", "upsert") using data-user parlance; interpret those requests as edits to this file's current cursor selection, DB properties, or records. If a request is ambiguous (e.g., multiple possible records), ask a short clarification or select the most recently updated matching record and state the assumption.

```mmpdb
db_id: mmpdb:sample:stroll
db_name: "My Mental Palace DB"
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
librarian:
  enabled: true
  primitive_queries:
    - "SELECT <record_id>"
    - "FIND <token>"
    - "EDGES <record_id>"
    - "LAST <n>"
    - "STATUS"
  max_reply_chars: 240
  invocation_prefix: "@AI"
```

```cursor
selected:
  - @LAT-81.6LON0.0
preview:
  @LAT-45.2LON-7.3: "TTAI is a maker-scale shop assistant and mmpdb librarian. It assumes the active umwelt and can be invoked as \"@AI\"."
agent_note: "Interpret DB-action language as edits to the current cursor selection, DB properties, or records. If selection is ambiguous, ask or select the most recently updated match and state the assumption. Favor maker-scale, inspectable state."
dot: |
  digraph Cursor {
    rankdir=LR;
    "@LAT-45.2LON-7.3" -> "@LAT-48.8LON76.9" [label="assumes"];
    "@LAT-45.2LON-7.3" -> "@LAT-47.0LON-145.2" [label="defaults_to"];
    "@LAT-45.2LON-7.3" -> "@LAT-61.9LON-30.5" [label="operates_in"];
    "@LAT-45.2LON-7.3" -> "@LAT-54.8LON23.2" [label="archives_to"];
  }
```

---

@LAT-81.6LON0.0 | created:1700000000 | updated:1700000600 | relates:inspires>@LAT-71.1LON-84.2,anchors>@LAT-75.4LON137.9

## The Root Workbench
You arrive at **@LAT-81.6LON0.0**, the root node.  
![the forge](/images/time-foundry.svg)
A workbench sits here, lit well enough to build, dim enough to notice what is unknown.   
- **Rule of this workshop:** all paths are *chosen*, not forced.
- The bench **inspires** a first workflow to [the South-East](@LAT-71.1LON-84.2).
- It also **anchors** a small alcove to [the East](@LAT-75.4LON137.9).
---

@LAT-75.4LON137.9 | created:1700000100 | updated:1700000700 | relates:references>@LAT-81.6LON0.0,tradeoffs>@LAT-67.6LON53.7

## The Alcove of Tradeoffs
A thin shelf of notes, all written in the same hand, but in different moods.

This alcove exists to remind you:
- even neighbors can disagree
- disagreement can be *useful*
- a tradeoff edge is a build device

---

@LAT-71.1LON-84.2 | created:1700000200 | updated:1700000900 | relates:leads_to>@LAT-61.9LON-30.5,iterates>@LAT-67.6LON53.7,blocks>@LAT-64.6LON-168.4

## Workflow Corridor
The corridor slopes South-East one increment at a time.
Each step is a coordinate, each coordinate a promise.

This corridor:
- **leads_to** a workshop
- **iterates** a side room of repeating motifs
- **blocks** a locked door nearby

---

@LAT-67.6LON53.7 | created:1700000250 | updated:1700000950 | relates:refines>@LAT-61.9LON-30.5,tradeoffs>@LAT-75.4LON137.9

## Iteration Room
Here, the same idea repeats until it changes shape.

- An iteration is not duplication.
- An iteration is a pressure wave that reveals structure.

This room **refines** the workshop by sending it better questions.

---

@LAT-64.6LON-168.4 | created:1700000300 | updated:1700001000 | relates:gates>@LAT-57.0LON-114.7

## The Locked Gate (With a Friendly Note)
The gate is locked, but the note is not.

> "If you can explain the build in one paragraph, you may enter."

This node **gates** a deeper chamber (a future you, waiting).

