# Check Site Availability

A reusable GitHub Action that fetches a URL and verifies that the response body contains an expected text fragment.

This action is designed for simple site validation checks in workflows where a successful HTTP response is not enough on its own. It helps catch cases where a page still responds but is missing critical content.

## What It Does

- Fetches a URL with `curl`
- Retries transient request failures up to 3 times
- Fails the workflow if the request fails
- Fails the workflow if the response body does not contain the expected text
- Writes failure details to the GitHub step summary
- Logs a truncated response body preview when the expected text is missing

## What It Does Not Do

- It does not parse HTML or validate DOM structure
- It does not support regular expressions
- It does not expose outputs in `v1`
- It does not schedule checks by itself; you run it from your own workflows

## Usage

```yaml
name: Check site availability

on:
  workflow_dispatch:
  schedule:
    - cron: "17 * * * *"

jobs:
  check-site:
    runs-on: ubuntu-slim
    steps:
      - uses: LightNetDev/check-site-availability@v1
        with:
          url: https://example.com
          expected-text: Example Domain
```

GitHub recommends avoiding scheduled workflows at the start of the hour because high load at those times can delay or drop queued runs. Pick an offset minute such as `17` instead of `0` for more reliable checks. See [GitHub's schedule event notes](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

If you want email alerts when a check fails, enable GitHub Actions email notifications for the account that owns or maintains the workflow and optionally limit them to failed workflows only. See [Managing GitHub Actions notifications](https://docs.github.com/en/subscriptions-and-notifications/how-tos/managing-github-actions-notifications).

For testing, you can trigger the workflow manually with `workflow_dispatch` from the Actions tab and choose the branch to run. The workflow file must exist on the repository's default branch for the **Run workflow** button to appear. See [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

Scheduled monitoring is not a good fit for **public repositories** that may sit idle for long periods. GitHub automatically disables scheduled workflows in a public repository after 60 days without repository activity. See [GitHub's schedule event notes](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## Inputs

| Input           | Required | Description                                                  |
| --------------- | -------- | ------------------------------------------------------------ |
| `url`           | Yes      | Full URL to request.                                         |
| `expected-text` | Yes      | Literal text fragment that must appear in the response body. |

## Failure Behavior

The action exits with a non-zero status in these cases:

- `url` is missing
- `expected-text` is missing
- the HTTP request fails
- the response body does not include the expected text

When a check fails, the action also writes a short summary to `GITHUB_STEP_SUMMARY` so the failure is easier to review in the workflow run UI.

If the request succeeds but the expected text is missing, the action also prints a truncated response body preview to the workflow log to help with debugging without dumping the entire page.

## Versioning

Consumers should reference the stable major tag:

```yaml
uses: LightNetDev/check-site-availability@v1
```

This keeps workflows on the latest compatible `v1` release while still allowing exact version pinning when needed.

Maintainer release instructions live in [RELEASING.md](./RELEASING.md).
