# Methods: <task name>

Record what actually ran. Label planned steps and unknown details explicitly;
update this document when inputs or methods change.

## Inputs

- Source files, dataset/reference versions, samples, and features.
- Data type, units/scale, dimensions, and relevant matrix/object/layer names.
- Preprocessing already applied, with links to upstream methods and any unknowns.

## Data processing

Describe all processing in execution order, including steps applied automatically
by analysis or plotting tools. Cover filtering, missing-value handling, normalization,
transformation/scaling, correction, and aggregation when applicable. State when
normalization or transformation was not applied; do not assume incoming data is raw.

Repeat the following block for each step:

### <number>. <processing step>

- **Input → output:** exact artifacts or objects/layers, units/scale, and
  sample/feature counts before and after where relevant.
- **Procedure:** software/version, function or command, code link, and exact
  parameters, thresholds, formulas, and material defaults.
- **Scope:** samples/features, groups, and reference or fitting data used to
  estimate parameters; distinguish training and evaluation data when applicable.
- **Rationale:** why this procedure and these settings were used.
- **Checks:** criteria, observed values, exclusions, and links to diagnostics.

For **normalization**, specify the method, denominator/reference or scaling
factors and how they were obtained, applicable axis/groups, and resulting units.
For **transformations**, specify the formula, log base, pseudocount,
centering/scaling axis and reference, and handling of zeros, negative/missing
values, or clipping where applicable. Record any imputation and batch correction
with their parameters and place in the processing sequence.

## Analysis

- Methods, comparisons, model settings/covariates, and statistical thresholds
  or multiple-testing correction where applicable.
- Exact input artifact or object/layer and data scale used by each analysis.
- Inputs used for figures; include additional plot-specific processing above.

## Reproduction and outputs

- Code/notebook links, execution commands and working directory, run/version,
  environment/lockfile reference, and random seeds where applicable.
- Output paths, what they contain, and their processing state/units for reuse.
- Validation criteria and observed results, with links to evidence.

## Run summary and caveats

After each agent run on this task, including partial or failed runs, append a
concise dated entry before the final response. Preserve earlier entries and
carry forward relevant unresolved caveats; link evidence when marking them
resolved or superseded. Link this record from the final response.

### <date/time or run ID>

- **Status and outcome:** completed, partial, or failed; what ran, what changed,
  and the main observed findings.
- **Outputs and checks:** links to produced artifacts and validation evidence;
  checks that passed, failed, or were not performed.
- **Caveats:** warnings, limitations, and unresolved issues, including their
  effect on interpretation or reuse of the results.
- **Follow-up:** remaining work or decisions needed, if any.
