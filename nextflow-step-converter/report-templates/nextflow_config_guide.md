# Nextflow Config Guide

This guide describes what the generated `nextflow.config` should contain.

## Recommended sections

- default parameters
- process resource defaults
- profiles for local, docker, singularity, conda, slurm, or other HPC executors
- trace, report, timeline, and DAG settings when useful

## Recommended defaults

- output directory: `results`
- work directory: `work`
- publish mode: `copy`
- error strategy: `terminate` by default

## Profile suggestions

### local

Use for laptop or workstation testing.

### docker

Use when Docker containers are available.

### singularity

Use for HPC environments where Singularity or Apptainer is preferred.

### slurm

Use for cluster execution with Slurm.

## Notes

Keep config simple unless the user asks for nf-core style complexity. The goal is a readable workflow that can resume and produce traceable outputs.
