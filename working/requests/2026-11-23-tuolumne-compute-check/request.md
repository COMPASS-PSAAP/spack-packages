# Request: 2026-11-23-tuolumne-compute-check

- **Asked for by:** Claude Code, for patrickb314, 2026-11-23
- **Machine:** Tuolumne, login node
- **Allocation:** login node; `run.sh` also submits one five-minute,
  one-node job with `flux run -N 1 -t 5m`
- **Expected cost:** at most 0.1 node-hours
- **Depends on:** nothing outside this branch

## Why

`2026-11-23-tuolumne-hostname-check` showed Spack choosing `compass-tuolumne` on
the login node, but its compute job listed no compass scope. That check
kept its temporary user scope under `$TMPDIR`, which was in
`/var/tmp` and is probably not visible from compute nodes, so the
failure is likely the check's, not `include.yaml`'s. The check now
keeps the scope in `~/.system-check.*` and prints the full scope list
on the compute node. This run answers whether Spack lists a
`compass-tuolumne` scope on a compute node. If it still does not,
`compute.txt` shows which scopes Spack did see.

## Before running

Load Spack 1.2.2. The check uses a temporary user scope in
`~/.system-check.*`, holding only this checkout's `include.yaml`,
removes it at the end, and installs nothing.

## Run

From the repository root:

    working/bin/run-request working/requests/2026-11-23-tuolumne-compute-check

## Results to return

The same files as `2026-11-23-tuolumne-hostname-check`; `compute.txt` is
the one this run is for.
