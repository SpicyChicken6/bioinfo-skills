# Main Workflow Guide

This guide describes what the generated `main.nf` should contain.

## Required elements

1. Enable DSL2.
2. Define input parameters.
3. Define output directory parameter.
4. Include local modules from `modules/local`.
5. Create input channels from user-provided files.
6. Connect each process output to the next process input.
7. Keep final outputs under `results` or the user-provided output directory.

## Recommended parameters

- `params.input`
- `params.metadata`
- `params.outdir`
- `params.container`
- `params.profile`

## Recommended run flags

Use resume, report, trace, and timeline output during real runs.

## Notes

For a simple one-step workflow, keep `main.nf` short and readable. For multi-step workflows, split each logical step into a separate module under `modules/local`.
