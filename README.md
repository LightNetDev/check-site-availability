# Check Site Availability

A reusable GitHub Action that fetches a URL and verifies that the response body contains an expected text fragment.

This action is designed for simple site validation checks in workflows where a successful HTTP response is not enough on its own. It helps catch cases where a page still responds but is missing critical content.

## What It Does

- Fetches a URL with `curl`
- Retries transient request failures up to 3 times
- Fails the workflow if the request fails
- Fails the workflow if the response body does not contain the expected text
- Writes failure details to the GitHub step summary

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
    - cron: "0 * * * *"

jobs:
  check-site:
    runs-on: ubuntu-slim
    steps:
      - name: Check page content
        uses: LightNetDev/check-site-availability@v1
        with:
          url: https://example.com
          expected-text: Example Domain
```

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

## Versioning

Consumers should reference the stable major tag:

```yaml
uses: LightNetDev/check-site-availability@v1
```

This keeps workflows on the latest compatible `v1` release while still allowing exact version pinning when needed.

Maintainer release instructions live in [RELEASING.md](./RELEASING.md).
