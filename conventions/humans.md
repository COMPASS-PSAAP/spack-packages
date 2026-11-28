# Human instructions

Directions for the humans running the agents, which the agents also read.

## Running agents safely

- **Keep credentials out of the repository and out of harness configuration.** Inject
  API keys from a password manager or a Codespaces secret at the start of the session.
- **Scope tokens to this repository**, not to the account. A personal access token
  handed to an MCP server has whatever reach you gave it, for as long as the session runs.
- **Add an MCP server only when you can say what it is for.** A GitHub server that
  reads issues, opens pull requests, and checks Actions status earns its place by
  removing hand-copying. Each additional one is another path out of the sandbox.
- **Match the model to the task.** Mechanical work — boilerplate, formatting, a
  straightforward fix, a test case — does not need the expensive model. Watch the context
  too: a session that repeatedly dumps whole files and long command output spends
  budget without adding understanding, so point the agent at line ranges.
- **Assume the next session runs a different model.** Instructions live in `AGENTS.md`
  and the files it indexes, which every harness reads, with `CLAUDE.md` as a symlink
  to it. What a session learned goes in the repository, not in one harness's
  configuration.

## The coding feature loop

One change at a time, and the same way every time:

1. **Branch** off `origin/HEAD`, named for the change.
2. **Orient the agent** — the requirement, the section of the specification, the
   existing code it has to fit.
3. **Ask for a plan and the tests before any implementation**, and read the plan. A
   wrong approach costs a sentence to correct here and a rewrite to correct later.
4. **Implement in small steps**, running the tests after each one.
5. **Read every line of the diff.** A change you cannot explain is not reviewed, and it
   does not matter that it works.
6. **Commit with a message that says why**, and note in the pull request what the agent
   was asked to do.
7. **Open the pull request** once the tests pass locally.
8. **Close the session by updating the memory file** — see
   [Memory and session continuity](memory.md).

## What the human owns

The agent instructions above constrain the agent. These are the reviewer's, and no
instruction given to an agent can substitute for them:

- **Review agent-written code as code from a stranger**, not as your own. 
- **Check the tests hardest.** An agent that wrote both the implementation and its
  test can agree with itself, and a test written after the fact asserts what the code
  does rather than what it should do.
- **Check every number and every citation** that will leave the repository. Fabricated
  references and numbers can look exactly like real ones.
- **Do not merge what you cannot explain.** If you could not defend the change in a
  group meeting, it is not ready. The fix is to understand it.
