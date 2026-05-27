---
name: consensus-mcp
description: Set up, verify, repair, and use the official Consensus MCP server for peer-reviewed academic literature search in Claude Code, Claude Desktop, Codex, or other MCP clients. Use when the user asks about Consensus MCP installation, OAuth failures, missing Consensus tools, literature-search MCP setup, or evidence-focused paper search via Consensus.
---

# Consensus MCP

## Purpose

Connect an agent to the official Consensus MCP server and use it safely for peer-reviewed literature search.

The official endpoint is:

```text
https://mcp.consensus.app/mcp
```

The `/mcp` path is required.

## Correct Claude setup

For Claude Code:

```bash
claude mcp add --transport http consensus https://mcp.consensus.app/mcp
```

OAuth opens in the browser automatically on first use. To trigger authentication manually, type `/mcp` inside Claude Code.

For Claude Desktop:

1. Open Settings.
2. Open Connectors.
3. Select Browse Connectors.
4. Search for Consensus.
5. Click Connect and finish OAuth sign-in.

## Correct Codex setup

For Codex:

```bash
codex mcp add consensus --url https://mcp.consensus.app/mcp
codex mcp login consensus
```

Expected `~/.codex/config.toml` entry:

```toml
[mcp_servers.consensus]
url = "https://mcp.consensus.app/mcp"
```

Do not add the Codex server with `-- --transport http`. Codex OAuth login needs the URL-style streamable HTTP setup.

## Verify

In Codex:

```bash
codex mcp get consensus
codex doctor --json
```

Expected:

- `transport: streamable_http`
- URL exactly `https://mcp.consensus.app/mcp`
- `mcp.config` status `ok`

In Claude Code:

1. Type `/mcp`.
2. Confirm Consensus appears.
3. Try a small research query.

If many tools are installed, Claude Code may load Consensus tools on demand. Retry once if it says Consensus search has not loaded yet.

## Repair common failures

If no tools appear or the server fails:

1. Confirm the URL includes `/mcp`.
2. Remove and re-add the server.
3. Fully restart the client.

For Claude Code OAuth expiry or 401 errors:

1. Type `/mcp`.
2. Select Consensus.
3. Choose Clear authentication.
4. Re-authenticate.
5. Fully quit and restart Claude Code.

If Claude Code says authentication succeeded but reconnection failed, fully quit and restart Claude Code. Do not rely only on reconnect.

For Claude Desktop, disconnect and reconnect Consensus in Settings -> Connectors.

For Codex OAuth refresh, handshake, 401, expired-token, or parse-server-response errors:

```bash
codex mcp logout consensus
codex mcp login consensus
```

Then finish browser OAuth and fully restart Codex.

If Codex was added incorrectly:

```bash
codex mcp remove consensus
codex mcp add consensus --url https://mcp.consensus.app/mcp
codex mcp login consensus
```

## Search behavior

Use Consensus for evidence-focused research questions. Prefer specific academic queries over casual wording.

Good search constraints:

- ask for randomized controlled trials, systematic reviews, meta-analyses, or human studies when relevant
- include year ranges for recency-sensitive questions
- use `medical_mode` for clinical or evidence-based medicine questions
- use `exclude_preprints` when the user needs peer-reviewed-only results
- use `human` for human-subject evidence
- use `sample_size_min` when small studies are not useful

Example prompt:

```text
Use Consensus to find human systematic reviews and randomized controlled trials since 2020 on cognitive behavioral therapy for anxiety. Exclude preprints and summarize the strongest evidence with citations.
```

## Tool notes

Most MCP clients expose the Consensus `search` tool.

The `fetch` tool is currently available for ChatGPT only. Do not assume Claude Code, Claude Desktop, Codex, Cursor, VS Code, or Windsurf will expose `fetch`.

## Security

Only connect to:

```text
https://mcp.consensus.app/mcp
```

Do not paste OAuth tokens or API keys into prompts, logs, commits, or public config files. If an enterprise Bearer-token setup is used, store secrets in environment variables or the client secret store.
