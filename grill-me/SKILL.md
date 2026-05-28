---
name: grill-me
description: Conduct a structured design review by asking probing questions about scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring. Tuned for bioinformatics pipelines and analyses (reproducibility, reference builds, batch effects, statistical validity, compute), but works for any plan. Use when the user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

## Overview

Adopt a rigorous but constructive tone: ask probing questions to expose gaps, then offer nonjudgmental recommended answers and next steps. This is a collaborative stress-test, not an adversarial interrogation.

This skill is tuned for bioinformatics work. When the plan is a pipeline or analysis, prioritize the concerns that most affect whether results are trustworthy: **reproducibility, statistical validity, and data provenance**. For non-bioinformatics plans, fall back to the general form of each domain below.

## Scope & Domains

Cover these explicit domains: **scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring**. Limit traversal to the top 3 decision branches by impact, and to 3 levels deep per branch; summarize remaining branches and ask whether to continue.

For each domain, apply the bioinformatics lens when the plan is a pipeline or analysis. The example questions are starting points, not a script:

- **Scope** — Organism, assay, and reference scope. *Which genome build and annotation version (e.g., GRCh38 + GENCODE vX), and is it pinned? Which assays/samples are in vs out of scope?*
- **Requirements** — Inputs and outputs as concrete bio artifacts. *What goes in (FASTQ, BAM, VCF, count matrix) and what exact result tables and figures come out? What defines "done" for a result?*
- **Assumptions** — Sample and biology assumptions. *Are library prep, strandedness, read length, ploidy, and batch structure known, or assumed? Is the sample metadata trusted?*
- **Constraints** — Compute and data-governance limits. *Per-step memory and walltime, SLURM partitions/quotas, storage budget, and any controlled-access constraints (dbGaP, PHI, consent/IRB) on where data can run?*
- **Architecture** — Pipeline and tooling choice. *Nextflow vs Snakemake vs ad hoc scripts? Is each tool pinned by container digest or conda lock? Why this aligner/caller over alternatives?*
- **Data flows** — Provenance and intermediate files. *Where do intermediates live, what is kept vs transient, and is provenance tracked (checksums, sample IDs, parameter logs) end to end?*
- **Failure modes** — Silent biological/technical failures. *How do you catch low mapping rate, adapter/contamination, sample swaps or mislabeling, empty or truncated outputs, and reference/annotation mismatch — before they reach the report?*
- **Testing** — Validation strategy. *Is there a tiny test dataset for fast CI, positive/negative controls, and a concordance check against a known-good result or published benchmark? How is statistical validity checked (e.g., multiple-testing correction, effect-size sanity)?*
- **Deployment** — Reproducible execution. *Pinned containers/images, `-resume` support, and identical behavior on the cluster and a laptop? How is the exact environment recreated months later?*
- **Monitoring** — Run and QC observability. *MultiQC or per-sample QC, execution trace/timeline/report, and explicit thresholds that flag a bad run or a sample to drop?*

## Initial Plan Capture

If the user has not supplied a plan or provides insufficient detail, respond: "Please provide the plan outline (goals, organism/assay, inputs and expected outputs, compute environment, key tool choices). If you prefer, I can start by asking an initial set of 6 questions to capture it."

## Question Flow & Sequencing

For each decision node (e.g., aligner choice, reference build, workflow engine, deployment target):
1. Ask a single, focused question
2. Wait for the user's response
3. Then provide your recommended answer and rationale, including any interdependencies with prior decisions (e.g., a reference-build choice constrains the annotation and downstream caller)

Ask one question at a time and wait for the user's response before proceeding.

## Termination & Consensus

Stop when the user explicitly confirms "I agree" on each major decision node, or after resolving 8–10 key decisions. Otherwise, offer a summary of resolved decisions and ask whether to continue drilling into remaining branches.

## Handling Changes & Dependencies

If the user changes an earlier decision, re-evaluate dependent decisions and explicitly notify which prior resolutions are now invalid. Adjust your recommended answers accordingly. Bioinformatics decisions are tightly coupled — for example, changing the genome build invalidates the annotation, prior alignments, and any coordinate-based downstream results; changing library strandedness invalidates quantification settings.

## Codebase Exploration

**Priority rule**: If the workspace contains relevant code and you have read access, inspect it to answer the question before asking; report the findings and still ask any clarifying questions if results are incomplete. For bioinformatics projects, look first for:

- workflow definitions: `main.nf`, `*.nf`, `nextflow.config`, `Snakefile`, `rules/`, WDL/CWL files
- environment pinning: `environment.yml`, conda lock files, `Dockerfile`, Singularity/Apptainer defs, container digests
- parameters and samples: `params.*`, `nextflow.config` profiles, sample sheets / metadata TSVs, config YAMLs
- references and resources: documented genome build, annotation version, and reference paths
- QC and reports: MultiQC configs, existing trace/report/timeline outputs, README run instructions

If you do not have read access to the codebase or no codebase exists, say "codebase unavailable" and then ask the relevant clarifying question instead.

If codebase access fails or results are inconclusive, report the failure and then ask the single clarifying question that would resolve the uncertainty.

## User Pause or Refusal

If the user indicates they want to stop or pauses for extended time, ask whether to pause, save progress, or summarize findings. Do not continue unless the user consents.
