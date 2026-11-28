# Exchanging work with the HPC systems

Agents do not reach the LLNL or CARC systems from outside them;
`conventions/machines.md` gives the rules. When an agent needs a build, a
test, or a measurement from one of them, it writes a request on a feature
branch; a person inspects the request and either runs it and commits the
results, or rejects it and commits a response saying why, to the same
branch; the agent pulls what came back and continues. This directory
holds those requests and the scripts that move them.

This repository uses the exchange only to test its system configuration
on the systems it manages, so it keeps no promoted results and has no
`results/` directory or `bin/promote`. Large files stay in each machine's
store until the branch retires. The template's copy of this file
describes promotion for repositories that need it.

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
| `bin/respond` | Person: reject a request that has not run, by creating its `response.md` |
| `bin/clean-large` | Person: delete a retired branch's large files from an HPC system |
| `bin/large-store` | The scripts: where this machine keeps a branch's large files |
| `bin/check` | CI and anyone: the size limit, and with `--merge`, the skeleton-only rule |
| `template/` | The `request.md` and `run.sh` each request starts from, and the `response.md` a rejection starts from |
| `requests/<date>-<topic>/` | One request per round trip, on a feature branch only |

A request directory holds:

- `request.md`: why the run is needed, the machine and allocation, the
  expected node-hours, any other repositories or branches it builds, and
  what it sends back
- `run.sh`: the commands, run from the repository root, which copy their
  artifacts into `$RESULTS_DIR` and write files too large to send back
  into `$LARGE_DIR`
- `results/`: written only by `run-request`, never by an agent:
  `stdout.log`, `manifest.md` (commit, host, start time, elapsed time,
  exit status, Spack version, an allowlisted set of environment
  variables, and the large files left on the machine), `large.sha256`
  when there are large files, and the artifacts `run.sh` copied
- `response.md`: written only by the inspector, never by the agent that
  asked, when the request is rejected instead of run: who inspected it,
  the reasons, what a new request needs, and room for a person to record
  how a dispute was settled. A request has `results/` or `response.md`,
  never both

## The round trip

1. **The agent writes a request.** `working/bin/new-request <topic>`
   creates `working/requests/<today>-<topic>/`. The agent fills in
   `request.md` and `run.sh`, commits them, and pushes the feature branch.
2. **The person inspects it.** Read `request.md` and every line of
   `run.sh`. Running it spends allocation time and is the person's
   decision; reject it rather than run something unclear, unsafe, or not
   worth its cost. To reject it, run
   `working/bin/respond working/requests/<name>`, fill in the
   `response.md` it creates, commit it, and push. `run-request` refuses
   a request that has a response.
3. **The person runs it.** On the HPC system, check out the branch, pull,
   start the allocation `request.md` names, and run
   `working/bin/run-request working/requests/<name>`. The script refuses
   to run from a checkout with uncommitted changes, from a commit not on
   `origin`, or from a checkout behind its branch on `origin`, where the
   agent may have revised the request; so the manifest names exactly the
   code that ran, and it is the current request. It
   commits `results/` and pushes; `--no-push` leaves the push to you.
4. **The agent reads what came back.** It pulls the branch and works
   from `results/`, or from `response.md`. A failed run is a result, not
   a reason to edit it. After a rejection, the agent writes a new request
   that addresses the response and names the rejected one, or tells its
   person why it disagrees; a person settles the disagreement and records
   the decision under Arbitration in `response.md`.

A request is never edited after it runs or is rejected. A changed or
repeated run is a new request, so the branch history shows what ran,
what was turned down, when, and with which script.

## Rules

