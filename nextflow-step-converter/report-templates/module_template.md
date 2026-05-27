# Nextflow DSL2 Module Template

Use this as a guide when creating a process file under `modules/local/step_name.nf`.

## Required sections

- process name
- tag
- publishDir
- cpus, memory, and time
- input block
- output block
- script block
- optional stub block

## Example shape

```nextflow
process STEP_NAME {
    tag "$sample_id"

    publishDir "${params.outdir}/step_name", mode: 'copy'

    cpus 2
    memory '8 GB'
    time '2h'

    input:
    tuple val(sample_id), path(input_file)

    output:
    tuple val(sample_id), path("output.tsv"), emit: result

    script:
    """
    Rscript ${projectDir}/scripts/script_name.R --input ${input_file} --output output.tsv
    """

    stub:
    """
    echo 'stub output' > output.tsv
    """
}
```

## Notes

Keep the original analysis logic in the script. The Nextflow process should mainly define inputs, outputs, resources, and execution environment.
