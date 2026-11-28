# Conventions

The organization's standing rules, one topic per file, for every repository
created from `COMPASS-PSAAP/compass-template`. `AGENTS.md` holds the rules every
task needs and indexes these files, in its "Conventions" section, with when to read
each.

Do not edit these files to fit one repository. A local change is invisible from
every other repository, and drift from the template should stay visible as a diff.
If a rule is wrong, change it in the template. A rule for this repository alone goes
in a "For This Repository" section at the end of `AGENTS.md`, and its build, test,
and style conventions go in `docs/contributing.md` once that exists.

| File | Covers |
|---|---|
| [`git-and-prs.md`](git-and-prs.md) | Branches, commits, and pull requests |
| [`evidence.md`](evidence.md) | Numbers, results, provenance, and what was dropped |
| [`writing.md`](writing.md) | Prose style, and whose voice a text may use |
| [`documentation.md`](documentation.md) | The documentation site: writing it, building it, and publishing it |
| [`issues-and-projects.md`](issues-and-projects.md) | Issues, labels, research questions, and how work links to findings |
| [`artifacts.md`](artifacts.md) | Generated files someone else will use |
| [`machines.md`](machines.md) | Machine time, Spack, timings, data, and the HPC exchange |
| [`memory.md`](memory.md) | `MEMORY.md` and carrying reasoning between sessions |
| [`humans.md`](humans.md) | Running agents safely, the feature loop, and what the reviewer owns |
