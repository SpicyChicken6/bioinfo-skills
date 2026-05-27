# Consensus MCP Skill

A lightweight portable skill for Claude Code and Codex that helps agents install, verify, repair, and use the official Consensus MCP server for peer-reviewed literature search.

It focuses on:

- correct HTTP MCP server setup
- Claude Code and Claude Desktop installation
- Codex installation
- OAuth re-authentication repair
- practical search-query discipline
- safe handling of tokens and API keys

## Install for Claude Code

```bash
claude mcp add --transport http consensus https://mcp.consensus.app/mcp
```

OAuth opens in your browser on first use. You can also trigger it manually with `/mcp`.

## Install for Codex

```bash
codex mcp add consensus --url https://mcp.consensus.app/mcp
codex mcp login consensus
```

## Install for Claude Desktop

Use Settings -> Connectors -> Browse Connectors, search for Consensus, then connect and finish OAuth sign-in.

## Recommended usage

```text
Use the consensus-mcp skill. Verify my Consensus MCP setup, repair OAuth if needed, then use Consensus to find recent human systematic reviews and RCTs on exercise for depression.
```

## Source

Official Consensus MCP documentation:

```text
https://docs.consensus.app/docs/mcp
```
