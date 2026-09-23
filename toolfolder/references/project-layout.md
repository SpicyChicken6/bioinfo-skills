# Example tool layout

This Python example is a menu, not a mandatory scaffold. Adapt package layout
and environment files to the language and existing repository. Create only
directories with an immediate purpose.

```text
my-tool/
├── README.md                  # Purpose, installation, quickstart, dev commands
├── AGENTS.md                  # Project development and collaboration rules
├── LICENSE                    # Preserve an existing license; user chooses a new one
├── .gitignore
├── pyproject.toml             # Python package metadata + Pixi workspace
├── pixi.lock                  # Generated, committed dependency resolution
├── src/
│   └── my_tool/               # Shared implementation grouped by functionality
├── tests/
│   └── fixtures/              # Small, versioned test inputs
├── examples/                  # Runnable user examples
├── docs/
│   ├── workflow.yaml          # Components, relationships, tasks, dependencies
│   └── decisions.md           # Optional significant design rationale
├── tasks/                     # Add workspaces when a task needs them
│   └── 01-parser/
│       ├── README.md          # Description, Plan, Output; matching workflow ID
│       ├── review.md          # Optional human-written feedback
│       ├── agent/             # Optional agent experiments and working notes
│       └── manual/            # Optional human experiments
├── benchmarks/                # Optional repeatable performance/accuracy evaluation
└── .github/workflows/         # Automated checks when configured
```

Humans and agents share `src/` and `tests/`; ownership of a task workspace does
not create a separate implementation. Task READMEs link to maintained source,
tests, and validation results. Shipped code must not import from `tasks/`.

Task numbers remain stable as priorities change; YAML dependencies define work
order. Simple tasks can exist only in the workflow without an empty folder.
Keep short implementation notes in the task README and create separate notes
only when needed. Preserve human-written reviews even after acting on them.

Keep the component overview in `docs/workflow.yaml`; do not add an
`architecture.md`. The [workflow contract](workflow-yaml.md) explains how to
record it using existing Research Flow fields. Scientific methods and detailed
design rationale may have their own linked documentation when useful.

Use one locked project environment. Reuse an existing Pixi manifest rather than
introducing a competing one. Other languages can use their normal package
manifests and lockfiles without adopting the Python layout. Keep large benchmark
datasets and generated results outside Git, documenting how to obtain or reproduce
them; small fixtures and selected useful artifacts can be tracked.
