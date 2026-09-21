---
name: consensus-mcp
description: Set up, repair, and use Consensus for academic literature search and query-relevant full-text excerpts. Use for Consensus MCP/OAuth problems, evidence-focused paper searches, or reading methods and results through MCP or the API.
---

# Consensus MCP

The official MCP endpoint is `https://mcp.consensus.app/mcp`; the `/mcp` path is
required. For API-key access, use the REST fallback below.

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

A paid-feature rejection does not prove the user lacks a subscription. Check
that OAuth used the account with the paid plan. After switching accounts or
refreshing OAuth, reconnect the live MCP session or restart the client before
retesting; an existing session can retain the previous authentication.

Never put OAuth tokens or API keys in prompts, logs, commits, or public config.
For enterprise Bearer-token authentication, use environment variables or the
client's secret store.

## Evidence search

Use specific academic questions. Apply study-design, year, human-subject, or
other filters when the user requests that scope; do not silently narrow an
unrestricted search. Use `exclude_preprints` for a peer-reviewed-only request.

Inspect the live tool schema. The official MCP `search` supports
`include_full_text_chunks`; a separate Consensus app connector may expose
different `search`/`fetch` tools without that parameter. A fetched abstract and
metadata do not establish that the article body was retrieved.

## Full-text excerpts

For methods, numerical results, or limitations beyond the abstract, call the
official MCP `search` with a focused query and `include_full_text_chunks=true`:

```json
{
  "query": "How does DESeq2 estimate gene-wise dispersion and shrink it toward a fitted trend in RNA-seq analysis?",
  "include_full_text_chunks": true,
  "page_size": 3
}
```

Inspect the actual output: MCP can return rendered paper records with labeled
excerpts; REST returns `results[].full_text_chunks` as a nullable list of strings.
Split each string on the first `|` to separate the section label from the passage.
Keep each passage with its paper title, DOI when present, exact returned URL,
and section. Section labels may be coarse or repeat the title. Follow the live
tool's citation requirements and distinguish excerpts from abstract-only evidence.

The feature requires Pro, Deep, Teams, or Enterprise access. It supplies selected
passages from eligible open-access PDFs, with at most 3 per paper and 60 per
request. Retracted papers and publisher-partner paywalled text are excluded.
Add `open_access=true` only when that restriction fits the requested scope.

Missing, null, or empty excerpts mean none were returned, not that no full text
exists. Eligibility, query relevance, or selection across the result page can
explain this. A focused follow-up may help; otherwise label the abstract/takeaway
fallback explicitly. Excerpts can repeat the abstract, so verify that a passage
contains body detail before claiming retrieval beyond the abstract.

These passages are not a complete article. Equations, tables, figures, and
supplementary material may be incomplete or absent. Follow the DOI or source
article/PDF when the requested detail or formatting is missing; do not imply
that the whole paper was read.

## REST fallback

When MCP is unavailable or lacks the excerpt option, use an authorized API key
with `GET https://api.consensus.app/v1/search` and the `x-api-key` header. An OAuth
token is not an API key. The bundled Python 3 helper requests excerpts and emits
the original JSON, preserving abstracts, passages, and citation metadata:

```bash
python3 scripts/search_full_text.py \
  "How does DESeq2 estimate and shrink gene-wise dispersion?" \
  --page-size 3 > /tmp/consensus-excerpts.json
```

Run from this skill's directory or use the helper's absolute path. It reads
`CONSENSUS_API_KEY` first, then `~/.config/consensus/api-key`; `--key-file` selects
another file. Store a user-authorized key outside the repository with owner-only
permissions (`0600`). Never pass the key as a command-line argument or embed it
in the skill. `--open-access` is optional; ordinary topical filters are omitted.

For `401`, check the key; for `403`, check the account and feature entitlement.
For `429`, distinguish a temporary rate limit from exhausted monthly usage
before retrying. Do not silently remove the excerpt flag and call abstract-only
results a successful full-text test.

Verify with returned passages, not just login or a successful HTTP status.
See [example requests](examples/example_prompt.md), the
[full-text guide](https://docs.consensus.app/api-full-text), and the
[endpoint reference](https://docs.consensus.app/api-reference/query-for-relevant-papers).
