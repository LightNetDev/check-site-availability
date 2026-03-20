# AGENTS

This repository publishes a reusable GitHub Action:

- action slug: `LightNetDev/check-site-availability`
- stable consumer ref: `LightNetDev/check-site-availability@v1`
- action type: root-level composite action

## Project Purpose

The action fetches a URL and verifies that the response body contains a required literal text fragment.

It is intentionally small and dependency-light:

- no Node.js package
- no build step
- no generated files
- shell-based implementation in [`action.yml`](./action.yml)

## Important Files

- [`action.yml`](./action.yml)
  The action entrypoint and implementation. Most functional changes happen here.
- [`README.md`](./README.md)
  Consumer-facing documentation. Keep usage examples aligned with the real inputs.
- [`RELEASING.md`](./RELEASING.md)
  Maintainer guide for versioning and exact release commands. Read this before changing release flow.
- [`.github/workflows/validate.yml`](./.github/workflows/validate.yml)
  CI workflow that self-tests the action with `uses: ./`.
- [`test/fixtures/index.html`](./test/fixtures/index.html)
  Local fixture served by CI for the success-path self-test.
- [`.gitignore`](./.gitignore)
  Local-only ignores for editor files and logs.

## Editing Guidance

- Preserve the public interface unless the task explicitly changes it.
  Current required inputs are `url` and `expected-text`.
- Keep the action portable for external GitHub users.
- Prefer runner-provided tools only.
  The current implementation relies on `bash`, `curl`, and `grep`.
- If you change failure behavior, keep `GITHUB_STEP_SUMMARY` output helpful.
- If you change the fixture text or URL expectations, update CI and docs together.

## Validation

Primary validation lives in [`.github/workflows/validate.yml`](./.github/workflows/validate.yml).

That workflow checks:

- success case against the local fixture server
- missing-text failure case
- request-failure case

When making behavior changes, verify that the workflow logic still matches the action contract.

## Releases

Use [`RELEASING.md`](./RELEASING.md) for releases.

Important release conventions:

- publish immutable SemVer tags like `v1.0.1`
- move the major tag `v1` to the latest compatible release
- keep the GitHub Release notes and README usage examples current
