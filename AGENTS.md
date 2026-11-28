# Working in this repository

Instructions for AI agents working in this repository, and the rules a human owns
when an agent works on their behalf. Reachable as `CLAUDE.md`, a symlink, so
harnesses that look for that name find this file.

This copy was adapted from `COMPASS-PSAAP/compass-template` on 2026-11-28. The
standing rules below, and the ones in `conventions/`, apply to every repository in the
organization; changes to them go to the template. The sections describing this
repository are its own.

This file holds the rules every task needs. The rest live in one file per topic,
listed in [Conventions](#conventions) with when to read each; read a file when the
task reaches its topic, not before.

## Contents

- [What this repository holds](#what-this-repository-holds)
- [Repository map](#repository-map)
- [Repository configuration](#repository-configuration)
- [What agents are for here](#what-agents-are-for-here)
- [Agent instructions](#agent-instructions)
  - [Ask a human first](#ask-a-human-first)
  - [Never](#never)
  - [How to work here](#how-to-work-here)
  - [Revision history discipline](#revision-history-discipline)
- [Conventions](#conventions)
- [Additional engineering conventions](#additional-engineering-conventions)

## What this repository holds

The COMPASS Spack package repository and the configuration that sets Spack up on
the center's HPC systems. `spack_pkgs/` holds two package namespaces: `compass`, for
packages COMPASS makes or uses, and `cupecs`, carried over from the CUP-ECS PSAAP-III
repository this one was forked from. `system_externals/` holds each system's Spack
configuration, chosen on each system by `system_externals/include.yaml`, and
`spack_setup_script.py` points a user's Spack at both. The applications built with
these packages live in their own repositories; this one owns only how Spack finds and
builds them. Changes here are tested on the HPC systems through the exchange in
`working/`.

## Repository map

| Path | Owns |
|---|---|
| `AGENTS.md` | This file. The rules every task needs, the repository map, and the index of `conventions/` and the HPC site pages. Inherited from the template; the sections describing this repository are its own, but standing-rule changes go back to the template |
| `CLAUDE.md` | A symlink to `AGENTS.md`. Edit `AGENTS.md`; never replace the symlink with a copy, or the two names drift |
| `conventions/` | The organization's standing rules, one topic per file, indexed in [Conventions](#conventions). Inherited from the template; changes go back to the template |
| `README.md` | Human-facing: what the packages need, how to set Spack up with them, how to add a package or a system, and how changes are tested on HPC systems |
| `CHANGELOG.md` | Concise history of changes to this repository, newest first, beginning with the template adoption |
| `LICENSE.md` | BSD 3-Clause, carried over from CUP-ECS. Changing it is the author's decision, not an agent's |
| `.github/` | The `working-directory` workflow. Changing a workflow or adding one is CI configuration and needs a human |
| `.gitignore` | Python bytecode kept out of the repository |
| `working/` | Optional exchange with HPC systems that agents may not run on: its protocol, scripts, and request and response templates. Requests and their results live only on feature branches; see `working/README.md`. Inherited from the template but changeable. This repository keeps no promoted results, so it has no `results/` |
| `spack_pkgs/` | The Spack package repository: `spack_repo/compass/` and `spack_repo/cupecs/`, each a namespace with its `repo.yaml` and `packages/` |
| `spack-repo-index.yaml` | The index that tells Spack where the two namespaces live in this repository |
| `system_externals/` | Each system's Spack configuration, in `system_externals/<system>/`, and `include.yaml`, which includes the right folder on each system |
| `spack_setup_script.py` | Sets up a user's Spack: adds this repository, includes `system_externals/include.yaml`, and with `-U` pulls updates |

## Repository configuration

**New repositories start from `COMPASS-PSAAP/compass-template`** — on
GitHub through "Use this template", or with
`gh repo create COMPASS-PSAAP/<name> --template COMPASS-PSAAP/compass-template`.

**Keep inherited files close to the template.** Drift is then visible as a diff
rather than buried in a rewrite. If possible, repository-specific additions to an 
inherited file go in a clearly marked "For This Repository" block at the end of it.
An improvement that belongs to every repository goes to the template as a pull request 
there.

Parts of the configuration will have nothing to act on. A pure-Python repository has
no use for `.clang-format` or its workflow, and a repository of prose has no use for
the Spack environments. Leaving them in place is the cheaper default; pruning them is
the author's call, and either way the decision is recorded in `CHANGELOG.md`
rather than left to be rediscovered.

## What agents are for here

An agent's output is a **proposal**, and it is not part of this repository until a
human has read it and merged it.

Work agents do well here, unsupervised: reading the repository and answering
questions about it, drafting an implementation on a branch, writing tests against a
stated specification, reproducing a failure, mechanical refactors with a green test
suite on both sides, and drafting prose for a human to argue with.

Work agents do badly here, and must not do alone: deciding what a result means,
choosing a threshold, resolving a disagreement between two documents, deciding that a
failing test was wrong, and anything whose cost lands on someone outside the session
— machine time, a collaborator's inbox, a published page, a merged branch.

## Agent instructions

Directions for AI agents, which the humans working with them should know too.

### Ask a human first

Stop and ask before any of these, and do not treat approval for one as approval for
the next:

- **Pushing to a shared branch**, force-pushing, or rewriting published history
- **Merging a pull request**, approving a review, or closing an issue
- **Creating an issue, a comment, a label, or a Project item**, on any repository.
  Draft it, and give a human the command that would post it
- **Submitting a batch job**, reserving nodes, or anything else that spends
  allocation hours
- **Installing into a shared environment** or modifying a shared module or Spack
  installation
- **Adding a dependency**, vendoring third-party code, or changing the license
- **Changing repository settings**, CI configuration, secrets, or branch protection
- **Deleting files, data, or results**, and anything whose undo is a restore from
  backup
- **Sending anything outside the repository** — publishing a page, opening an issue on
  another organization's repository, posting to an external service, or mailing a
  collaborator
- **A load-bearing rewrite.** A correction that invalidates a deliverable, a
  deadline, or a claim changes what the project can say. Write the proposal; apply it
  once it is accepted

### Never

- **Commit a secret** — a token, a key, a password, a certificate, a machine
  hostname-plus-credential pair — or a file that contains one. If a secret has 
  already been committed, stop and tell a human.
- **Send sensitive, export-controlled, proprietary, or unpublished collaborator
  material to an external service without permission.** Unpublished results and
  code shared under an agreement are included. By starting a session the human
  authorizes sending this repository's contents to the model behind it, but that
  does not authorize sending restricted third-party material anywhere. When in
  doubt, treat information as restricted and ask.
- **Invent a result, a number, a date, or a citation.** An unverified reference is
  marked unverified. A number you did not compute is not reported.
- **Make a test pass by weakening it, skipping it, or asserting what the code does.**
  A failing test is a finding.
- **Report work as done that was not run.** If the tests were not run, say so; if a
  step was skipped, say which.
- **Write in someone's voice about what they did.** Text that asserts what the authors
  chose, observed, understood, or learned comes from those people. See
  [Writing](conventions/writing.md).
- **Reach an LLNL or CARC system from outside it**, whether through SSH or a
  person's tmux session. Write a request, or draft commands a person may choose to
  run there themselves. An agent on an LLNL system runs only inside LC's sandboxed
  harness with a lab-approved model endpoint, and launches jobs only within an
  allocation a person created. No agent runs on a CARC system, such as Easley or
  Hopper, or takes part in running requests, until documented authorization
  exists. See
  [Machines, allocations, and data](conventions/machines.md).
- **Edit `LICENSE`**, or replace the `CLAUDE.md` symlink with a copy.

### How to work here

- **Re-read the files at the start of each task.** They change between sessions and
  outside them. Do not act on a remembered version, including one recalled from
  memory; memory records what was true when it was written.
- **Keep user edits.** People edit these files directly. Never revert an edit you did
  not make, and never regenerate a file wholesale when an edit will do.
- **Keep the diff small and reviewable.** A large reflow hides the substantive change
  inside it, and a reviewer who cannot see the change cannot catch the error.
- **Match the surrounding code and prose.** Naming, comment density, wrapping, and
  idiom. A patch that reads as if it came from somewhere else costs a reviewer twice.
- **Never remove a comment**, and never delete a claim to resolve a disagreement.
  Revise it and record the revision. 
- **Retire, do not erase.** When a decision is reversed, say so where the decision
  lives and in `CHANGELOG.md`. Retired decisions that vanish come back.
- **Update the cross-references you invalidate.** Section numbers, filenames, symbol
  names, and issue IDs are cited across files; grep for the identifier you moved.
- **Say what you are unsure of.** An open question written down is cheap; a guess
  hardened into an implementation is not.

### Revision history discipline

Each substantive change is recorded concisely in `CHANGELOG.md`, newest first.
Say what changed and why, with the date. Editorial cleanups need no entry.

## Conventions

The organization's standing rules beyond this file, one topic per file. Read each
when the task reaches its topic.

| File | Read when |
|---|---|
| [`conventions/git-and-prs.md`](conventions/git-and-prs.md) | Branching, committing, or opening a pull request |
| [`conventions/evidence.md`](conventions/evidence.md) | Reporting a number, a result, or a claim, in a document or a pull request |
| [`conventions/writing.md`](conventions/writing.md) | Writing prose someone else will read |
| [`conventions/documentation.md`](conventions/documentation.md) | Changing `docs/`, a doc comment, or the documentation site, or publishing it |
| [`conventions/issues-and-projects.md`](conventions/issues-and-projects.md) | Drafting an issue or a comment, opening a research question, or setting up how a repository manages its work |
| [`conventions/artifacts.md`](conventions/artifacts.md) | Producing a figure, a table, a script, or a page someone else will use |
| [`conventions/machines.md`](conventions/machines.md) | Building, testing, or measuring on an HPC system, or handling data |
| [`conventions/memory.md`](conventions/memory.md) | Starting from an earlier session's notes, or ending a session |
| [`conventions/humans.md`](conventions/humans.md) | Running agents, following the feature loop, or reviewing their work |
| [`systems/README.md`](https://github.com/COMPASS-PSAAP/compass-hub/blob/main/systems/README.md) in `compass-hub` | Writing an HPC request for a particular machine, or reading its results. Read a page with `gh api repos/COMPASS-PSAAP/compass-hub/contents/systems/<page> -H "Accept: application/vnd.github.raw"` |

## Additional engineering conventions

- **Spack 1.2 or newer**, with the builtin repository from `releases/v2026.06`, as
  `README.md` says; older builtin releases cannot load the `cupecs` Cabana package.
- **Test a package or system change on the systems it affects**, through a request in
  `working/`; an agent cannot build on them itself.
- **Version each system file.** Each file in `system_externals/` carries a version
  number; raise it with each change, so versions can be compared across systems.
- **Python runs in a virtual environment** when it needs packages beyond the standard
  library; `spack_setup_script.py` needs none.
- **Determinism.** Same inputs, same outputs. Seed anything sampled and record the
  seed.
- **Inline single-use variables and functions**, prefer self-documenting code to
  explanatory comments, and follow YAGNI and DRY.

## For This Repository

- **Nothing is promoted.** This repository keeps no `results/`, so the steps in
  `conventions/machines.md` and `working/README.md` for proposing results or large
  files to promote into Git LFS do not apply here. Large files stay in each
  machine's store, and when a branch retires, remind a person to run
  `working/bin/clean-large` on each machine its requests ran on.
