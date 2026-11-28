# Revision history

Newest first.

**2026-11-28 — agent rules from `compass-template`.** This repository has had the
template's HPC request exchange in `working/` since #13, but no `AGENTS.md`, so an
agent working here never read the rules for using it: what it may ask a person to
run, what it must never write, and how much machine time a request may spend. It now
carries the template's `AGENTS.md`, adapted to describe the package repository and
system configuration, the `CLAUDE.md` symlink, and `conventions/`, unchanged. The
exchange gains the template's newer rules: agents never reach an LLNL or CARC system
from outside it, run on LLNL systems only inside LC's sandbox and on CARC systems
not at all until the PI documents how they may, and a person can reject a request
with a `response.md` from `working/bin/respond` instead of running it. The exchange
also gains the template's large-file store: files too large to send back stay in
`/usr/workspace/unm_cs/spack-packages` on the LLNL systems and
`/projects/bridges/compass/spack-packages` on Easley and Hopper, shared with the project's
group, instead of in the home directory of whoever ran the request, where no one
else could analyze or clean them up. It keeps one difference from the template: no
`results/` and no promotion, since the repository tests its configuration and keeps
no results.
