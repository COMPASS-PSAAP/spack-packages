# Evidence and reporting

These apply to results, to documents, and to anything an agent asserts in a pull
request.

- **Distinguish measured from inferred, and predicted from observed**, on every
  number. A number derived from a model is labeled with the model and its inputs.
- **Every performance claim carries a trial count and a spread.** Single-run numbers
  are not results.
- **Report the tail, not the mean alone**, wherever the effect could live in the tail,
  and report a dispersion measure alongside every location measure.
- **Say what was dropped.** A truncated list, a sampled set, a capped sweep — a
  bounded analysis presented without its bound reads as full coverage.
- **Record provenance.** What produced the number: the commit, the inputs, the
  machine, the environment, the seed. A number with no provenance block is not a
  result.
- **Do not invent constants.** Machine-specific values default to a published number,
  cited where it is used, and are arguments rather than literals.
