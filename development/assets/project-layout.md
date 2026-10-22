# Project layout

Example for a frontend/backend project. Adapt it and create folders as needed.

```text
project/
├── README.md
├── AGENTS.md
├── DESIGN.md                 # Web UI projects
├── pyproject.toml            # Or pixi.toml
├── pixi.lock
├── frontend/
│   ├── src/
│   │   ├── assets/           # Imported images, fonts, illustrations
│   │   ├── components/
│   │   └── styles/
│   ├── public/               # Fixed-URL files, e.g. favicon
│   └── package.json
├── backend/
│   └── src/
├── packages/                 # Optional shared libraries
├── docs/
│   ├── project-layout.md
│   └── workflow.yaml
├── .moon/                    # Optional moon configuration
├── tests/                    # Or tests within each package
└── tasks/                    # Optional experiments and notes
```

For a CLI/library, use `src/<package>/` instead of frontend/backend folders.
Group multiple applications under `apps/` when useful. Keep JavaScript lockfiles
at the package or workspace root, matching the package-manager setup.
