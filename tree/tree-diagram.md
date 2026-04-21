# Tree Diagram — The Daily Reflection Tree

```mermaid
flowchart TD
    START([🌙 START]) --> A1_OPEN

    %% ─── AXIS 1: LOCUS ───────────────────────────────────────
    A1_OPEN["❓ A1_OPEN\nWeather report?"]
    A1_OPEN -->|Sunny / Overcast| A1_D1_HIGH["🔀 DECISION\nHIGH/MID path"]
    A1_OPEN -->|Stormy / Foggy| A1_D1_LOW["🔀 DECISION\nLOW path"]

    A1_D1_HIGH -->|Sunny| A1_Q1_HIGH["❓ A1_Q1_HIGH\nWhat made it go well?"]
    A1_D1_HIGH -->|Overcast| A1_Q1_MID["❓ A1_Q1_MID\nFirst instinct when off?"]
    A1_D1_LOW --> A1_Q1_LOW["❓ A1_Q1_LOW\nFirst reaction when sideways?"]

    A1_Q1_HIGH -->|Prepared / Adapted| A1_Q2_INT
    A1_Q1_HIGH -->|Team / Lucky| A1_Q2_EXT
    A1_Q1_MID -->|Figure out control / Push through| A1_Q2_INT
    A1_Q1_MID -->|Frustrated / Waited| A1_Q2_EXT
    A1_Q1_LOW -->|Looked for diff / Tried to adapt| A1_Q2_INT
    A1_Q1_LOW -->|Felt unfair / Felt stuck| A1_Q2_EXT

    A1_Q2_INT["❓ A1_Q2_INT\nWhat drove your decision?"]
    A1_Q2_EXT["❓ A1_Q2_EXT\nMore choice than you thought?"]

    A1_Q2_INT -->|Right call / Instinct| A1_R_INT
    A1_Q2_INT -->|Expected / Safest| A1_R_MID_1["💬 A1_R_MID\nReflection: mixed agency"]
    A1_Q2_EXT -->|Yes, could have...| A1_R_MID_1
    A1_Q2_EXT -->|Maybe / No / Not sure| A1_R_EXT

    A1_R_INT["💬 A1_R_INT\nHands on the wheel"]
    A1_R_EXT["💬 A1_R_EXT\nHappened to you"]

    A1_R_INT --> BRIDGE_1_2
    A1_R_MID_1 --> BRIDGE_1_2
    A1_R_EXT --> BRIDGE_1_2

    %% ─── BRIDGE 1→2 ──────────────────────────────────────────
    BRIDGE_1_2(["🔗 BRIDGE 1→2\nFrom how → to what you gave"])

    %% ─── AXIS 2: ORIENTATION ─────────────────────────────────
    BRIDGE_1_2 --> A2_OPEN

    A2_OPEN["❓ A2_OPEN\nHow did you show up\nin interactions?"]
    A2_OPEN -->|Helped someone| A2_Q1_CON["❓ A2_Q1_CON\nWhat motivated it?"]
    A2_OPEN -->|Focused on own work| A2_Q1_MID["❓ A2_Q1_MID\nDid you notice others?"]
    A2_OPEN -->|Not noticed / Waiting| A2_Q1_ENT["❓ A2_Q1_ENT\nEarned or assumed?"]

    A2_Q1_CON -->|Saw need / Meaningful| A2_R_CON
    A2_Q1_CON -->|Hoping noticed / Guilt| A2_R_MID_2["💬 A2_R_MID\nStayed in lane"]
    A2_Q1_MID -->|Yes and helped| A2_R_CON
    A2_Q1_MID -->|Too pressed / Assumed| A2_R_MID_2
    A2_Q1_MID -->|Didn't notice| A2_R_ENT
    A2_Q1_ENT -->|Earned / Mostly earned| A2_R_MID_2
    A2_Q1_ENT -->|Not sure / Assumed| A2_R_ENT

    A2_R_CON["💬 A2_R_CON\nYou gave — and not because you had to"]
    A2_R_ENT["💬 A2_R_ENT\nEntitlement is invisible from inside"]

    A2_R_CON --> BRIDGE_2_3
    A2_R_MID_2 --> BRIDGE_2_3
    A2_R_ENT --> BRIDGE_2_3

    %% ─── BRIDGE 2→3 ──────────────────────────────────────────
    BRIDGE_2_3(["🔗 BRIDGE 2→3\nFrom what you gave → who else was in today"])

    %% ─── AXIS 3: RADIUS ──────────────────────────────────────
    BRIDGE_2_3 --> A3_OPEN

    A3_OPEN["❓ A3_OPEN\nWho comes to mind\nfor today's challenge?"]
    A3_OPEN -->|Just me| A3_Q1_SELF["❓ A3_Q1_SELF\nIs someone carrying more?"]
    A3_OPEN -->|My team| A3_Q1_MID_3["❓ A3_Q1_MID\nSpecific person you noticed?"]
    A3_OPEN -->|Specific person / End user| A3_Q1_ALT["❓ A3_Q1_ALT\nDoes impact feel real?"]

    A3_Q1_SELF -->|Yes someone / Probably| A3_R_MID_3["💬 A3_R_MID\nHeld both"]
    A3_Q1_SELF -->|Don't think so / Haven't thought| A3_R_SELF
    A3_Q1_MID_3 -->|Yes and helped| A3_R_ALT
    A3_Q1_MID_3 -->|Aware but didn't / Generally / Outcome| A3_R_MID_3
    A3_Q1_ALT -->|Real — can picture| A3_R_ALT
    A3_Q1_ALT -->|Somewhat real| A3_R_MID_3
    A3_Q1_ALT -->|Abstract / Not sure| A3_R_SELF

    A3_R_ALT["💬 A3_R_ALT\nLooked up from your own experience"]
    A3_R_MID_3["💬 A3_R_MID\nHeld both — yours and others"]
    A3_R_SELF["💬 A3_R_SELF\nExperienced through your own lens"]

    A3_R_ALT --> SUMMARY
    A3_R_MID_3 --> SUMMARY
    A3_R_SELF --> SUMMARY

    %% ─── SUMMARY + END ───────────────────────────────────────
    SUMMARY["📋 SUMMARY\nAgency · Giving · Radius\n+ dynamic reflection text"]
    SUMMARY --> END(["👋 END\nSee you tomorrow"])

    %% ─── STYLING ─────────────────────────────────────────────
    classDef start fill:#1a1a2e,stroke:#00b4d8,color:#e0e0e0
    classDef question fill:#16213e,stroke:#0077b6,color:#e0e0e0
    classDef decision fill:#0f3460,stroke:#e94560,color:#e0e0e0
    classDef reflection fill:#533483,stroke:#c77dff,color:#e0e0e0
    classDef bridge fill:#1b4332,stroke:#52b788,color:#e0e0e0
    classDef summary fill:#1d3557,stroke:#ffd60a,color:#e0e0e0
    classDef end fill:#1a1a2e,stroke:#00b4d8,color:#e0e0e0

    class START,END start
    class A1_OPEN,A1_Q1_HIGH,A1_Q1_MID,A1_Q1_LOW,A1_Q2_INT,A1_Q2_EXT question
    class A1_D1_HIGH,A1_D1_LOW decision
    class A2_OPEN,A2_Q1_CON,A2_Q1_MID,A2_Q1_ENT question
    class A3_OPEN,A3_Q1_SELF,A3_Q1_MID_3,A3_Q1_ALT question
    class A1_R_INT,A1_R_MID_1,A1_R_EXT,A2_R_CON,A2_R_MID_2,A2_R_ENT,A3_R_ALT,A3_R_MID_3,A3_R_SELF reflection
    class BRIDGE_1_2,BRIDGE_2_3 bridge
    class SUMMARY summary
```

---

## Node Count by Type

| Type | Count |
|------|-------|
| start | 1 |
| question | 14 |
| decision | 14 |
| reflection | 9 |
| bridge | 2 |
| summary | 1 |
| end | 1 |
| **Total** | **42** |

## Possible Paths

Each axis has 3 outcome lanes (High/Mid/Low → Internal/External for Axis 1, Con/Mid/Ent for Axis 2, Alt/Mid/Self for Axis 3).  
Total unique reflection sequences: **3 × 3 × 3 = 27 distinct paths** through the tree.  
Each path produces a different combination of reflections and a different summary template.
