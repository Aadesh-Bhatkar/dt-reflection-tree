#!/usr/bin/env python3
"""
The Daily Reflection Tree — CLI Agent
A deterministic reflection tool. No LLM at runtime.
Built for DeepThought Fellowship Assignment.
"""

import json
import os
import sys
import time
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
MAGENTA= "\033[35m"
WHITE  = "\033[37m"
GRAY   = "\033[90m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text: str, delay: float = 0.018, color: str = ""):
    """Print text character by character for a reflective feel."""
    end_color = RESET if color else ""
    for ch in text:
        sys.stdout.write(color + ch + end_color)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def divider(char="─", width=60, color=GRAY):
    print(color + char * width + RESET)

def print_header():
    clear()
    divider("═", 60, CYAN)
    print(CYAN + BOLD + "  🌙  The Daily Reflection Tree".center(60) + RESET)
    divider("═", 60, CYAN)
    print()

def print_node_text(text: str, color: str = WHITE):
    """Print node text with word-wrapping at 60 chars."""
    import textwrap
    wrapped = textwrap.fill(text, width=60)
    slow_print(wrapped, delay=0.012, color=color)

def print_options(options: list[str]) -> int:
    """Display numbered options and return the user's 1-based choice."""
    print()
    for i, opt in enumerate(options, 1):
        print(f"  {CYAN}{BOLD}{i}{RESET}{GRAY}.{RESET}  {opt}")
    print()

    while True:
        try:
            raw = input(f"  {YELLOW}Your choice (1–{len(options)}): {RESET}").strip()
            idx = int(raw)
            if 1 <= idx <= len(options):
                return idx
            print(f"  {GRAY}Please enter a number between 1 and {len(options)}.{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"  {GRAY}Please enter a valid number.{RESET}")

def press_continue():
    input(f"\n  {GRAY}[Press Enter to continue]{RESET} ")

# ─────────────────────────────────────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────────────────────────────────────

class SessionState:
    """Tracks answers and axis signal tallies across the session."""

    def __init__(self):
        self.answers: dict[str, str] = {}        # node_id → chosen answer text
        self.signals: dict[str, dict[str, int]] = {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"altrocentric": 0, "mid": 0, "self": 0},
        }

    def record_answer(self, node_id: str, answer: str):
        self.answers[node_id] = answer

    def apply_signal(self, signal: Optional[str]):
        if not signal:
            return
        parts = signal.split(":")
        if len(parts) != 2:
            return
        axis, pole = parts
        if axis in self.signals and pole in self.signals[axis]:
            self.signals[axis][pole] += 1

    def dominant(self, axis: str) -> str:
        """Return the dominant pole for a given axis."""
        counts = self.signals.get(axis, {})
        if not counts:
            return "balanced"
        top = max(counts, key=lambda k: counts[k])
        # If tied, call it balanced
        values = list(counts.values())
        if values.count(values[0]) == len(values) and len(set(values)) == 1:
            return "balanced"
        return top

    def summary_key(self) -> str:
        a1 = self.dominant("axis1")   # internal / external
        a2 = self.dominant("axis2")   # contribution / entitlement
        a3 = self.dominant("axis3")   # altrocentric / mid / self
        return f"{a1}_{a2}_{a3}"

    def interpolate(self, text: str) -> str:
        """Replace {node_id.answer} and {axis.dominant} placeholders."""
        import re

        def replace_answer(m):
            node_id = m.group(1)
            return self.answers.get(node_id, "[your earlier answer]")

        def replace_dominant(m):
            axis = m.group(1)
            d = self.dominant(axis)
            labels = {
                "internal": "an internal locus — you saw your choices",
                "external": "an external locus — circumstances felt heavy",
                "contribution": "contribution — giving without keeping score",
                "entitlement": "entitlement — waiting to receive",
                "altrocentric": "a wide radius — you thought beyond yourself",
                "mid": "a middle radius — aware of others, but still mostly self-focused",
                "self": "a narrow radius — today was about you",
                "balanced": "somewhere in the middle",
            }
            return labels.get(d, d)

        text = re.sub(r"\{(\w+)\.answer\}", replace_answer, text)
        text = re.sub(r"\{(axis\d)\.dominant\}", replace_dominant, text)
        return text

