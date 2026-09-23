# bioinfo-skills

Portable skills for bioinformatics and research, usable by Codex and Claude Code.

| Skill | Purpose |
| --- | --- |
| [biofolder](biofolder/SKILL.md) | Organize modality modules and agent/manual task workspaces; initialize Pixi and Git; upload manual results to a configured cloud drive. |
| [toolfolder](toolfolder/SKILL.md) | Organize reusable tools with shared source and tests, task workspaces, and components and development plans in workflow YAML. |
| [research-flow](research-flow/SKILL.md) | Read workflow YAML as context for requested work, without automatically executing or changing the plan. |
| [cellxgene-browser](cellxgene-browser/SKILL.md) | Set up and launch CELLxGENE Annotate for single-cell H5AD data, locally or over SSH. |
| [consensus-mcp](consensus-mcp/SKILL.md) | Search academic literature and retrieve full-text excerpts through Consensus MCP or its API. |
| [semantic-scholar-literature-search](semantic-scholar-literature-search/SKILL.md) | Search the Semantic Scholar API, enrich records, and export literature tables. |
| [over-representation-analysis](over-representation-analysis/SKILL.md) | Run unranked-gene pathway ORA with GSEApy and MSigDB, including paired plots. |

## Start a project

```text
Use biofolder to initialize this project for bulk RNA-seq, proteomics, and
clinical metadata. Our goal is to identify disease-associated pathways.
Inspect existing files, ask for missing information, and use the default
Pixi environment. Reference datasets in place; do not run analyses yet.
```

Biofolder includes a [project README template](biofolder/assets/project-README.md)
for project background and research questions, a
[full example tree](biofolder/references/project-layout.md),
[project instruction template](biofolder/assets/AGENTS.md), and
[starter environment](biofolder/references/pixi-environment.md) with Python, R,
and Research Flow. The project plan lives at `docs/workflow.yaml`.

Initialization also installs [module/task commands](biofolder/references/scaffold-commands.md):

```bash
pixi run add-module transcriptomics
pixi run add-task transcriptomics differential-expression
cd modules/transcriptomics
pixi run add-task enrichment
```

Modules are unnumbered; tasks receive the next number within their module.

Upload manual results with the [result sync command](biofolder/references/sync-results.md):

```bash
# Preview all modules, using a remote already configured in rclone.
pixi run sync-results --remote my-box --destination Project_Results

# Upload when ready; optionally select one module with --module.
pixi run sync-results --remote my-box --destination Project_Results --upload
```

The command copies `manual/results/`, `manual/figures/`, and `manual/tables/`,
preserving paths from `modules/` onward. Agent outputs are excluded, and files
already on the cloud drive are never deleted. Any configured rclone remote can
be used, including Box, OneDrive, and Google Drive.

To read that plan:

```text
Use research-flow to explain which tasks the multimodal integration depends on.
Read docs/workflow.yaml.
```

For the visual editor, see the [Research Flow installation guide](https://github.com/SpicyChicken6/research-flow/blob/main/docs/install.md)
and [releases](https://github.com/SpicyChicken6/research-flow/releases).

## Start a tool project

```text
Use toolfolder to initialize a reusable Python CLI for validating sample sheets.
Use Pixi, keep source and tests shared, and record components, relationships,
and development tasks in docs/workflow.yaml. Scaffold the project without
implementing the planned features yet.
```

Toolfolder includes an [example layout](toolfolder/references/project-layout.md),
[project instructions](toolfolder/assets/AGENTS.md), README templates, and a
[workflow example](toolfolder/examples/workflow.yaml). It keeps maintained code
outside task workspaces and uses the workflow for the component overview instead
of a separate architecture document.

## Analysis examples

- [Consensus search and setup](consensus-mcp/examples/example_prompt.md)
- [Semantic Scholar literature search](semantic-scholar-literature-search/examples/example_prompt.md)
- [Pathway over-representation analysis](over-representation-analysis/examples/example_prompt.md)
