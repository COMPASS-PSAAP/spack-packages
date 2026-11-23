# Temporary: CARC system check

**Remove this directory before the pull request merges, and squash-merge
the pull request**, so neither the script nor its results reach `main`.

`check.sh` checks, on UNM CARC's Easley and Hopper, the conditional system
configuration that `system_externals/include.yaml` adds, and surveys what
each system offers Spack. It installs nothing and leaves your own Spack
configuration alone: every Spack command it runs uses a temporary user
scope that holds only this checkout's `include.yaml`.

On each system's login node, with Spack 1.2.2 loaded:

    git clone -b conditional-system-config https://github.com/COMPASS-PSAAP/spack-packages.git
    cd spack-packages
    tmp-carc-check/check.sh             # or: tmp-carc-check/check.sh --compute

`--compute` also runs a five-minute, one-node Slurm job that checks the
choice on a compute node; it spends allocation, so use it only if you
want that check. Arguments after `--compute` pass to `srun`, for example
an account with `-A <account>`.

The results land in `tmp-carc-check/results/<host>/`. Commit and push
them to this branch:

    git add tmp-carc-check/results
    git commit -m "CARC check results from $(hostname -s)"
    git push
