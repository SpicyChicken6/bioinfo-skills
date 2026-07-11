# Grill Me Skill

A lightweight Claude Code / Codex skill for adaptively stress-testing a plan before implementation. It asks one high-impact question at a time, recommends defensible choices, and tracks dependencies until the design is decision-ready.

The skill is tuned for bioinformatics, where code that runs can still produce invalid science. It therefore prioritizes:

- computational correctness, including version-specific API and parameter behavior
- statistical correctness, including study design, test assumptions, data leakage, backgrounds, multiple testing, effect sizes, uncertainty, and power
- biological correctness, including compatible references, annotations, identifiers, assays, and sample metadata
- explicit justification of consequential defaults and parameter choices
- validation with diagnostics, controls, known-truth data, benchmarks, or sensitivity analyses
- reproducibility, provenance, and prevention of silent failures

## How It Works

The skill inspects available project evidence before asking the user for information. It then chooses the unresolved question with the greatest expected impact, considering the cost of being wrong, uncertainty, irreversibility, and downstream dependencies.

Standard review areas—scope, assumptions, architecture, data flow, failure modes, testing, deployment, monitoring, and governance—are used as lenses rather than a mandatory checklist. There is no fixed branch depth or question quota.

For consequential package or function parameters, the skill verifies version-specific semantics, asks whether the value is justified by the data and study design, and records the rationale. Package defaults are treated as candidate settings, not automatically correct choices.

For example, an over-representation analysis should define an eligible background gene universe that reflects which genes could have entered the foreground. It should also check selection bias from features such as expression, gene length, or detectability. Silently using the whole genome or a package-defined default can change the null model and the resulting statistical conclusions.

## Recommended Usage

```text
Use the grill-me skill to stress-test this bioinformatics plan before implementation.
Prioritize scientific and computational correctness. Ask one high-impact question at a time,
and challenge consequential method, test, and parameter choices rather than accepting defaults.

Plan:
...
```
