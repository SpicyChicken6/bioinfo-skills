---
name: consensus-mcp
description: Set up, verify, repair, and use the official Consensus MCP server for academic literature search. Use for Consensus installation, missing tools, OAuth failures, or evidence-focused paper searches in Claude, Codex, and other MCP clients.
---

# Consensus MCP

Connect only to `https://mcp.consensus.app/mcp`; the `/mcp` path is required.

## Client setup

**Claude Code:**

```bash
claude mcp add --transport http consensus https://mcp.consensus.app/mcp
```

OAuth opens on first use; `/mcp` triggers it manually. Confirm Consensus appears
there and try a small query. With many installed tools, discovery may be deferred;
retry once if Consensus search has not loaded.

**Claude Desktop:** Settings → Connectors → Browse Connectors → Consensus →
Connect, then complete browser OAuth.

**Codex:**

```bash
codex mcp add consensus --url https://mcp.consensus.app/mcp
codex mcp login consensus
```

Codex OAuth requires URL-style streamable HTTP setup; do not use
`-- --transport http`. Confirm the exact endpoint and `streamable_http` transport,
then verify the connection with a real Consensus search query.

## Recovery and credentials

For missing tools, check the endpoint and registration. For authentication failures:

- **Claude Code:** `/mcp` → Consensus → Clear authentication, re-authenticate,
  then fully restart. If authentication succeeds but reconnection fails, a full
  restart is still required.
- **Claude Desktop:** disconnect and reconnect Consensus in Settings → Connectors.
- **Codex:** log out and refresh OAuth, complete browser sign-in, then fully
  restart. Re-register with the URL-style command if configured incorrectly.

Never put OAuth tokens or API keys in prompts, logs, commits, or public config.
For enterprise Bearer-token authentication, use environment variables or the
client's secret store.

## Evidence search

Use specific academic questions with relevant study designs (RCTs, systematic
reviews, meta-analyses), human-study constraints, and year ranges. Apply
`medical_mode` for clinical/evidence-based medicine questions, `exclude_preprints`
for peer-reviewed-only searches, `human` for human-subject evidence, and
`sample_size_min` when small studies are unsuitable.

Most clients expose `search`; `fetch` is available only for ChatGPT. Do not assume
Claude Code, Claude Desktop, Codex, Cursor, VS Code, or Windsurf exposes it.

See the [example request](examples/example_prompt.md).
