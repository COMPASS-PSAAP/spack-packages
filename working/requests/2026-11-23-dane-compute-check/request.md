# Request: 2026-11-23-dane-compute-check

- **Asked for by:** Claude Code, for patrickb314, 2026-11-23
- **Machine:** Dane, login node
- **Allocation:** login node; `run.sh` also submits one five-minute,
  one-node job with `srun -N 1 -n 1 -t 00`
- **Expected cost:** at most 0.1 node-hours
- **Depends on:** nothing outside this branch

## Why

`2026-11-23-dane-hostname-check` showed Spack choosing `compass-dane` on
the login node, but its compute job listed no compass scope. That check
kept its temporary user scope under `$TMPDIR`, which was in
`/var/tmp` and is probably not visible from compute nodes, so the
failure is likely the check's, not `include.yaml`'s. The check now
keeps the scope in `~/.system-check.*` and prints the full scope list
on the compute node. This run answers whether Spack lists a
`compass-dane` scope on a compute node. If it still does not,
`compute.txt` shows which scopes Spack did see.

## Before running

Load Spack 1.2.2. The check uses a temporary user scope in
`~/.system-check.*`, holding only this checkout's `include.yaml`,
removes it at the end, and installs nothing.05:00: If `srun` needs an account, set `SLURM_ACCOUNT` before running.

## Run

From the repository root:

    working/bin/run-request working/requests/2026-11-23-dane-compute-check

## Results to return

The same files as `2026-11-23-dane-hostname-check`; `compute.txt` is
the one this run is for.
