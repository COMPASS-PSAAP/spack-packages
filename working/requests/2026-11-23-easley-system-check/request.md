# Request: 2026-11-23-easley-system-check

- **Asked for by:** Claude Code, for patrickb314, 2026-11-23
- **Machine:** Easley (UNM CARC), login node
- **Allocation:** login node; `run.sh` also submits one five-minute,
  one-node job with `srun -N 1 -n 1 -t 00:05:00`
- **Expected cost:** at most 0.1 node-hours
- **Depends on:** nothing outside this branch

## Why

`2026-11-23-carc-check` showed Spack 1.2.2 choosing `compass-easley` on
the login node and reusing CARC's Spack as an upstream, but it ran
before this exchange, from an older script, and without the
compute-node check. This run repeats the check through `run-request`,
on the current branch, and answers:

- Does Spack list a `compass-easley` scope on a compute node? The
  compute nodes are named `easley001` and up, and the hostname pattern
  in `include.yaml` has only been tested offline against that form. If
  the scope is missing, `compute.txt` shows the full scope list.
- Do `spack spec -I cmake` and `spack spec -I hdf5 +mpi ^openmpi` still
  reuse CARC's builds (`[^]`), as in `2026-11-23-carc-check`?

## Before running

Load Spack 1.2.2. Your own Spack configuration does not matter: the
check uses a temporary user scope in `~/.system-check.*`, holding only
this checkout's `include.yaml`, removes it at the end, and installs
nothing. If `srun` needs an account or a partition, set `SLURM_ACCOUNT`
or `SLURM_PARTITION` before running.

## Run

From the repository root:

    working/bin/run-request working/requests/2026-11-23-easley-system-check

## Results to return

`system.txt`, `carc-spack.txt`, `modules.txt`, `include.txt`,
`reuse.txt`, `detect.txt`, `detected-packages.yaml`, and `compute.txt`
(the full scope list on a compute node).
