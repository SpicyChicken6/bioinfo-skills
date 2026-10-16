# Example project layout

This example uses transcriptomics, proteomics, and multimodal integration to show
the hierarchy. Choose modules and tasks for the actual project; these modalities,
task names, and deeper directories are suggestions, not a required scaffold.

```text
project/
├── README.md                          # Project background and research questions only
├── AGENTS.md                          # Shared folder, ownership, Git, and Pixi rules
├── pixi.toml                          # One project workspace and repeatable tasks
├── pixi.lock                          # Committed dependency resolution
├── .pixi/                             # Generated environments; Git-ignored
├── .git/                              # Git metadata; may be a file in a worktree
├── .gitignore
├── scripts/
│   └── biofolder.py                   # Pixi add-module, add-task, add-run, sync-results
├── config/                            # Shared configuration; no credentials
├── data/                              # Inputs and datasets shared across modules
│   ├── README.md                      # Sources, locations, provenance, access notes
│   ├── raw/                           # Original shared inputs; preserve unchanged
│   ├── metadata/                      # Sample sheets and data dictionaries
│   ├── interim/                       # Shared intermediate datasets
│   └── processed/                     # Shared analysis-ready datasets
├── docs/
│   ├── workflow.yaml                  # Canonical task list and dependencies (Research Flow)
│   ├── workflow-preview.html          # Generated offline viewer; refresh after YAML edits
│   ├── environment.md                 # Optional notes for nonstandard setup
│   ├── methods.md                     # Optional cross-task methods overview
│   └── decisions.md                   # Decisions that affect multiple tasks
├── modules/
│   ├── transcriptomics/
│   │   ├── README.md                  # Module description, requirements, task links
│   │   ├── config/                    # Modality-specific parameters, if needed
│   │   ├── data/                      # Data specific to this module
│   │   │   ├── README.md
│   │   │   ├── raw/                   # Original transcriptomics inputs
│   │   │   ├── metadata/
│   │   │   ├── interim/               # Intermediate data reused across tasks
│   │   │   └── processed/             # Analysis-ready data reused across tasks
│   │   └── tasks/
│   │       ├── 01-quality-control/
│   │       │   ├── README.md          # Task description, plan, and output
│   │       │   ├── agent/             # Agent-owned work and its artifacts
│   │       │   │   ├── code/
│   │       │   │   ├── tests/
│   │       │   │   ├── data/
│   │       │   │   │   ├── interim/
│   │       │   │   │   └── processed/
│   │       │   │   ├── figures/
│   │       │   │   │   └── run-001/   # Figures for this analysis attempt
│   │       │   │   ├── tables/
│   │       │   │   │   └── run-001/   # Findings for the same attempt
│   │       │   │   ├── docs/
│   │       │   │   │   ├── methods.md  # Methods and cumulative run summaries
│   │       │   │   │   ├── review.md   # Optional human-written review and next-task guidance
│   │       │   │   │   ├── workflow.md # Optional orchestration notes; links to methods.md
│   │       │   │   │   └── runs/
│   │       │   │   │       └── run-001/ # Run reservation and optional reports
│   │       │   │   └── logs/
│   │       │   │       └── run-001/
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
│   ├── proteomics/
│   │   ├── README.md
│   │   ├── config/
│   │   ├── data/                      # README.md, raw/, metadata/, interim/, processed/
│   │   └── tasks/
│   │       ├── 01-quality-control/    # README.md + agent/ + manual/
│   │       └── 02-differential-abundance/ # README.md + agent/ + manual/
│   └── multimodal-integration/
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

The [scaffold commands](scaffold-commands.md) create each new task's shared README,
both workspaces with the standard subfolders shown above (without run directories), and
`agent/docs/methods.md` from the [methods template](../assets/task-methods.md),
linked from the README's **Plan** section. For manual scaffolding, include the
methods file and link; add deeper folders as needed. Modules are unnumbered;
task numbers are stable identifiers, not dependency order.
The agent fills the methods record after scaffolding and keeps planned steps
distinct from executed methods. Existing tasks are returned unchanged; when
working on them, add a missing methods file and **Plan** link, preserving existing
documentation.
Before analysis, `pixi run add-run <module> <task>` creates the matching run
directories shown above. Later attempts use `run-002`, `run-003`, and so on,
preserving finalized results. Use run subdirectories under `agent/code/` and
`agent/data/{interim,processed}/` only when those files need run-specific versions;
reference shared inputs and reusable caches in place. Existing custom `results/`
folders may retain matching run subdirectories. Existing unversioned outputs stay
in place; version new work without automatically migrating old files.
See [run versioning](run-versioning.md) for attempt boundaries and run records.
Human-written `agent/docs/review.md` files remain human-owned within the agent
workspace; the [simple review template](../assets/task-review.md) is optional.
The [project rules](../assets/AGENTS.md) define ownership, data placement, Git,
and Pixi conventions. See the [starter packages](pixi-environment.md) and
[workflow schema](workflow-yaml.md) when initializing those parts.
