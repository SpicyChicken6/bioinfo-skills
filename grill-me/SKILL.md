---
name: grill-me
description: Conduct a structured design review by asking probing questions about scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

## Overview

Adopt a rigorous but constructive tone: ask probing questions to expose gaps, then offer nonjudgmental recommended answers and next steps. This is a collaborative stress-test, not an adversarial interrogation.

## Scope & Domains

Cover these explicit domains: **scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring**. Limit traversal to the top 3 decision branches by impact, and to 3 levels deep per branch; summarize remaining branches and ask whether to continue.

## Initial Plan Capture

If the user has not supplied a plan or provides insufficient detail, respond: "Please provide the plan outline (goals, stakeholders, constraints, key decisions). If you prefer, I can start by asking an initial set of 6 questions to capture it."

## Question Flow & Sequencing

For each decision node (e.g., API choice, data model, deployment option):
1. Ask a single, focused question
2. Wait for the user's response
3. Then provide your recommended answer and rationale, including any interdependencies with prior decisions

Ask one question at a time and wait for the user's response before proceeding.

## Termination & Consensus

Stop when the user explicitly confirms "I agree" on each major decision node, or after resolving 8–10 key decisions. Otherwise, offer a summary of resolved decisions and ask whether to continue drilling into remaining branches.

## Handling Changes & Dependencies

If the user changes an earlier decision, re-evaluate dependent decisions and explicitly notify which prior resolutions are now invalid. Adjust your recommended answers accordingly.

## Codebase Exploration

**Priority rule**: If the workspace contains relevant code and you have read access, run static analysis or search for TODOs/comments/architecture docs to answer the question; report the findings and still ask any clarifying questions if results are incomplete.

If you do not have read access to the codebase or no codebase exists, say "codebase unavailable" and then ask the relevant clarifying question instead.

If codebase access fails or results are inconclusive, report the failure and then ask the single clarifying question that would resolve the uncertainty.

## User Pause or Refusal

If the user indicates they want to stop or pauses for extended time, ask whether to pause, save progress, or summarize findings. Do not continue unless the user consents.