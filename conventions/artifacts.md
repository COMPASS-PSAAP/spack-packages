# Durable artifacts

The session scratchpad is not storage. Anything someone outside the session will read
again — a figure, a generated table, a campaign script, a shareable page — belongs
in this repository, on a branch, pushed. Scratchpad files disappear with the session and
are unrecoverable.

- **A generated artifact is not finished until it is committed.** Publishing puts a
  rendering on a hosted page; committing puts it where someone else can regenerate,
  diff, and correct it. Commit it locally, and ask before publishing.
- **A derived artifact names its sources inside the artifact** — which files, at which
  commit — and states that the sources win where the two disagree. A rendering with no
  provenance becomes a second source of truth that nobody can date.
- **Derived files live in their own directory**, never beside the authoritative ones.
  The directory is the signal that the file is generated rather than owned.
- **One-shot helper scripts are not artifacts.** A patch script already applied, or a
  validator written to check one file once, stays in the scratchpad.
