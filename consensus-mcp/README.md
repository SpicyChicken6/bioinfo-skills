# Consensus MCP

Portable guidance for connecting Claude or Codex to Consensus, repairing OAuth,
searching academic evidence, and retrieving query-relevant full-text excerpts.

- [Skill instructions](SKILL.md): client commands, verification, recovery, search
  filters, full-text evidence limits, and an API-key fallback.
- [REST helper](scripts/search_full_text.py): Python 3, no extra dependencies;
  reads an environment variable or a private local key file.
- [Example request](examples/example_prompt.md).
- [Official Consensus MCP documentation](https://docs.consensus.app/consensus-mcp).
- [Full-text documentation](https://docs.consensus.app/api-full-text).

Invoke with: “Use the consensus-mcp skill to verify my connection and search for
peer-reviewed evidence on my research question, requesting full-text excerpts
for methods and results.” Excerpts are selected passages, not whole articles.
