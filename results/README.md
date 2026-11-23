# Results

Results of small-scale HPC test runs that a pull request relies on, or
that serve as baselines. Each is a request from the `working/` exchange,
promoted by a person; see `working/README.md`, "Keeping a result".

## What a result carries

A promoted result is the request's directory, copied unchanged:

- `request.md`: why the run was made, the machine, and the allocation
- `run.sh`: exactly what ran
- `results/manifest.md`: the commit, host, start time, elapsed time, exit
  status, Spack version, and an allowlisted set of environment variables
- `results/stdout.log` and the artifacts `run.sh` copied

That records the job script, the environment, and the provenance without
a second format. Do not edit a promoted result; a new run is a new
result.

## Naming

A result keeps its request's name: `results/<date>-<topic>/`, for
example `results/2026-11-20-solver-baseline/`.
