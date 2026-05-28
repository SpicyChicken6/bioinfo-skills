# Example prompt

Use the grill-me skill.

Stress-test the design below. Cover scope, requirements, assumptions, constraints, architecture, data flows, failure modes, testing, deployment, and monitoring.

Ask one focused question at a time and wait for my answer. After each answer, give your recommended answer and rationale, and flag any earlier decisions it depends on.

Design:

```text
A Nextflow pipeline that takes raw paired-end RNA-seq FASTQ files, runs QC and trimming,
aligns to a reference genome, quantifies gene counts, and produces a DESeq2
differential-expression report. It should be resumable and run on a SLURM cluster.
```

Priorities:

- focus on the top 3 highest-impact decisions first
- explicitly call out assumptions I have not stated
- stop and summarize once we have resolved the major decisions, then ask whether to continue

If the workspace contains relevant code or config, inspect it to answer questions before asking me, and report what you found.
