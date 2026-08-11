# Issue tracker: GitHub

Issues and PRDs for this repository live in GitHub Issues. Use the `gh` CLI
from this checkout so it resolves `ReidSurmeier/kicad-agent-toolkit` from the
`origin` remote.

- Create: `gh issue create --title "..." --body-file FILE`
- Read: `gh issue view NUMBER --comments`
- List: `gh issue list --state open`
- Comment: `gh issue comment NUMBER --body-file FILE`
- Label: `gh issue edit NUMBER --add-label LABEL`
- Close: `gh issue close NUMBER --comment "..."`

When a skill says to publish to the issue tracker, create a GitHub issue. When
it says to fetch a ticket, use `gh issue view` and include comments and labels.
