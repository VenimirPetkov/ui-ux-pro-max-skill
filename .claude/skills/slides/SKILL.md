---
name: slides
description: Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies.
argument-hint: "[topic] [slide-count]"
metadata:
  author: claudekit
  version: "1.0.0"
---

# Slides

Strategic HTML presentation design with data visualization.

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## Script Paths

Paths in this skill and its references are relative to the directory containing the loaded `SKILL.md`. Resolve local `scripts/`, `references/`, and `templates/` paths from that directory, using the skill location supplied by the runtime. Invoke scripts with quoted absolute paths while keeping the working directory at the project root; project inputs and outputs such as `docs/brand-guidelines.md`, `assets/design-tokens.json`, and `src/` remain project-relative.

A command written as `../<skill>/scripts/<file>` refers to another skill. Use the adjacent folder when it exists; otherwise resolve that skill by name through the runtime's available skill catalog and use its actual script path. Separately imported skills may live in unrelated directories. If a required skill or tool is unavailable, report the missing dependency instead of guessing a path.

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Determine the requested operation from the user request. Use `$ARGUMENTS` only if the runtime supplies it; otherwise use the task text directly.
2. Load the corresponding reference listed in Subcommands.
3. Execute with the supplied context; ask only for missing information needed for the task.
