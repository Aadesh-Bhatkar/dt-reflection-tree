# Write-Up: Design Rationale — The Daily Reflection Tree

---

## Why These Questions

The hardest constraint in this assignment is **no free text**. Every question must work as a closed menu — and yet the options must feel honest, not like a trick quiz where the "right" answer is obvious. That tension forced me to think carefully about what each question is actually trying to surface.

### Axis 1 — Locus of Control

The opening question ("If today were a weather report...") is deliberately metaphorical. A tired employee at 7pm resists clinical language. Weather is intuitive, non-judgmental, and emotionally evocative in a way that "how productive were you today?" is not. Rotter's Locus of Control research shows that internal vs. external attribution is revealed not in grand statements, but in small instinctive reactions — so the follow-up questions target *first reactions*, not considered opinions. I used Dweck's growth mindset framing to shape the internal-locus options: they emphasize effort, adaptation, and deliberate decisions rather than just "I succeeded."

### Axis 2 — Contribution vs. Entitlement

The hardest part of designing this axis is that **entitlement is invisible to the person holding it**. It doesn't feel like entitlement — it feels like legitimate expectation. So the questions don't say "were you entitled today?" They ask: *"Which interaction best captures how you showed up?"* and *"Was that expectation earned or assumed?"* The second question in particular is designed to create the slight discomfort of honest self-audit. Organ's OCB research shows that discretionary effort is the clearest signal of contribution orientation — so I used helping behaviors that were explicitly *not in the job description* as the markers for the contribution pole.

### Axis 3 — Radius of Concern

Maslow's 1969 work on self-transcendence (often omitted from the popular "hierarchy" diagram) argued that the most meaningful human experiences involve orientation *beyond* the self. Batson's perspective-taking research operationalizes this as a cognitive skill: can you simulate another person's experience? So the questions here move progressively outward — from "was it just me?" to "a specific person" to "the end user we serve." The final question ("does that feel real or abstract?") is designed to test whether the altrocentric frame is genuine or performed.

---

## How I Designed the Branching

The tree uses two-layer branching per axis:
1. **Opening question** → routes to a High/Mid/Low question bank
2. **Second question** → routes to the specific reflection

This means no axis is decided by a single question, which reduces the risk of misrouting someone based on one ambiguous answer. Signal tallies (internal/external, contribution/entitlement, altrocentric/self) accumulate across both questions, so the summary is based on the aggregate of the path taken — not just the last answer.

**Key trade-off**: I chose *breadth over depth*. With 42 nodes across 3 axes, some paths are shorter than they could be. An alternative design would go 4-5 questions deep per axis with more personalized branching. I prioritized getting a complete, working tree that covers all three axes cleanly over depth on any single axis. With more time, I would expand each axis to 3 questions minimum and add a "recovery" branch that lets someone who initially responded as external check a moment where they did have agency.

**The bridge nodes** are intentionally connective rather than neutral. Each bridge ("Now let's look at what you gave") builds on the axis just completed by framing the next axis as a *natural extension*. Someone who just explored their locus of control is already primed to think about agency — the bridge shifts that to *generosity* of agency. This exploits the psychological progression described in the assignment: locus → contribution → radius is not three independent ideas, it's one coherent arc.

---

## Psychological Sources

- **Rotter, J.B. (1954)**. *Social learning and clinical psychology*. The foundational locus of control framework. Internal attribution = effort, strategy, choice. External attribution = luck, others, circumstances.
- **Dweck, C.S. (2006)**. *Mindset: The New Psychology of Success*. Growth mindset questions ("I adapted") map onto internal locus; fixed/helpless responses ("I felt stuck") map onto external.
- **Campbell, W.K. et al. (2004)**. Psychological entitlement scale. Entitlement is characterized by the belief that one deserves outcomes independent of demonstrated contribution — made visible through questions about recognition expectations.
- **Organ, D.W. (1988)**. Organizational citizenship behavior. Helping beyond formal role requirements is the clearest behavioral marker of contribution orientation.
- **Maslow, A.H. (1969)**. *The farther reaches of human nature*. Self-transcendence: the level above self-actualization, where meaning comes from contributing to something beyond the self.
- **Batson, C.D. (2011)**. *Altruism in humans*. Perspective-taking as a cognitive (not just emotional) capacity — imagining another's experience, not just sympathizing with it.

---

## What I'd Improve With More Time

1. **Deeper axis 1 branching** — add a "recovery" branch that explicitly invites someone on the external path to name one choice they actually did make, rather than just observing the pattern.
2. **Streak/history awareness** — the tree could reference yesterday's dominant signal ("Yesterday you leaned external. Today?") using a local state file. Still deterministic, no LLM.
3. **More summary templates** — the current summary uses 12 templates (2×2×3 combinations). A richer design would include axis-specific modifiers (e.g., "you've been consistently external this week — here's what that often means for teams").
4. **Question rotation** — the same questions every day become predictable. A pool of 3–4 questions per slot that rotates deterministically by day-of-week would keep the tool fresh while remaining fully auditable.
5. **A web interface** — the CLI is functional but a minimal browser UI (single HTML file, no backend) would make the reflective tone easier to sustain. Slow text reveals, a calm dark mode, and no navigation chrome would preserve the conversational feel.

---

*Total nodes: 42 | Questions: 14 | Decision nodes: 14 | Reflections: 9 | Bridges: 2 | Summary: 1*
