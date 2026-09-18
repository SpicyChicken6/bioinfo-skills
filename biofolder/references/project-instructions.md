# Persistent project instructions

During initialization, install durable instructions at the **project root** so
later sessions keep following the layout and environment policy without having
to reload biofolder. Use the exact filenames `AGENTS.md` and `CLAUDE.md`.

## One shared set of rules

- Use [the AGENTS.md template](../assets/AGENTS.md) as the shared project policy.
  It covers orientation, file placement, human/agent ownership, data provenance,
  Pixi, and the boundaries of the workflow plan.
- Use [the CLAUDE.md template](../assets/CLAUDE.md) to import that policy with a
  standalone `@AGENTS.md` line outside a code fence. Keep Claude-specific additions
  below the import when needed; avoid copying the whole policy into both files.
- Copy these assets into a new project; they are templates, not instructions to
  reorganize the skill repository itself. Tailor them to agreed project choices.

For existing projects, read both files and relevant nested instructions first.
Merge missing rules into the existing shared policy, preserving project-specific
requirements, user overrides, and Claude-specific content. Do not overwrite
either file wholesale or create a second competing policy. If `CLAUDE.md` already
has substantive rules, retain them while consolidating only confirmed duplicates.
Surface unresolved contradictions rather than silently changing their meaning.

## What belongs in the policy

Keep stable operating rules in `AGENTS.md`:

- Read the root README, `docs/workflow.yaml`, and relevant module/task READMEs.
- Put agent code and artifacts in the task's `agent/` workspace; protect `manual/`
  and raw inputs, and maintain the shared README and accepted-output references.
- Use the project Pixi workspace for Python, R, notebooks, and scientific tools.
  Manage dependencies through Pixi and run ordinary analysis with a current lock.
- Keep the canonical plan in `docs/workflow.yaml`; keep detailed methods and
  results in task docs. Reading a plan does not authorize executing or editing it.

Keep package versions and installed dependencies in the manifest and lockfile.
Keep changing observations, analysis decisions, commands, validation evidence,
and result links in task READMEs/docs. Record project-wide decisions in
`docs/decisions.md` when appropriate. Instruction files are not session logs.

After merging, verify the root `CLAUDE.md` import resolves to the root `AGENTS.md`
and that neither file contradicts the actual layout or manifest. Summarize the
installed rules and any intentional project-specific deviations.

The import syntax follows [Claude Code's documented file imports](https://code.claude.com/docs/en/memory#import-additional-files).
