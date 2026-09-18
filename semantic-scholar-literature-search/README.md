# Semantic Scholar Literature Search

An API-based skill for paper discovery, seed recommendations, metadata exports, and literature triage.

See [SKILL.md](SKILL.md) for agent instructions and the [example request](examples/example_prompt.md) for usage. The [Python helper](scripts/s2_literature_search.py) requires `requests`; provide `S2_API_KEY` in the environment when available. Outputs include JSONL records, optional CSV tables, and a concise synthesis.

Full-text reading and formal systematic reviews require additional sources and methods.
