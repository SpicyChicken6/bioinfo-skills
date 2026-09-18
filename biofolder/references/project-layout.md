# Example project layout

This example uses transcriptomics, proteomics, and multimodal integration to show
the hierarchy. Choose modules and tasks for the actual project; these modalities,
task names, and deeper directories are suggestions, not a required scaffold.

```text
project/
├── README.md                          # Purpose, setup, module map, accepted results
├── AGENTS.md                          # Shared folder, ownership, Git, and Pixi rules
├── CLAUDE.md                          # Imports AGENTS.md; Claude-specific additions
├── pixi.toml                          # One project workspace and repeatable tasks
├── pixi.lock                          # Committed dependency resolution
├── .pixi/                             # Generated environments; Git-ignored
├── .git/                              # Git metadata; may be a file in a worktree
├── .gitignore
├── config/                            # Shared configuration; no credentials
├── data/                              # Inputs and datasets shared across modules
│   ├── README.md                      # Sources, locations, provenance, access notes
│   ├── raw/                           # Original shared inputs; preserve unchanged
│   ├── metadata/                      # Sample sheets and data dictionaries
│   ├── interim/                       # Shared intermediate datasets
│   └── processed/                     # Shared analysis-ready datasets
├── docs/
│   ├── workflow.yaml                  # Canonical Research Flow graph
│   ├── methods.md                     # Project methods and reproducibility notes
│   └── decisions.md                   # Decisions that affect multiple tasks
├── modules/
│   ├── 01-transcriptomics/
│   │   ├── README.md                  # Module scope, inputs, task map, accepted results
│   │   ├── config/                    # Modality-specific parameters, if needed
│   │   ├── data/                      # Data specific to this module
│   │   │   ├── README.md
│   │   │   ├── raw/                   # Original transcriptomics inputs
│   │   │   ├── metadata/
│   │   │   ├── interim/               # Intermediate data reused across tasks
│   │   │   └── processed/             # Analysis-ready data reused across tasks
│   │   └── tasks/
│   │       ├── 01-quality-control/
│   │       │   ├── README.md          # Shared task brief, branch links, accepted outputs
│   │       │   ├── agent/             # Agent-owned work and its artifacts
│   │       │   │   ├── code/
│   │       │   │   ├── tests/
│   │       │   │   ├── data/
│   │       │   │   │   ├── interim/
│   │       │   │   │   └── processed/
│   │       │   │   ├── figures/
│   │       │   │   ├── tables/
│   │       │   │   ├── docs/
│   │       │   │   │   └── workflow.md # Optional explanation of this branch's steps
│   │       │   │   └── logs/
│   │       │   └── manual/            # Human-owned work and its artifacts
│   │       │       ├── code/
│   │       │       ├── tests/
│   │       │       ├── data/
│   │       │       │   ├── interim/
│   │       │       │   └── processed/
│   │       │       ├── figures/
│   │       │       ├── tables/
│   │       │       ├── docs/
│   │       │       │   └── workflow.md # Optional; scoped to the manual branch
│   │       │       └── logs/
│   │       └── 02-differential-expression/
│   │           ├── README.md
│   │           ├── agent/             # Add the same internal categories as needed
│   │           └── manual/
│   ├── 02-proteomics/
│   │   ├── README.md
│   │   ├── config/
│   │   ├── data/                      # README.md, raw/, metadata/, interim/, processed/
│   │   └── tasks/
│   │       ├── 01-quality-control/    # README.md + agent/ + manual/
│   │       └── 02-differential-abundance/ # README.md + agent/ + manual/
│   └── 03-multimodal-integration/
│       ├── README.md
│       ├── config/
│       ├── data/                      # Same data categories, only where needed
│       └── tasks/
│           ├── 01-sample-alignment/   # README.md + agent/ + manual/
│           └── 02-joint-analysis/     # README.md + agent/ + manual/
└── .archive/
    └── YYYY-MM-DD_description/
        └── README.md                  # Retirement reason, original paths, replacements
```

## Create only what the work needs

For each new task, create its shared `README.md` and both `agent/` and `manual/`
branch roots. Add deeper directories only when there is content for them. The
expanded quality-control task illustrates available categories, not empty folders
to create everywhere. If Git must preserve an empty branch root, use `.gitkeep`.
Keep task child directories limited to `agent/` and `manual/`.

Use stable, zero-padded names such as `01-quality-control`. Numbers organize the
directory listing; do not renumber existing tasks to express dependencies. Use
globally unique, stable node IDs in `docs/workflow.yaml`, including module context
where useful. Express dependencies explicitly in that graph. It is the canonical
Research Flow YAML; branch-local `docs/workflow.md` files only explain local work.
Do not add a project-level `workflow.md` or a `project-status.md`.

## Place data once, at the scope where it is shared

Preserve original inputs unchanged in project `data/raw/` when shared across
modules, or module `data/raw/` when specific to that module. Record their sources
and locations in the corresponding data README. Reference those inputs from tasks;
do not copy them into project, module, and task directories simultaneously.

Use `data/interim/` for intermediate datasets and `data/processed/` for datasets
ready for the next analysis. Task-specific derivatives stay within their producing
branch. Promote a derivative to module or project data only when it needs to be
shared; preserve provenance and update consumers instead of maintaining ambiguous
copies. Integration tasks normally reference accepted upstream datasets directly.

## Keep ownership separate from validation

Agents write their code, tests, data derivatives, figures, tables, notes, and logs
inside `agent/` by default. They may read `manual/` for context, but modify its
contents only on explicit user request. Preserve human-authored content when
updating the shared task README. Keep `AGENTS.md` and `CLAUDE.md` consistent.

Neither branch name implies that work is validated. Record validation evidence
and explicitly link accepted code and outputs from the shared task README; link
those summaries from module and project READMEs as appropriate. Acceptance does
not require moving files across ownership boundaries or creating duplicate outputs.

## Manage environments and retired work

Use Git from initialization onward. Reuse the repository that covers the project
or initialize one at its root. Track source, docs, configuration, and environment
definitions; exclude raw/private/large data, caches, and environments from automatic
commits. The [session Git policy](git-tracking.md) checks existing changes before
work and makes reviewed local checkpoints. Its age-observation metadata lives
inside Git's local metadata area, not in the project docs or committed history.

Use one Pixi workspace at the project root. During initialization, install both
Python and R with [the starter data-science packages](pixi-environment.md). Commit
`pixi.toml` and `pixi.lock`, ignore `.pixi/`, and run scientific commands through
`pixi run --locked`. Reuse a pre-existing Pixi-enabled `pyproject.toml` when present.
Use named environments inside that workspace when incompatible toolchains require
different dependencies. Install [persistent project instructions](project-instructions.md)
so future sessions keep following these conventions.

Archive superseded work under `.archive/<date>-<topic>/` with a README explaining
what moved, why, and what replaces it. Active modules must not depend on archived
files. Preserve raw inputs and useful provenance; archiving is not deletion.
