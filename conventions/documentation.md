# Writing and publishing documentation

## Writing documentation

Where `docs/` exists, two tools build one site. MkDocs builds Markdown pages in
`docs/` that explain the system, and `mkdocs.yml` lists them. Doxygen builds an API
reference from doc comments in the source into the site's `api/` directory, and
`docs/doxygen/Doxyfile` says what it reads.

- **Explain the system in Markdown pages in `docs/`**, one topic to a page:
  - `index.md`: what the system is for, who uses it, and what is out of scope
  - `architecture.md`: the major components, what each owns, how data and control
    move between them, and where each lives in the source tree
  - `design-decisions.md`: each decision that shaped the system, with its date, the
    problem, the alternatives, the choice, and its consequences. A reversed decision
    is marked superseded, not deleted
  - `contributing.md`: the conventions for working in the repository, such as how
    to build, test, and format, the branch and review workflow, and the traps that
    have already cost someone a day
- **Goals and design rationale come from people.** [Writing](writing.md) applies: draft
  a goal or a decision record only from what a person said or wrote, cite it, and
  leave it for them to confirm. Structure and conventions you can verify in the code
  and its history are yours to document.
- **List each page in the `nav` of `mkdocs.yml`**, which also sets the page order.
  Link between pages with ordinary Markdown links to the `.md` file. The build fails
  on a link it cannot resolve and on a page missing from `nav`.
- **Keep one owner for each fact.** Once `contributing.md` exists, it owns the build,
  test, and style conventions, and **Additional engineering conventions** in
  `AGENTS.md` points to it instead of repeating them; `AGENTS.md` and `conventions/`
  keep the rules for agents. Architecture pages point at the code instead of copying
  signatures the API reference shows.
- **Document the contract a caller relies on**, not the steps the code takes: what a
  function does, its preconditions, the units of every quantity, who owns memory and
  for how long, and what happens on error. For parallel code, say whether a call is
  collective and over which communicator, whether a pointer is host or device memory,
  and whether the call is thread-safe.
- **Give every public symbol in a header a doc comment**, written as `///` with
  `@brief`, `@param`, and `@return`. Internal code needs none. A header that declares
  free functions also needs a `/// @file` comment, or Doxygen drops its functions and
  checks nothing in them. Doc comments on public interfaces are API documentation, so
  the preference for self-documenting code over explanatory comments does not apply.
- **Change the docs in the same pull request as the behavior they describe**, and fix
  the docs your change invalidates, including the architecture and conventions pages
  when a component or a convention moves. Stale documentation reads like a fact.
- **Documentation is a claim.** [Evidence and reporting](evidence.md)
  applies: no performance number, citation, or behavior you did not verify. An example
  compiles and runs, or is marked untested.
- **Build the docs before opening a pull request.** Install the packages once in a
  virtual environment, with `python3 -m venv .venv` and
  `.venv/bin/pip install -r docs/requirements.txt`, then run
  `.venv/bin/mkdocs build --strict` and `doxygen docs/doxygen/Doxyfile`, in that
  order, because MkDocs empties `build/site/` first. CI fails on any warning from
  either, and a warning is a finding to fix, not noise to silence.
- **Never commit generated HTML.** `build/site/` is derived output that CI rebuilds.
- **Publishing is a human's decision.** Enabling Pages or setting `PUBLISH_DOCS` falls
  under [Ask a human first](../AGENTS.md#ask-a-human-first). A published site is
  public even when the repository is private, so nothing goes in `docs/` or a doc comment that does
  not belong on the COMPASS website.

## Publishing documentation

The template ships `docs/`, an MkDocs configuration in `mkdocs.yml`, a Doxygen
configuration in `docs/doxygen/`, and the `docs` workflow, which builds the site on
every pull request. Nothing is published until someone with admin access to the
repository follows the steps below. A repository with no use for a documentation site
deletes `docs/`, `mkdocs.yml`, and `.github/workflows/docs.yml` and records the choice
in `CHANGELOG.md`.

### Turning on the documentation site

1. **Confirm that everything can be public.** The organization's GitHub Team plan
   cannot restrict a Pages site, so `https://compass.unm.edu/<repository>/` is public
   even when the repository is private. Check `docs/` and the doc comments for
   unpublished results, collaborator material, and export-controlled content.
2. **Check the repository name.** It becomes the site's path, so it must not match a
   top-level path of the main site, such as `projects`, `research`, `team`,
   `members`, `blog`, or `artifacts`. GitHub does not document which site wins a
   collision.
3. **Configure the build.** In `mkdocs.yml`, set `site_name` and `site_url`, and
   replace `docs/index.md` with a real front page. In `docs/doxygen/Doxyfile`, set
   `PROJECT_NAME` and add the source directories to `INPUT`, and replace
   `docs/doxygen/mainpage.md` with a real front page for the API reference.
4. **Build it locally**, as [Writing documentation](#writing-documentation) says,
   fix every warning, and open `build/site/index.html`. Merge these changes through a
   pull request.
5. **Point Pages at the workflow.** In the repository on GitHub, open **Settings →
   Pages**, and under **Build and deployment** set **Source** to "GitHub Actions".
6. **Allow publishing.** Open **Settings → Secrets and variables → Actions**, choose
   the **Variables** tab, and add a repository variable named `PUBLISH_DOCS` with the
   value `true`.
7. **Publish.** Open **Actions → Documentation**, choose **Run workflow** on `main`,
   and wait for the "Publish to GitHub Pages" job. Later merges to `main` republish
   the site.
8. **Check and link the site.** Open `https://compass.unm.edu/<repository>/`, then
   link it from the main site with a pull request to `compass-psaap.github.io`.

To stop publishing, set `PUBLISH_DOCS` to `false`, then under **Settings → Pages**
open the "⋯" menu next to "Your site is live at" and choose **Unpublish site**.

### Keeping the documentation useful

- **Preview before merging.** Each pull request's run attaches the built site as the
  `docs-html` artifact; download it and open `index.html`.
- **Write the goals and design decisions yourself**, or give the agent what you wrote
  elsewhere to draft from. Record a decision when you make it; one reconstructed
  months later records what you remember, not what you weighed. Agents can draft the
  architecture and conventions pages from the code, and you check them.
- **Review docs against the code.** An agent can describe what code does accurately
  and still miss what it is for, and the intent is yours to check.
- **Tighten the warnings once the public interface is documented** by setting
  `WARN_IF_UNDOCUMENTED = YES` in `docs/doxygen/Doxyfile`, so new gaps fail CI.
