# Version outputs by analysis run

A task is a scientific question or deliverable; a run is one analysis execution
attempt. Keep successive results inspectable by giving each attempt a task-local
`run-NNN` ID, starting at `run-001`. IDs identify attempts, not approval status.
Approved agent results may remain in `agent/`.

## Reserve a run

Use the [scaffold command](scaffold-commands.md) before starting an attempt:

```bash
pixi run add-run <module> <task>   # From the project root
pixi run add-run <task>            # From the module
pixi run add-run                   # From the task or any directory below it
```

The task must already exist. The helper reserves the next ID by creating
`agent/docs/runs/run-NNN/`, then creates the matching figures, tables, and logs
directories with `.gitkeep` files. It never reuses gaps or overwrites existing
files. It only creates directories; analysis and documentation remain separate.

```text
agent/
├── figures/run-001/
├── tables/run-001/
├── logs/run-001/
└── docs/
    ├── methods.md              # Cumulative methods and run summaries
    ├── review.md               # Optional, human-owned
    └── runs/run-001/
        └── report.md           # Optional per-run methods, QC, and interpretation
```

Keep shared analysis code in `agent/code/`, recording its revision for every run.
Use `agent/code/run-NNN/` for run-specific scripts/notebooks or snapshots when
needed. Run-specific intermediate or processed data may use
`agent/data/{interim,processed}/run-NNN/`. Reference authoritative inputs and
reusable caches in place instead of copying large data for every run. Record
their exact versions or checksums and preserve what is needed to reproduce
completed results. Existing custom `results/` folders may retain matching run
subdirectories.

## Start, resume, and finish

- Start a new run when inputs, parameters, or methods change, or when rerunning a
  completed analysis. Keep its figures, tables, logs, and reports under that ID.
- Deliberately resume the same incomplete attempt under its existing ID when
  continuing the same analysis. Do not call `add-run` again for that resumption;
  append a new summary explaining what continued and preserve useful diagnostics.
- A chat message, planning discussion, or inspection of existing results alone
  does not create a run. A single attempt may span several sessions.
- Preserve finalized outputs and earlier attempts, including failed or partial
  ones. Corrections to finalized results belong in a new run with a link to the
  prior result; do not silently replace it.

After working on a run, append a dated summary to `agent/docs/methods.md` before
the final response. Include its exact ID and status; commands and working
directory; code revision or snapshot; input/reference and environment/lockfile
versions or checksums; parameters/seeds; output links; QC; caveats; and follow-up.
Per-run reports can hold the details, linked from the summary. Keep earlier
entries and unresolved caveats, including when resuming the same ID.

Link accepted artifacts in the task README's **Output** section using their
exact run paths. Downstream analyses must select a specific upstream result and
record its provenance. Preserve human-owned `review.md` and `manual/` files.

For existing tasks, leave legacy unversioned files in place and version new work.
Adopting this convention does not authorize migration, deletion, or rewriting
existing results or project customizations.
