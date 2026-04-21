# The Daily Reflection Tree

A deterministic end-of-day reflection tool built for the DeepThought Fellowship Assignment.

**No LLM at runtime.** The tree is pure structured data. The agent is a simple Python script that walks the tree, branches based on answers, and produces a personalized reflection — with zero API calls.

---

## Repository Structure

```
/tree/
  reflection-tree.json     ← The full tree (42 nodes, all 3 axes)
  tree-diagram.md          ← Mermaid visual of the branching structure

/agent/
  agent.py                 ← Python CLI agent (loads tree from JSON)

/transcripts/
  persona-1-transcript.md  ← Riya: external / entitlement / self-centric path
  persona-2-transcript.md  ← Arjun: internal / contribution / altrocentric path

write-up.md                ← Design rationale (2 pages)
README.md                  ← This file
```

---

## Running the Agent (Part B)

**Requirements**: Python 3.10+ (uses `list[str]` type hints). No external libraries needed.

```bash
# From the repo root
python3 agent/agent.py
```

The agent automatically looks for `../tree/reflection-tree.json` relative to its own location.  
If that fails, it falls back to `./reflection-tree.json` in the same directory.

---

## Reading the Tree (Part A)

The tree is a JSON file: `tree/reflection-tree.json`.

### Schema

Each node has:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier |
| `parentId` | string \| null | Parent node (`null` = root or cross-linked) |
| `type` | string | Node type (see below) |
| `text` | string | What the employee sees (supports `{node_id.answer}` and `{axis.dominant}` interpolation) |
| `options` | list | For questions: answer text. For decisions: routing rules. Empty for others. |
| `target` | string \| null | Explicit jump target (used by bridges and some reflections) |
| `signal` | string \| null | State tally to increment: `"axis1:internal"`, `"axis2:contribution"`, etc. |

### Node Types

| Type | User-visible? | Interaction |
|------|--------------|-------------|
| `start` | Yes | Auto-advances |
| `question` | Yes | Employee picks one option |
| `decision` | No | Routes based on prior answer |
| `reflection` | Yes | Employee reads, clicks Continue |
| `bridge` | Yes | Auto-advances (axis transition) |
| `summary` | Yes | Shows aggregate path summary |
| `end` | Yes | Closes session |

### Decision Routing Format

Decision node `options` are routing rules, not user-visible choices:

```
answer=Option text A|Option text B:TARGET_NODE_ID;answer=Option text C:OTHER_TARGET
```

The agent reads the prior question's recorded answer and finds the matching rule.

### Signal Format

```
axis1:internal   →  state["axis1"]["internal"] += 1
axis2:entitlement →  state["axis2"]["entitlement"] += 1
axis3:self        →  state["axis3"]["self"] += 1
```

At the end, the dominant pole per axis drives the summary template selection.

### Interpolation

Reflection and summary nodes use `{placeholder}` syntax:

- `{A1_OPEN.answer}` → replaced with what the employee selected at node `A1_OPEN`
- `{axis1.dominant}` → replaced with the dominant pole label for axis 1

---

## Tracing a Path Manually

To trace the "external / entitlement / self" path (Persona 1):

```
START → A1_OPEN [Stormy] → A1_D1 → A1_Q1_LOW [felt situation was unfair]
→ A1_D2C → A1_Q2_EXT [no room for choice] → A1_D3B → A1_R_EXT
→ BRIDGE_1_2 → A2_OPEN [contributions not noticed] → A2_D1 → A2_Q1_ENT [earned]
→ A2_D2C → A2_R_MID → BRIDGE_2_3 → A3_OPEN [just me]
→ A3_D1 → A3_Q1_SELF [haven't thought about it] → A3_D2 → A3_R_SELF
→ SUMMARY → END
```

Every path is fully traceable by reading the JSON. No code needed to verify branching logic.

---

## Design Principles

1. **No LLM at runtime** — the agent makes zero API calls. All intelligence is in the tree structure.
2. **Deterministic** — same answers always produce the same path, same reflection, same summary.
3. **Fixed options only** — no free text. The options are designed to honestly capture the spectrum without being leading.
4. **No moralizing** — the external/entitlement/self-centric path doesn't shame the employee. It holds up a mirror and asks a question.
5. **One conversation** — the three axes build on each other. Axis 2's opening connects to what was surfaced in Axis 1. Axis 3's bridge explicitly references both prior axes.

---

## Psychological Grounding

| Axis | Spectrum | Source |
|------|----------|--------|
| Locus | Victim ↔ Victor | Rotter (1954), Dweck (2006) |
| Orientation | Entitlement ↔ Contribution | Campbell et al. (2004), Organ (1988) |
| Radius | Self-centric ↔ Altrocentric | Maslow (1969), Batson (2011) |

See `write-up.md` for full design rationale.
