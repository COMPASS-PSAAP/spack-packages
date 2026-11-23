# Request: 2026-11-23-tuolumne-system-check

- **Asked for by:** Claude Code, for patrickb314, 2026-11-23
- **Machine:** Tuolumne, login node
- **Allocation:** login node; `run.sh` also submits one five-minute,
  one-node job with `flux run -N 1 -t 5m`
- **Expected cost:** at most 0.1 node-hours
- **Depends on:** nothing outside this branch

## Why

This branch replaces the old setup, which copied
`system_externals/tuolumne/packages.yaml` into `~/.spack/$CLUSTER` and
set `SPACK_USER_CONFIG_PATH`, with `system_externals/include.yaml`,
which includes `system_externals/tuolumne/` when `CLUSTER` is
`tuolumne`. Easley and Hopper are checked (`2026-11-23-carc-check`);
Tuolumne is not. The run answers:

- Does Spack 1.2.2 list a `compass-tuolumne` scope on the login node and
  on a compute node? If not, the condition in `include.yaml` is wrong
  for Tuolumne, or `CLUSTER` is not set where the job runs.
- Does `spack spec -I hdf5 +mpi` reuse the system's MPI and HDF5 as
  externals (`[e]`)? Tuolumne should use Cray MPICH and the HDF5
  external. If it builds them, the externals in
  `system_externals/tuolumne/packages.yaml` (refreshed in #11 and not
  yet tested on Tuolumne) do not match what the concretizer wants.

## Before running

Load Spack 1.2.2, as for any use of these packages. Your own Spack
configuration does not matter: the check uses a temporary user scope
that holds only this checkout's `include.yaml`, and installs nothing.

## Run

From the repository root:

    working/bin/run-request working/requests/2026-11-23-tuolumne-system-check

## Results to return

`system.txt`, `modules.txt`, `include.txt` (scopes, upstreams, `spack
config blame packages`, `spack find`), `reuse.txt` (`spack spec -I` of
`cmake`, `hdf5 +mpi`, and `hdf5 +mpi ^openmpi`), `detect.txt` and
`detected-packages.yaml` (what `spack compiler find` and `spack external
find` see, in a scratch scope), and `compute.txt` (the scopes on a
compute node).
