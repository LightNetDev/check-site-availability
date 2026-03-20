# Releasing

This document covers the release process for `LightNetDev/check-site-availability`.

## Versioning

Consumers should normally use:

```yaml
uses: LightNetDev/check-site-availability@v1
```

Maintainers publish immutable version tags such as `v1.0.1` and then move the major tag `v1` to the same commit.

## Release Steps

Before starting:

- make sure the working tree is clean
- make sure you are on `main`
- make sure `origin/main` is up to date

```bash
git switch main
git pull --ff-only origin main
git status --short
```

## Future Patch Release

Example: release `v1.0.1`

```bash
git switch main
git pull --ff-only origin main
git status --short

git tag -a v1.0.1 -m "Release v1.0.1"
git tag -f v1

git push origin main
git push origin v1.0.1
git push origin --force v1

gh release create v1.0.1 \
  --repo LightNetDev/check-site-availability \
  --title "v1.0.1" \
  --notes "Patch release for the Check Site Availability action."
```

## Future Minor Release

Example: release `v1.1.0`

```bash
git switch main
git pull --ff-only origin main
git status --short

git tag -a v1.1.0 -m "Release v1.1.0"
git tag -f v1

git push origin main
git push origin v1.1.0
git push origin --force v1

gh release create v1.1.0 \
  --repo LightNetDev/check-site-availability \
  --title "v1.1.0" \
  --notes "Minor release for the Check Site Availability action."
```

## Verification

After publishing:

```bash
git ls-remote --tags origin
gh release view v1.0.1 --repo LightNetDev/check-site-availability
```

Confirm that:

- the new SemVer tag exists on GitHub
- the moving tag `v1` points to the latest `v1.x` release
- the GitHub Release page is published
- the README usage example still matches the supported inputs
