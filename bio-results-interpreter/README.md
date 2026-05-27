# Bio Results Interpreter Skill

A lightweight portable skill for Claude Code and Codex that turns existing research background, result figures, tables, and summaries into a concise evidence-grounded interpretation report.

It does **not** run new analyses by default. It focuses on:

- research question and background
- analysis modules
- embedded figures and linked tables
- direct observations
- cautious interpretation
- plausible conclusions and hypotheses
- caveats and next validation steps
- claim-strength table

## Install for Claude Code

Copy this folder into your Claude skills directory or project-level skills folder, depending on your setup.

The important file is:

```text
bio-results-interpreter/SKILL.md
```

## Install for Codex

Copy this folder into your Codex skills directory or project-level skills folder.

Codex should detect the same `SKILL.md` file.

## Recommended usage

```text
Use the bio-results-interpreter skill. Create a Markdown interpretation report from the background, figures, and result tables in this folder. Do not run new analyses. Group results by analysis module. Embed figures and link tables. Make plausible conclusions, but separate direct observations from hypotheses and speculation.
```

## Optional file inventory helper

```bash
python scripts/collect_result_files.py /path/to/project > result_inventory.md
```

Then give `result_inventory.md` to Claude/Codex as context.
