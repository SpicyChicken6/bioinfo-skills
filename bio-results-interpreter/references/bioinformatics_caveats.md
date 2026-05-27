# Bioinformatics Interpretation Caveats

## Differential expression

Check whether conclusions account for:

- effect size, not only adjusted p-value
- sample size and biological replicates
- model design and covariates
- multiple-testing correction
- directionality
- batch effects
- cell-type composition effects if bulk data

## Single-cell analysis

Check whether conclusions account for:

- sample-level replication
- pseudoreplication
- cell-type annotation uncertainty
- batch effects
- doublets
- ambient RNA
- cluster resolution dependence
- cell composition versus cell-intrinsic expression
- donor/sample imbalance

## Pathway enrichment

Check whether conclusions account for:

- direction of enrichment
- leading-edge/core genes
- redundancy among gene sets
- whether pathway activity was directly measured
- whether changes are driven by a few highly expressed genes

## Epigenomics

Check whether conclusions account for:

- peak calling thresholds
- normalization strategy
- antibody quality or assay-specific bias
- promoter versus enhancer interpretation
- motif enrichment versus TF activity
- chromatin accessibility versus gene expression linkage

## Variant interpretation

Check whether conclusions account for:

- inheritance model
- variant consequence
- allele frequency
- segregation
- phenotype match
- functional evidence
- ClinVar/HGMD/OMIM evidence strength
- candidate versus diagnostic wording

## Model performance

Check whether conclusions account for:

- training versus validation performance
- external validation
- class imbalance
- data leakage
- calibration
- confidence intervals
- biological plausibility
