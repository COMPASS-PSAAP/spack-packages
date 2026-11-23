#!/bin/bash
# Checks the conditional system configuration on a supported system and
# surveys what the system offers Spack. A request's run.sh calls this from
# the repository root, under working/bin/run-request, which sets RESULTS_DIR.
#
# Usage: bash working/requests/common/system-check.sh [slurm|flux]
#
# slurm or flux also checks the choice on a compute node with a five-minute,
# one-node job.
set -u

: "${RESULTS_DIR:?run this through working/bin/run-request}"
repo=$(git rev-parse --show-toplevel)
out=$RESULTS_DIR
scheduler=${1:-}

command -v spack &>/dev/null || {
  echo "system-check.sh: load Spack 1.2.2 first" >&2
  exit 1
}
case $(spack --version) in
  1.2.*) ;;
  *) echo "system-check.sh: expected Spack 1.2.x, found $(spack --version)" >&2 ;;
esac

mkdir -p "$out"
# In the home directory, which compute nodes share. mktemp's default,
# $TMPDIR, put it in /var/tmp on Dane and Tuolumne, probably node-local:
# their compute jobs listed no compass scope
scope=$(mktemp -d "$HOME/.system-check.XXXXXX")
trap 'rm -rf "$scope"' EXIT
mkdir -p "$scope/user" "$scope/detect"
printf 'include:\n- path: %s/system_externals/include.yaml\n' "$repo" \
  >"$scope/user/include.yaml"
# Every Spack command below sees only the include under test
export SPACK_USER_CONFIG_PATH=$scope/user
unset COMPASS_SYSTEM

# run <command...>: echo the command, run it, and record a failure instead
# of stopping, since a failure is itself a finding
run() {
  echo "\$ $*"
  "$@" 2>&1 || echo "(exit status $?)"
  echo
}

spack_db_version() {
  python3 -c 'import json, sys
d = json.load(open(sys.argv[1]))["database"]
print("database version", d["version"], "with", len(d["installs"]), "installs")' "$1"
}

{
  run date
  run hostname
  run hostname -f
  run uname -a
  # Whether a login shell sets CLUSTER, and whether it exports it
  run bash -lc 'declare -p CLUSTER'
  run cat /etc/os-release
  echo "\$ env | grep -E 'CLUSTER|SYS_TYPE|CARC|LMOD_SYSTEM|SLURM_CONF'"
  env | grep -E 'CLUSTER|SYS_TYPE|CARC|LMOD_SYSTEM|SLURM_CONF'
  echo
  run lscpu
  run nvidia-smi --query-gpu=name,compute_cap,driver_version --format=csv
  run sinfo -s
  run which -a spack
  run spack --version
  run spack arch
} >"$out/system.txt"

# Where CARC keeps its own Spack, its release, and its database format,
# which decides whether Spack 1.2.2 can read it as an upstream
[ -d /opt/spack ] && {
  run ls -ld /opt/spack /opt/spack/opt/spack
  echo "\$ ls -d /opt/*spack* /usr/local/*spack* /packages/*spack*"
  ls -d /opt/*spack* /usr/local/*spack* /packages/*spack* 2>&1
  echo
  run git -C /opt/spack describe --tags --always
  run git -C /opt/spack log -1 --format='%H %cd'
  run /opt/spack/bin/spack --version
  run spack_db_version /opt/spack/opt/spack/.spack-db/index.json
  if [ -n "${LMOD_CMD:-}" ]; then
    echo "\$ module -t avail | grep -i spack"
    "$LMOD_CMD" bash -t avail 2>&1 | grep -i spack
    echo
  fi
} >"$out/carc-spack.txt"

if [ -n "${LMOD_CMD:-}" ]; then
  run "$LMOD_CMD" bash -t avail >"$out/modules.txt"
fi

# Which compass-<system> scope Spack chose, and what it brought in
{
  run spack config scopes -p
  run spack config get upstreams
  run spack config blame packages
  echo "\$ spack find | head -40"
  spack find 2>&1 | head -40
  echo
  for p in gcc llvm cmake python cuda openmpi mvapich2 mpich hdf5; do
    run spack find -lv "$p"
  done
} >"$out/include.txt"

# What Spack reuses: "[^]" marks an upstream package and "[e]" an
# external; the plain hdf5 shows the system's preferred MPI
{
  run spack spec -I cmake
  run spack spec -I hdf5 +mpi
  run spack spec -I hdf5 +mpi ^openmpi
} >"$out/reuse.txt"

# What Spack finds on the system itself, for a system with no upstream;
# written to a scratch scope, never to yours
{
  run env SPACK_USER_CONFIG_PATH="$scope/detect" spack compiler find --scope user
  run env SPACK_USER_CONFIG_PATH="$scope/detect" spack external find --scope user
} >"$out/detect.txt"
[ -f "$scope/detect/packages.yaml" ] &&
  cp "$scope/detect/packages.yaml" "$out/detected-packages.yaml"

on_compute='hostname; spack config scopes -p'
case $scheduler in
  slurm) run srun -N 1 -n 1 -t 00:05:00 bash -c "$on_compute" >"$out/compute.txt" ;;
  flux) run flux run -N 1 -t 5m bash -c "$on_compute" >"$out/compute.txt" ;;
esac
