# Project instructions

## Before working

- Read README.md, docs/workflow.yaml, and relevant task notes and human reviews.
- Inspect Git changes before editing; preserve unrelated work.
- Follow existing conventions and stay within the requested scope.
- Resolve routine choices independently; ask when ambiguity materially changes
  requirements, public behavior, or compatibility.

## File placement and ownership

- Put maintained implementation in src/ and automated tests in tests/, adapting
  these paths to the project's established language conventions.
- Put runnable user examples in examples/ and small test inputs in tests/fixtures/.
- Use tasks/<NN-name>/ for plans, experiments, validation results, and links to
  implementation. Task numbers are stable identifiers, not execution order.
- Humans and agents edit the same maintained source and tests. Shipped code
  must not depend on task workspaces; promote reusable experiments into source.
- Use agent/ and manual/ only for separate exploratory work. Use Git branches or
  worktrees when independent source changes need isolation.
- Read relevant task review.md files before continuing work. Preserve human
  review notes and manual work unless asked to edit them.
- Create directories and documentation only when needed.

## Implementation and environment

- Keep changes focused and reuse existing functionality. Separate core logic
  from CLI, UI, and external-service adapters where applicable.
- Preserve public interfaces and file formats unless a change is intended.
- Validate inputs at external boundaries and provide actionable errors; do not
  silently discard data or hide failures.
- Add dependencies when their benefit justifies the maintenance cost.
- Use the project's locked environment and documented commands. Keep package
  metadata and environment definitions consistent.
- Track source, documentation, configuration, and lockfiles. Exclude secrets,
  environments, caches, and large generated outputs from Git.

## Documentation and review

- Keep README.md focused on purpose, installation, and working examples. Its
  Development section records actual install, test, lint, and build commands.
- Use docs/workflow.yaml as the canonical record of components, relationships,
  task statuses, and dependencies. Do not create a separate architecture.md.
- In Research Flow version 1, describe components and runtime relationships in
  project.description; depends_on describes development prerequisites only.
- Reading the workflow does not request execution or edits. Keep plan changes
  within the user's requested scope and preserve unrelated content and layout.
- Keep task READMEs concise: Description, Plan, Output. Link to them from YAML
  notes rather than duplicating implementation details or task-status tracking.
- Record significant design rationale in docs/decisions.md when useful.
- Document scientific algorithms, assumptions, and validation where relevant.

## Validation and completion

- Run checks appropriate to the change, including meaningful failure cases.
- Add regression tests for bug fixes when practical. Documentation-only changes
  normally need link and content checks, not new automated tests.
- Update affected documentation and examples.
- Report what changed, what was checked, and remaining limitations. Distinguish
  planned validation from observed results; never claim an unrun check passed.

## Git

- Preserve unrelated edits and staged selections; keep commits focused.
- Use Codex as the contributor for Codex-authored work.
- Push, publish, or release only when requested.
