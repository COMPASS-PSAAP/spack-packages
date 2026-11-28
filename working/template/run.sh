#!/bin/bash
# working/bin/run-request runs this from the repository root, with
# RESULTS_DIR set to this request's results/ directory and LARGE_DIR set to
# its directory in the large-file store on this machine. Copy anything to
# send back into "$RESULTS_DIR", write files too large to send back into
# "$LARGE_DIR", and analyze them here. run-request records stdout, the exit
# status, the environment, and the large files itself.
# See "Writing run.sh" in working/README.md before filling this in.
set -euo pipefail

: "${RESULTS_DIR:?run this through working/bin/run-request}"
