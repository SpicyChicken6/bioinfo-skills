# Git tracking and session checkpoints

Use Git for every project. These rules authorize reviewed **local commits** for
initialization, completed agent work, and eligible stale changes. They do not
authorize pushing, adding a remote, publishing data, or editing human files.
Respect explicit read-only or no-commit instructions for the current session.

## Initialize once

Inspect the project and its ancestors for an existing repository, including
linked worktrees. Reuse the correct repository; do not create a nested repository
inside an existing one. For a standalone project without Git, run `git init` at
the project root. If its repository also contains other projects, restrict all
staging and commits to the requested project's paths.

Review `.gitignore` before staging the initial scaffold. Track code, tests,
instructions, READMEs, workflow/configuration files, the Pixi manifest and real
lockfile, and deliberately selected small artifacts. Keep raw/private datasets,
large generated outputs, environments, credentials, caches, and disposable logs
out of ordinary Git. Track appropriate data manifests, source references and
checksums instead of duplicating those datasets. Preserve existing data-tracking
policies; ignoring a path does not untrack content already committed. Do not
blanket-ignore `agent/`, `manual/`, or all useful task documentation.

Create an initial commit of the reviewed scaffold when Git identity and hooks
permit. Preserve configured identity; do not invent an author or disable hooks
to make setup appear complete. Report an unresolved commit blocker and continue
independent initialization work.

## Check at the start of every session

Before changing files, inspect the current branch and complete working state:

```bash
git status --short --branch --untracked-files=all
git diff
git diff --cached
```

Also check for unresolved conflicts or an ongoing merge, rebase, cherry-pick, or
revert. Understand pre-existing changes and distinguish them from this session's
work. Do not commit automatically during such an operation or on a detached
HEAD. Preserve existing staged work. Proceed with a nonempty index only when its
entire selection is reviewed, attributable, and eligible for the same checkpoint;
otherwise defer rather than incorporating or rearranging that selection.

### Determine age conservatively

Git does not record the age of an uncommitted change. Filesystem modification
times and the latest commit time are hints, never proof that a change is old.
Use a small, worktree-local observation ledger at the path returned by:

```bash
git rev-parse --git-path biofolder-session.json
```

Use the same schema across agents so subsequent sessions can compare observations:

- Top-level fields: `version` is `1`; `worktree` is the canonical absolute Git
  repository-root path; `entries` is an object keyed by repository-relative path.
- Each entry has `first_seen_utc` (ISO 8601 UTC) and a `fingerprint` object with
  exactly `head`, `index`, and `working_tree` comparison fields.
- `head` and `index` are `[Git mode string, object ID]`, or `null` when absent.
  `working_tree` is `[Git mode string, SHA-256 of raw file bytes]`, or `null` when
  absent. Use `100644` for ordinary files, `100755` for executable files, and
  `120000` for symlinks; hash a symlink's target text bytes without following it.
- These states describe additions, modifications, and deletions, including
  untracked files. Store rename source and destination as separate paths. Defer
  unsupported file types. Compare fields structurally, not a hash of JSON text.

Store hashes and metadata, never file contents. In a repository containing more
than one project, update entries within the requested project and preserve other
projects' entries.

On each check, retain the timestamp only for an identical fingerprint. Reset it
to now when the observed version changes; remove entries that are clean or no
longer eligible. A missing, malformed, incompatible, or foreign ledger means
age is unknown: start a fresh observation rather than inferring old age. Treat
invalid/future timestamps as unknown. Keep the ledger in Git's administrative
directory, not among tracked project files.

A version qualifies after it has been observed unchanged for **at least 24
hours**. Newly encountered changes must wait for a later observation. This is a
conservative measure of observed age, not a claim about when the work began.
The agent maintains this bookkeeping during sessions; biofolder installs no
background scheduler, Git hook, or automatic checkpoint helper.

## Make a reviewed checkpoint

Review each eligible diff and untracked file. Include only understood,
attributable project changes suitable for Git. Include existing human/manual work
only when covered by explicit project tracking policy or user scope; preserve its
ownership and provenance. This grants no permission to edit those files. Skip
ambiguous changes, sensitive/large files, and changes outside this project.
Keep related files together; defer a stale file if committing it alone would
omit required newer dependencies or only one side of a rename.

Recheck the index and candidate fingerprints immediately before staging. Stage
explicit paths with `git add -- <paths>`; do not use blanket `git add .` or
`git add -A`. Review the staged diff and recheck that it contains only the chosen
snapshot before committing. If concurrent changes interfere, stop the checkpoint
and preserve that work. Do not reset, stash, discard changes, or bypass hooks to
force a clean tree. Use a factual message such as `chore: checkpoint pre-existing
project work`; a checkpoint does not mean results are validated or accepted.

Refresh the ledger and inspect status after a successful commit. Summarize what
was committed and any remaining changes or blockers. Uncertainty or a blocked
checkpoint need not stop unrelated authorized work or trigger repeated approval
requests. Push only when the user has authorized publication.

At session end, review and commit coherent changes made for the requested work
without waiting 24 hours, preserving unrelated files and staged selections.
Report validation actually performed and anything intentionally left uncommitted.
