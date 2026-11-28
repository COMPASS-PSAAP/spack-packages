# Issues and Projects

GitHub issues track the work in a repository, one piece of work to an issue.
`knowledge/` records what the work showed; an issue records that the work was asked for, who is doing it, and
whether it is done.

## Agents and issues

- **Agents draft issues and comments; people post them.** An agent never creates an
  issue, a comment, a label, or a Project item without a human's permission for that
  one item. It writes the draft, with its title, type, labels, and body, and gives the
  human the `gh issue create` or `gh issue comment` command that would post it.
- **Say that an agent drafted it**, with the `agent-drafted` label, as a pull request
  says an agent wrote it.
- **Read freely.** Reading issues, comments, and Project status with `gh` changes
  nothing and needs no permission.

## Issue types

The organization defines four issue types, and each issue template sets one:

| Type | For |
|---|---|
| Bug | Something that behaves wrongly, with how to reproduce it |
| Feature | New functionality |
| Task | A specific piece of work, including a research question |
| Paper | Writing and publishing a paper |

## Research questions

An issue tracks a question, not a run. Answering one research question, such as how
an application's advection kernel scales on Tuolumne, usually takes a sequence of HPC
runs, each shaped by the results of the last, and an agent plans most of that
sequence. One issue per run would track the agent's steps rather than the question a
person cares about, and would close long before anything is known.

So a research question gets one issue, from the Research Question template, which
files a Task with the `research` label. The issue states the question, the approach,
and the node-hours the whole question may spend. Its work happens on one branch, where
each run is a request in `working/requests/`, and the issue gains a line for each
request as it runs or is rejected. It closes when its finding in `knowledge/` has been reviewed, or
when a person decides the question is no longer worth answering, which the issue
says.

Break a large piece of work into sub-issues of one parent issue rather than a
checklist, so each part has its own assignee and status. A research question whose
answer depends on smaller questions is such a piece of work.

## Labels

Issue types cover the kind of work, so labels mark only what a type cannot:

| Label | Marks | Color |
|---|---|---|
| `research` | A research question that tests or HPC runs should answer | `#5319e7` |
| `agent-drafted` | An issue or comment an agent drafted and a person posted | `#c5def5` |

A person creates them in a new repository with:

    gh label create research --color 5319e7 --description "A research question that tests or HPC runs should answer"
    gh label create agent-drafted --color c5def5 --description "Drafted by an agent, posted by a person"

## Linking the work

Each step names the one before it, so anyone can follow a research question from
the question to the answer in either direction:

1. **The issue** asks the question.
2. **The branch** is named for the question, and its pull request says
   `Closes #<issue>`.
3. **Each request** in `working/requests/` names the issue in its **Issue** line.
4. **Each result**, once promoted to `results/`, carries its request unchanged.
5. **The finding** in `knowledge/` lists the results, the issue, and the commits in
   its `sources`, and the issue links to the finding before it closes.

## Managing the work

Each repository's owners decide how to manage its work: with issues alone, with
milestones, or with a GitHub Project of their own. The repository's note in
`COMPASS-PSAAP/compass-hub` says which, and links to the Project if there is one.

The hub's Obsidian dashboards give the organization-wide view. They read each tracked repository's open research questions and `knowledge/` files
through the hub's `bin/sync`, whatever its owners use to manage the rest, so the
conventions above are all a repository needs to appear there.
