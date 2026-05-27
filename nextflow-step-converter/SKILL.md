---
name: nextflow-step-converter
description: Convert existing analysis scripts, commands, notebooks, or manually described data-analysis steps into clean, resumable, trackable Nextflow DSL2 workflow components. Use when the user wants scripts packaged as Nextflow processes, modules, workflows, step manifests, or reproducible execution units. Do not redesign the analysis logic unless explicitly requested.
---

# Nextflow Step Converter

## Purpose

Convert existing analysis logic into Nextflow DSL2 components so analysis steps become resumable, trackable, reproducible, and easier to summarize later.

This skill is a packaging and workflow-conversion skill. It is not a general analysis-design skill.

Core workflow:

**Existing script or command → explicit input/output contract → step manifest → Nextflow process → DSL2 workflow → config and run instructions**

## When to use this skill

Use this skill when the user asks to:

- convert scripts into Nextflow
- wrap R, Python, bash, or command-line steps as Nextflow processes
- make an analysis resumable with `-resume`
- make tasks trackable with trace, report, and timeline outputs
- split a workflow into DSL2 modules
- create a minimal `main.nf`
- create a `nextflow.config`
- create step manifests for agent-generated analysis steps
- convert exploratory code into a more reproducible workflow

## When not to use this skill

Do not use this skill when the user only wants:

- biological interpretation of final results
- manuscript discussion writing
- open-ended hypothesis generation
- new statistical method design
- major pipeline redesign

If a better statistical method seems needed, note it separately. Do not silently change the method.

## Main rule

**Package existing analysis logic. Do not redesign it.**

The agent may improve file paths, parameters, process boundaries, and workflow structure, but should not change the core method, statistical model, filtering thresholds, or biological assumptions unless the user explicitly asks.

## Required behavior

For every converted step, identify or create:

1. Step name
2. Purpose
3. Input files
4. Output files
5. Parameters
6. Script or command to run
7. Software environment, container, conda env, or module load requirements
8. Expected resource needs if known
9. Publish directory
10. Stub command for quick testing when possible

## Recommended output structure

Prefer this project layout unless the user has a different one:

```text
project/
  main.nf
  nextflow.config
  modules/
    local/
      step_name.nf
  scripts/
    existing_script.R
    existing_script.py
  conf/
    base.config
  manifests/
    step_manifest.yaml
  results/
  logs/
```

## Step manifest format

Before writing Nextflow code for a non-trivial workflow, produce or update a manifest like:

```yaml
steps:
  - id: step_name
    purpose: Short description of the step
    script: scripts/script_name.R
    inputs:
      - path: data/input.tsv
        type: file
        description: input table
    outputs:
      - path: results/step_name/output.tsv
        type: table
        description: main result table
    parameters:
      parameter_name: default_value
    environment:
      container: docker_image_or_null
      conda: env_file_or_null
    resources:
      cpus: 2
      memory: 8 GB
      time: 2h
```

## Nextflow process rules

Use DSL2.

Each process should:

- have a clear process name in uppercase or consistent project style
- take explicit inputs through `input:`
- declare all expected outputs through `output:`
- use `publishDir` only for final or useful outputs
- avoid hidden hard-coded absolute paths
- avoid modifying input files
- avoid writing outputs outside the task working directory except through declared outputs and `publishDir`
- expose parameters through `params`
- use containers, conda, or clearly documented environment requirements
- include `stub:` when practical

## Channel and workflow rules

For simple workflows, create a readable `main.nf` with:

- `nextflow.enable.dsl=2`
- input parameters with defaults
- validation of required paths when useful
- clear channels from input paths
- included local modules
- one workflow block

For larger workflows, create one module per logical step under `modules/local/`.

## File and path rules

Prefer relative paths and stable output directories:

```text
results/<module_name>/
logs/<module_name>/
```

Never assume a user-specific absolute path unless the user provides one and asks to keep it.

## Resumability rules

To preserve Nextflow caching and resumability:

- keep declared inputs stable
- keep process scripts deterministic
- do not mutate input files
- write all outputs inside the task directory first
- declare outputs explicitly
- avoid timestamps inside output filenames unless required
- set random seeds in wrapped scripts when relevant
- document software versions

## Reporting rules

Always recommend running with:

```bash
nextflow run main.nf -resume -with-report -with-trace -with-timeline
```

If the user wants a reportable workflow, ensure outputs include files that downstream interpretation skills can read, such as:

- `results/`
- `trace.txt`
- `report.html`
- `timeline.html`
- `pipeline_info/` if used
- summary tables
- figures
- logs

## Output response style

When generating files, summarize:

- files created or modified
- how to run the workflow
- what each process does
- what outputs to expect
- assumptions made
- unresolved questions or required user checks

## Safety and correctness checks

Before finalizing a conversion, check:

- Are all expected outputs declared?
- Are input paths explicit?
- Does each process have one clear responsibility?
- Are there hidden dependencies or hard-coded paths?
- Are containers or environments documented?
- Does the workflow support `-resume`?
- Are outputs organized for later interpretation?

## Do not over-engineer

Default to minimal, readable DSL2. Avoid heavy nf-core style unless the user asks for it.