# ─────────────────────────────────────────────────────────────────────────────
# TREE LOADER
# ─────────────────────────────────────────────────────────────────────────────

class ReflectionTree:
    """Loads and indexes the tree from a JSON file."""

    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.meta = data.get("meta", {})
        self.nodes: dict[str, dict] = {}
        self.children: dict[str, list[str]] = {}  # parentId → [child ids]

        for node in data["nodes"]:
            self.nodes[node["id"]] = node
            pid = node.get("parentId")
            if pid:
                self.children.setdefault(pid, []).append(node["id"])

    def get(self, node_id: str) -> dict:
        return self.nodes[node_id]

    def children_of(self, node_id: str) -> list[str]:
        return self.children.get(node_id, [])

# ─────────────────────────────────────────────────────────────────────────────
# DECISION ROUTING
# ─────────────────────────────────────────────────────────────────────────────

def resolve_decision(node: dict, state: SessionState) -> Optional[str]:
    """
    Parse decision node routing rules.
    Format: "answer=opt1|opt2:TARGET_ID;answer=opt3:OTHER_TARGET"
    Also supports: "condition=axis1.dominant=internal:TARGET_ID"
    """
    rules = node.get("options", [])
    if isinstance(rules, list):
        rule_str = ";".join(rules)
    else:
        rule_str = str(rules)

    # Find the most recently answered question (the parent question node)
    # We look at all answers and take the last recorded one
    last_answer = None
    for rule in rule_str.split(";"):
        rule = rule.strip()
        if rule.startswith("answer="):
            # Find which node this decision is branching on
            # The parent of the decision node is the question node
            parent_id = node.get("parentId")
            if parent_id and parent_id in state.answers:
                last_answer = state.answers[parent_id]
            break

    for rule in rule_str.split(";"):
        rule = rule.strip()
        if not rule or ":" not in rule:
            continue
        condition, target = rule.rsplit(":", 1)
        target = target.strip()

        if condition.startswith("answer="):
            opts_str = condition[len("answer="):]
            options = [o.strip() for o in opts_str.split("|")]
            if last_answer and last_answer in options:
                return target

        elif condition.startswith("condition="):
            # e.g. condition=axis1.dominant=internal
            cond_body = condition[len("condition="):]
            parts = cond_body.split("=")
            if len(parts) == 2:
                axis_key, expected = parts
                if "." in axis_key:
                    axis, method = axis_key.split(".", 1)
                    if method == "dominant" and state.dominant(axis) == expected:
                        return target

    return None

# ─────────────────────────────────────────────────────────────────────────────
# AGENT RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_agent(tree: ReflectionTree):
    state = SessionState()
    current_id = "START"

    print_header()

    while current_id:
        node = tree.get(current_id)
        ntype = node["type"]
        raw_text = node.get("text", "")
        text = state.interpolate(raw_text)
        signal = node.get("signal")
        target = node.get("target")  # explicit jump (bridge, etc.)

        # ── START ──────────────────────────────────────────────────────────
        if ntype == "start":
            print()
            print_node_text(text, color=CYAN)
            print()
            press_continue()
            clear()
            print_header()
            current_id = target or _first_child(tree, current_id)

        # ── QUESTION ───────────────────────────────────────────────────────
        elif ntype == "question":
            print()
            divider()
            print()
            print_node_text(text, color=WHITE + BOLD)
            options = node.get("options", [])
            print_options(options)
            choice_idx = print_options_and_get(options)
            chosen = options[choice_idx - 1]
            state.record_answer(current_id, chosen)
            state.apply_signal(signal)
            clear()
            print_header()
            # Move to first child (likely a decision node)
            current_id = _first_child(tree, current_id)

        # ── DECISION ───────────────────────────────────────────────────────
        elif ntype == "decision":
            next_id = resolve_decision(node, state)
            if not next_id:
                # Fallback: go to first child
                next_id = _first_child(tree, current_id)
            current_id = next_id

        # ── REFLECTION ─────────────────────────────────────────────────────
        elif ntype == "reflection":
            print()
            divider("·", 60, MAGENTA)
            print()
            print_node_text(text, color=MAGENTA)
            print()
            divider("·", 60, MAGENTA)
            state.apply_signal(signal)
            press_continue()
            clear()
            print_header()
            current_id = target or _first_child(tree, current_id)

        # ── BRIDGE ─────────────────────────────────────────────────────────
        elif ntype == "bridge":
            print()
            slow_print(text, delay=0.015, color=BLUE)
            print()
            time.sleep(1.2)
            current_id = target or _first_child(tree, current_id)

        # ── SUMMARY ────────────────────────────────────────────────────────
        elif ntype == "summary":
            _render_summary(node, state)
            press_continue()
            clear()
            print_header()
            current_id = target or _first_child(tree, current_id)

        # ── END ────────────────────────────────────────────────────────────
        elif ntype == "end":
            print()
            divider("═", 60, CYAN)
            print()
            slow_print(text, delay=0.02, color=CYAN)
            print()
            divider("═", 60, CYAN)
            print()
            break

        else:
            # Unknown type — skip
            current_id = target or _first_child(tree, current_id)


