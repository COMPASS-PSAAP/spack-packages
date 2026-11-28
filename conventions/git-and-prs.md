# Git and pull requests

- **Get default branch protection enabled.** After the repository is created or
  forked, ask a human to turn it on if the organization has not already turned
  it on by default.
- **Never commit to the default branch.** Branch off `origin/HEAD` with a name that
  says what the branch does, and open a pull request.  This includes initial setup — 
  you may create the default branch (`main`) if it does not exist, but every change 
  to it goes through a pull request.
- **Fill in the pull-request template**, including the checklists. They are the
  organization's review contract.
- **Say in the pull request that an agent wrote it**, and what a reviewer should look
  at hardest.
- **Do not add agent `Co-Authored-By` trailers.** Attribution belongs in the pull
  request description, where it can be read alongside what was reviewed.
- **Prefer amending to stacking fix commits**, and update the message to match what
  the commit now does. Subject under 51 characters, body lines under 73, why over
  what, real newlines.
- **One change per pull request.** A formatting sweep and a behavior change in the
  same branch cannot be reviewed, only skimmed.
