#!/bin/bash
# working/bin/run-request runs this from the repository root, with
# RESULTS_DIR set to this request's results/ directory. Copy anything to
# send back into "$RESULTS_DIR". run-request records stdout, the exit
# status, and the environment itself.
# See "Writing run.sh" in working/README.md before filling this in.
set -euo pipefail

: "${RESULTS_DIR:?run this through working/bin/run-request}"
[ "${CLUSTER:-}" = dane ] || {
  echo "run.sh: this request is for Dane; CLUSTER is '${CLUSTER:-}'" >&2
  exit 1
}
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
bash "$here/../common/system-check.sh" slurm
