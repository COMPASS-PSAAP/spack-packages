# Exchanging work with the HPC systems

Agents may not run on LLNL systems or on Easley. When an agent needs a
build, a test, or a measurement from one of them, it writes a request on
a feature branch; a person reads the request, runs it, and commits the
results to the same branch; the agent pulls the results and continues.
This directory holds those requests and the scripts that move them.

The exchange is optional. A repository that never runs on HPC systems
deletes `working/`, `results/`, and
`.github/workflows/working-directory.yml`, and records that in
`CHANGELOG.md`.

Only the skeleton of this directory merges into the default branch: this
file, `bin/`, and `template/`. Requests live on feature branches, and the
"Working Directory Check" workflow fails any pull request into the default
branch that still contains them. A repository with other long-lived
branches, such as `develop`, adds them to the workflow's condition.

## Layout

| Path | Holds |
|---|---|
| `README.md` | This protocol |
| `bin/new-request` | Agent: create a request from `template/` |
| `bin/run-request` | Person: run a request on an HPC system and commit its results |
| `bin/check` | CI and anyone: the size limit, and with `--merge`, the skeleton-only rule |
| `template/` | The `request.md` and `run.sh` each request starts from |
| `requests/<date>-<topic>/` | One request per round trip, on a feature branch only |

A request directory holds:

- `request.md`: why the run is needed, the machine and allocation, the
  expected node-hours, any other repositories or branches it builds, and
  what it sends back
- `run.sh`: the commands, run from the repository root, which copy their
  artifacts into `$RESULTS_DIR`
- `results/`: written only by `run-request`, never by an agent:
  `stdout.log`, `manifest.md` (commit, host, start time, elapsed time,
  exit status, Spack version, and an allowlisted set of environment
  variables), and the artifacts `run.sh` copied

## The round trip

1. **The agent writes a request.** `working/bin/new-request <topic>`
   creates `working/requests/<today>-<topic>/`. The agent fills in
   `request.md` and `run.sh`, commits them, and pushes the feature branch.
2. **The person reviews it.** Read `request.md` and every line of
   `run.sh`. Running it spends allocation time and is the person's
   decision; change it or send it back rather than run something unclear.
3. **The person runs it.** On the HPC system, check out the branch, pull,
   start the allocation `request.md` names, and run
   `working/bin/run-request working/requests/<name>`. The script refuses
   to run from a checkout with uncommitted changes, from a commit not on
   `origin`, or from a checkout behind its branch on `origin`, where the
   agent may have revised the request; so the manifest names exactly the
   code that ran, and it is the current request. It
   commits `results/` and pushes; `--no-push` leaves the push to you.
4. **The agent reads the results.** It pulls the branch and works from
   `results/`. A failed run is a result, not a reason to edit it.

A request is never edited after it runs. A changed or repeated run is a
new request, so the branch history shows what ran, when, and with which
script.

## Rules

- **1 MiB per file.** `run-request` compresses larger files, and moves
  any still too large to `~/<repository>-oversize/<name>/` on the machine, where
  the manifest lists them. `bin/check` enforces the limit in CI. Ask for
  the specific lines or numbers needed rather than whole build trees.
- **No secrets, and nothing restricted.** The manifest records only
  allowlisted environment variables. Commit results only where the
  repository's visibility and the machine's policy allow it, and ask a
  person when unsure; see `AGENTS.md` in `COMPASS-PSAAP/compass-template`,
  "Machines, allocations, and data".
- **Agents never write `results/`** and never edit a request that has run.
- **Every request states its expected node-hours.**

## Writing `run.sh`

These come from the first exchange, in `COMPASS-PSAAP/fumata`, where
five of its requests ran on Tuolumne and stopped on a script bug instead
of the experiment.

- **Find the request's own files from the script's path.**
  `run-request` runs `bash <absolute path>/run.sh` from the repository
  root, so use `$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)`; joining
  `$(pwd)` to `$(dirname "${BASH_SOURCE[0]}")` doubles the path.
- **Write for `set -euo pipefail`.** A function that reads another
  function's `local` variables fails under `-u` once that function has
  returned; keep shared state in globals. A pipe that a reader closes
  early, such as `sort | head`, exits 141 under `pipefail`; end it with
  `|| true` where that is expected.
- **Keep to bash 3.2.** macOS still ships it, so a script that avoids
  `declare -A`, `local -n`, and other bash 4 features can be tested on a
  laptop.
- **Test before pushing, the way `run-request` runs it.** Run
  `RESULTS_DIR=<scratch> bash $(pwd)/working/requests/<name>/run.sh`
  against stubs for Spack and the application, so path, strict-mode, and
  parsing bugs show up before they cost an allocation.
- **Check inputs before the experiment.** Stop with a plain message when
  an input file, an executable, or a patched dependency is missing, by
  checking the installed file itself, rather than letting every run fail
  the same way.

## Keeping a result

Most exchanged output is disposable. A result a pull request relies on,
or a baseline, is promoted: a person copies the whole request directory,
with `request.md`, `run.sh`, and `results/`, into `results/` at the top of
the repository, following `results/README.md`, or copies its artifacts
into the tests with its `manifest.md`, so they record their source. Promotion
is a person's decision; an agent may propose it.

## Merging

Before a feature branch's pull request into the default branch is
merged, promote what should be kept, then remove the requests:

    git rm -r working/requests
    git commit -m "Remove exchanged requests before merging"
    working/bin/check --merge

Merge with a squash merge, so the exchanged files never enter the history
of the default branch. The feature branch keeps the full exchange for as
long as the branch exists.
