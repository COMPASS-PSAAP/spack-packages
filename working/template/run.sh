#!/bin/bash
# working/bin/run-request runs this from the repository root, with
# RESULTS_DIR set to this request's results/ directory. Copy anything to
# send back into "$RESULTS_DIR". run-request records stdout, the exit
# status, and the environment itself.
# See "Writing run.sh" in working/README.md before filling this in.
set -euo pipefail

: "${RESULTS_DIR:?run this through working/bin/run-request}"