- **1 MiB per file.** `run-request` compresses larger files in
  `results/`, and moves any still too large to `$LARGE_DIR`; see
  [Large files](#large-files). `bin/check` enforces the limit in CI. Ask
  for the specific lines or numbers needed rather than whole build trees.
- **No secrets, and nothing restricted.** The manifest records only
  allowlisted environment variables. Commit results only where the
  repository's visibility and the machine's policy allow it, and ask a
  person when unsure; see `conventions/machines.md`.
- **Agents never write `results/` or `response.md`** and never edit a
  request that has run or been rejected.
- **Every request states its expected node-hours.**

## Toward agents on the HPC systems

The exchange is meant to grow into one where a local agent pushes a
request, and an agent on an LLNL or CARC system, approved for the work
and running inside an allocation a person created, pulls it, inspects
it, and either runs it, committing `results/`, or rejects it, committing
`response.md`, then pushes. A person monitors the exchange and settles
disagreements between the two agents. It will be tried first on CARC's
Easley and Hopper. Following LC's guidance at
<https://hpc.llnl.gov/si-agents>, COMPASS already limits agents on LC
systems to LC's sandboxed harnesses, lab-approved model endpoints, and
allocations a person created.

None of this is in place yet. Until an agent has documentation that
specifically authorizes its part, from Patrick Bridges, the COMPASS PI,
or, for an LC system, from a representative of LC, it refuses to
inspect, run, or answer requests; a person does all three. The
documentation will be in `systems/carc.md` or `systems/llnl.md` in
`COMPASS-PSAAP/compass-hub`. See `conventions/machines.md`.

## Large files

Files over 1 MiB, such as captures, traces, and output from full-size
runs, stay on the HPC system that made them. Each machine keeps them in a
large-file store, in project storage that its jobs can reach and that is
never purged, since a file there may later need to be kept. Each site's
page in `systems/` in `COMPASS-PSAAP/compass-hub`, the organization's
hub, names its store. `bin/large-store` maps hosts to stores and to the
UNIX group that shares them; `run-request` gives that group read, write,
and delete access to what it stores, so anyone in the group can clean up
a run. A machine missing from `bin/large-store`
cannot run requests until someone adds it there and to its site's page.

In a store, each branch has a directory, and each request a directory in
that: `<store>/<repository>/<branch>/<request>/`, with each `/` in the
branch name replaced by `--`. `run-request` creates the request's
directory and passes it to `run.sh` as `$LARGE_DIR`. Afterward, the
manifest lists every file in it with its size, and `large.sha256` records
their SHA-256 sums.

- **Analyze large files on the machine.** They cannot come back through
  git, so `run.sh` reduces them to what the agent needs, such as a table
  of numbers or a plot, and copies that into `$RESULTS_DIR`. A later
  request may read an earlier request's large files, by the path in its
  manifest, to analyze them further; it never changes or deletes them.
- **Use scratch only for files nobody will keep**, such as checkpoints a
  run reads back or an analysis's temporary files. Each site's page in
  the hub's `systems/` says where its scratch is, whether it is purged,
  and who can reach it. `run.sh` deletes what it puts in scratch, since `bin/clean-large`
  cleans only the large-file store. Anything that may need to be kept
  goes in `$LARGE_DIR`.
- **State the expected size** in `request.md`, so the person running the
  request can check that the store has room.
- **Clean up when the branch retires**, whether it merges or is
  abandoned; see [Merging](#merging).

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
- **Write large output to `$LARGE_DIR`**, not to `$RESULTS_DIR` or the
  checkout, which may sit in a home directory with a small quota.
- **Check inputs before the experiment.** Stop with a plain message when
  an input file, an executable, or a patched dependency is missing, by
  checking the installed file itself, rather than letting every run fail
  the same way.

## Merging

Before a feature branch's pull request into the default branch is
merged, remove the requests:

    git rm -r working/requests
    git commit -m "Remove exchanged requests before merging"
    working/bin/check --merge

Merge with a squash merge, so the exchanged files never enter the history
of the default branch. The feature branch keeps the full exchange for as
long as the branch exists.

Once the branch is merged or abandoned, delete its large files from each
machine whose host appears in its manifests:

    working/bin/clean-large <branch>            # lists the files
    working/bin/clean-large --delete <branch>

Deleting is a person's decision; the files are gone for good.
