# Example project layout

This example uses transcriptomics, proteomics, and multimodal integration to show
the hierarchy. Choose modules and tasks for the actual project; these modalities,
task names, and deeper directories are suggestions, not a required scaffold.

```text
project/
├── README.md                          # Purpose, setup, module map, accepted results
├── AGENTS.md                          # Shared folder, ownership, Git, and Pixi rules
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

Create each task's shared README and both workspace roots; populate deeper folders
only as needed. Module/task numbers are stable identifiers, not dependency order.
The [project rules](../assets/AGENTS.md) define ownership, data placement, Git,
and Pixi conventions. See the [starter packages](pixi-environment.md) and
[workflow schema](workflow-yaml.md) when initializing those parts.
