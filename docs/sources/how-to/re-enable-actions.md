# Re-enable GitHub Actions

<!-- diataxis: how-to -->

GitHub automatically disables Actions on repositories that have not received
commits for a certain period. `plone.meta` provides a command to re-enable
them across all tracked packages.

## Prerequisites

Install [GitHub's CLI application](https://github.com/cli/cli) and
authenticate:

```shell
gh auth login
```

## Re-enable Actions

From the plone.meta directory:

```shell
venv/bin/re-enable-actions
```

This command iterates over all packages listed in `packages.txt`, checks if
a "Meta" workflow exists, and enables it if it was disabled. It does no harm
if Actions are already enabled.
