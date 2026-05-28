# Grill Me Skill

A lightweight, portable skill for Claude Code and Codex that runs a structured, constructive design review by asking probing questions and then offering recommended answers.

It is domain-agnostic and works well for bioinformatics pipelines, analysis plans, and software designs alike.

It focuses on:

- stress-testing plans across scope, requirements, assumptions, and constraints
- probing architecture, data flows, and failure modes
- covering testing, deployment, and monitoring
- asking one focused question at a time, then giving a recommended answer and rationale
- bounding traversal to the highest-impact decision branches
- using the codebase to answer questions when read access is available
- driving toward explicit consensus on each major decision

The skill is intentionally collaborative, not adversarial. It exposes gaps, then proposes next steps.

## Scope and domains

The review explicitly covers: **scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring**.

Traversal is bounded to the top 3 decision branches by impact and 3 levels deep per branch, with a summary of remaining branches before continuing.

## How it works

For each decision node:

1. Ask a single, focused question.
2. Wait for your response.
3. Provide a recommended answer and rationale, noting interdependencies with earlier decisions.

It stops when you confirm agreement on each major decision, or after resolving 8–10 key decisions, then summarizes and asks whether to continue.

## Recommended usage

```text
Use the grill-me skill. Stress-test my plan below. Ask one question at a time, then give your recommended answer and rationale before moving on.

Plan:
...
```

If you have not written a plan yet, the skill can start by asking an initial set of questions to capture it.
