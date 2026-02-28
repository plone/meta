# Update Multiple Repositories

<!-- diataxis: tutorial -->

In this tutorial you will use `multi-call` to apply `config-package` across
multiple Plone repositories in a single run.

## Prerequisites

- `plone.meta` installed (see {doc}`first-package`)
- Git
- Enough disk space for the cloned repositories

## Create a packages file

Create a text file listing the repositories you want to configure.
Each line is a repository name (without the GitHub org prefix):

```shell
cd meta
cat > my-packages.txt << 'EOF'
plone.api
plone.app.contenttypes
plone.restapi
EOF
```

Lines starting with `#` are ignored:

```text
# Core packages
plone.api
plone.app.contenttypes
# REST API
plone.restapi
```

## Prepare a clones directory

Create a directory where repositories will be cloned:

```shell
mkdir -p ../clones
```

## Run multi-call

Run `multi-call` with the path to `config-package`, your packages file,
and the clones directory:

```shell
venv/bin/multi-call venv/bin/config-package my-packages.txt ../clones
```

For each package, `multi-call`:

1. Clones the repository if it does not exist in `../clones`
2. If it already exists, stashes changes, switches to `master`, and pulls
3. Runs `config-package` on the repository

:::{caution}
Running `multi-call` stashes any uncommitted changes in existing repositories.
Run `git stash pop` in each repository to recover them.
:::

## Review the results

After the run completes, inspect the clones:

```shell
cd ../clones/plone.api
git log --oneline -3
```

Each repository now has a new branch with the updated configuration files.

## Summary

You have learned:

- How to create a `packages.txt` file listing target repositories
- How `multi-call` orchestrates cloning and configuring
- How to review results across multiple repositories
