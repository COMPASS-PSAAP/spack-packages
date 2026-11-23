# Request: <name>

- **Asked for by:** <agent or person>, <date>
- **Machine:** <Tuolumne, Dane, Tioga, Easley, or a workstation>
- **Allocation:** <for example `flux alloc -N1 -t 1h`, or "login node">
- **Expected cost:** <node-hours>
- **Depends on:** <other repositories and branches the run builds, if any>

## Why

<The question this run answers, and what each possible result would mean.>

## Before running

<Anything the human must set up first, such as a Spack configuration or a
branch to check out in another repository.>

## Run

From the repository root, inside the allocation above:

    working/bin/run-request working/requests/<name>

## Results to return

<What run.sh copies into `$RESULTS_DIR`, in addition to the `stdout.log`
and `manifest.md` that `run-request` always writes.>
