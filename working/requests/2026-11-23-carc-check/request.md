# Request: 2026-11-23-carc-check

- **Asked for by:** Claude Code, for patrickb314, 2026-11-23
- **Machine:** Easley and Hopper (UNM CARC), login nodes
- **Allocation:** login node
- **Expected cost:** none
- **Depends on:** nothing outside this branch

This request predates the `working/` exchange on this branch and is
recorded here after the fact. It ran as `tmp-carc-check/check.sh`, which
is `run.sh` here unchanged (commit 404acad), not through
`working/bin/run-request`; so it has no `manifest.md` or `stdout.log`,
and it wrote one directory per host under `results/`. The results
arrived in commits 7f2ec48 (Easley), 25d998f (Hopper), and 675acff
(Hopper again, after its `upstreams.yaml` was added; this replaced the
first Hopper results). Do not run it again; it cannot run under
`run-request`. Later checks are requests that use
`working/requests/common/system-check.sh`.

## Why

Whether `system_externals/include.yaml` selects Easley's and Hopper's
configuration from their hostnames, with no `CLUSTER` set, and whether
Spack 1.2.2 reuses CARC's Spack installation in `/opt/spack` as an
upstream.

## Results to return

Per host, in `results/<host>/`: `system.txt`, `carc-spack.txt`,
`modules.txt`, `include.txt`, `reuse.txt`, `detect.txt`, and
`detected-packages.yaml`.
