# Memory and session continuity

A session's memory dies with it, and the next agent inherits the files rather than the
reasoning. When agent reasoning is worth carrying forward but belongs in no file,
write it in a `MEMORY.md` file at the root of the repository. The last step of a
working session is to bring it up to date:

- **Current state** — what was being worked on, and whether it is done, blocked, or
  half finished
- **Design decisions and their reasoning**, where the code or the document records only
  the outcome, and reversals, so they are not proposed again
- **Operational procedures that are easy to get wrong**
- **Open questions and next steps**, including threads waiting on a person or an event
  rather than on work

Keep it short and dated without a revision history, point at the file that owns each 
area rather than duplicating it, and verify before acting on it: it records what was 
true when it was written.  Add its row to the **Repository map** in `AGENTS.md` when
you create it.
