# Development guidance

- Choose a maintained stack; use frameworks, libraries, and build tools where
  they simplify development.
- Prefer a monorepo for related applications and libraries. Separate frontend
  and backend responsibilities; create shared packages only for actual reuse.
- Use one root Pixi workspace for runtimes and development tools: `pyproject.toml`
  for Python projects, `pixi.toml` otherwise. Commit manifests and lockfiles,
  use `pixi run`, and avoid global or untracked installs. Document exceptions.
- Manage JavaScript dependencies with npm or pnpm; use workspaces when
  coordinating multiple packages.
- [moon](https://moonrepo.dev/docs) is optional for dependency graphs and task
  coordination. Keep its tasks in Pixi-managed environments without competing
  runtime installations; declare dependencies it cannot infer.
- Keep checks focused on changed behavior and meaningful regressions. Avoid
  trivial tests and unnecessary full-suite reruns; broaden testing as features
  stabilize or risk warrants.
- Keep README.md current and follow DESIGN.md for web UI work. See
  [project-layout.md](docs/project-layout.md) for structure examples.
- Keep components and development plans in `docs/workflow.yaml`. Refresh its
  read-only preview after edits using the README command. Report failures and
  identify any older preview as stale.
- Use Codex as the contributor for Codex-authored GitHub work.
