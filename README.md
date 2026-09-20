# bioinfo-skills

Portable skills for bioinformatics and research, usable by Codex and Claude Code.

| Skill | Purpose |
| --- | --- |
| [biofolder](biofolder/SKILL.md) | Organize modality modules and agent/manual task workspaces; initialize Pixi, Git, and persistent project rules. |
| [research-flow](research-flow/SKILL.md) | Read workflow YAML as context for requested work, without automatically executing or changing the plan. |
| [consensus-mcp](consensus-mcp/SKILL.md) | Set up, repair, and use Consensus MCP for peer-reviewed literature search. |
| [semantic-scholar-literature-search](semantic-scholar-literature-search/SKILL.md) | Search the Semantic Scholar API, enrich records, and export literature tables. |
| [over-representation-analysis](over-representation-analysis/SKILL.md) | Run unranked-gene pathway ORA with GSEApy and MSigDB, including paired plots. |

## Start a project

```text
Use biofolder to initialize this project for bulk RNA-seq, proteomics, and
clinical metadata. Our goal is to identify disease-associated pathways.
Inspect existing files, ask for missing information, and use the default
Pixi environment. Reference datasets in place; do not run analyses yet.
```

Biofolder includes a [full example tree](biofolder/references/project-layout.md),
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

To read that plan:

```text
Use research-flow to explain which tasks the multimodal integration depends on.
Read docs/workflow.yaml.
```

For the visual editor, see the [Research Flow installation guide](https://github.com/SpicyChicken6/research-flow/blob/main/docs/install.md)
and [releases](https://github.com/SpicyChicken6/research-flow/releases).

## Analysis examples

- [Consensus search and setup](consensus-mcp/examples/example_prompt.md)
- [Semantic Scholar literature search](semantic-scholar-literature-search/examples/example_prompt.md)
- [Pathway over-representation analysis](over-representation-analysis/examples/example_prompt.md)
