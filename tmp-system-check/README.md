# Temporary: system configuration check

**Remove this directory before the pull request merges, and squash-merge
the pull request**, so neither the script nor its results reach `main`.

`check.sh` checks, on each supported system (Dane, Tuolumne, Easley, and
Hopper), the conditional system configuration that
`system_externals/include.yaml` adds, and surveys what each system offers
Spack. It installs nothing and leaves your own Spack
configuration alone: every Spack command it runs uses a temporary user
scope that holds only this checkout's `include.yaml`.

On each system's login node, with Spack 1.2.2 loaded:

    git clone -b conditional-system-config https://github.com/COMPASS-PSAAP/spack-packages.git
    cd spack-packages
    tmp-system-check/check.sh             # or: tmp-system-check/check.sh --compute

`--compute` also runs a five-minute, one-node Slurm job that checks the
choice on a compute node; it spends allocation, so use it only if you
want that check. Arguments after `--compute` pass to `srun`, for example
an account with `-A <account>`. On Tuolumne, which runs Flux, use
`flux run -N1 -t 5m bash -c 'hostname; spack config scopes -p | grep compass'`
by hand instead.

The results land in `tmp-system-check/results/<host>/`. Commit and push
them to this branch:

    git add tmp-system-check/results
    git commit -m "System check results from $(hostname -s)"
    git push