def print_options_and_get(options: list[str]) -> int:
    """Display numbered options and return the user's 1-based choice."""
    while True:
        try:
            raw = input(f"  {YELLOW}Your choice (1–{len(options)}): {RESET}").strip()
            idx = int(raw)
            if 1 <= idx <= len(options):
                return idx
            print(f"  {GRAY}Please enter a number between 1 and {len(options)}.{RESET}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n  {GRAY}Please enter a valid number.{RESET}")


def _first_child(tree: ReflectionTree, node_id: str) -> Optional[str]:
    children = tree.children_of(node_id)
    return children[0] if children else None


def _render_summary(node: dict, state: SessionState):
    """Render the summary node with dynamic text and the right template."""
    print()
    divider("═", 60, GREEN)
    print(f"\n{GREEN}{BOLD}  Tonight's Reflection{RESET}\n")

    a1 = state.dominant("axis1")
    a2 = state.dominant("axis2")
    a3 = state.dominant("axis3")

    axis_labels = {
        "internal": "internal locus — you saw your choices",
        "external": "external locus — circumstances felt heavy",
        "contribution": "contribution — giving without scorekeeping",
        "entitlement": "entitlement — expecting before giving",
        "altrocentric": "wide radius — thinking beyond yourself",
        "mid": "mid radius — some awareness of others",
        "self": "narrow radius — mostly your own frame",
        "balanced": "balanced",
    }

    print(f"  {WHITE}Agency    →  {BOLD}{axis_labels.get(a1, a1)}{RESET}")
    print(f"  {WHITE}Giving    →  {BOLD}{axis_labels.get(a2, a2)}{RESET}")
    print(f"  {WHITE}Radius    →  {BOLD}{axis_labels.get(a3, a3)}{RESET}")
    print()
    divider("─", 60, GRAY)
    print()

    # Get the best-matching summary template
    key = state.summary_key()
    templates = node.get("summary_templates", {})
    summary_text = templates.get(key)

    # Fallback: find closest key
    if not summary_text:
        for k, v in templates.items():
            if a1 in k and a2 in k:
                summary_text = v
                break
    if not summary_text:
        summary_text = "Today happened. You reflected on it. That's more than most people do."

    import textwrap
    wrapped = textwrap.fill(summary_text, width=58)
    slow_print(wrapped, delay=0.014, color=WHITE)
    print()
    divider("═", 60, GREEN)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    tree_path = os.path.join(os.path.dirname(__file__), "..", "tree", "reflection-tree.json")
    if not os.path.exists(tree_path):
        # Try same directory
        tree_path = os.path.join(os.path.dirname(__file__), "reflection-tree.json")
    if not os.path.exists(tree_path):
        print(f"Error: Could not find reflection-tree.json")
        print("Make sure the file is at: ../tree/reflection-tree.json")
        sys.exit(1)

    try:
        tree = ReflectionTree(tree_path)
    except json.JSONDecodeError as e:
        print(f"Error loading tree: {e}")
        sys.exit(1)

    print_header()
    print(f"  {GRAY}Loading your reflection tree...{RESET}")
    time.sleep(0.8)

    run_agent(tree)


if __name__ == "__main__":
    main()
