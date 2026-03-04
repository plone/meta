---
myst:
  html_meta:
    "description": "Tutorial: configure your first package with plone.meta"
    "property=og:description": "Tutorial: configure your first package with plone.meta"
    "property=og:title": "Configure Your First Package"
    "keywords": "plone.meta, tutorial, first package, config-package"
---

# Configure Your First Package

<!-- diataxis: tutorial -->

In this tutorial you will run `config-package` on a Plone repository and
inspect the generated configuration files.

By the end, you will understand the basic workflow: run the command, review
the generated files, and customize via {file}`.meta.toml`.

This is especially useful for repositories in the
[Plone collective](https://github.com/collective) that want to adopt
the standard Plone tooling configuration.

## Prerequisites

- Python 3.9 or later (with [uv](https://docs.astral.sh/uv/) recommended)
- Git
- A Plone Python package repository to configure (or you can use any
  single-package Python repository)

## Run config-package

Pick a target repository. For this tutorial, we use `plone.api` as an example:

```shell
git clone https://github.com/plone/plone.api.git
```

Now run `config-package` using `uvx`:

```shell
uvx --from=plone.meta config-package plone.api
```

:::{note}
If you prefer a local installation instead of `uvx`, see
{doc}`/how-to/install` for the virtual environment approach, then run
`.venv/bin/config-package plone.api`.
:::

You should see output showing:
1. A new git branch being created (named like `config-with-default-template-<hash>`)
2. Configuration files being written
3. A commit being created

## Inspect the results

Look at the generated files:

```shell
cd plone.api
git log --oneline -1
git diff HEAD~1 --stat
```

You will see that `config-package` created or updated these files:

- {file}`.meta.toml` -- plone.meta's own configuration
- {file}`.editorconfig` -- editor settings
- {file}`.flake8` -- flake8 linting rules
- {file}`.gitignore` -- git ignore patterns
- {file}`.github/workflows/meta.yml` -- GitHub Actions CI (for GitHub-hosted repos)
- {file}`.pre-commit-config.yaml` -- pre-commit hooks
- {file}`pyproject.toml` -- Python tooling configuration
- {file}`tox.ini` -- tox test environments

## Understand .meta.toml

Open {file}`.meta.toml`. This is the central configuration file. It looks like:

```toml
[meta]
template = "default"
commit-id = "a1b2c3d4"

[tox]
test_runner = "zope.testrunner"
```

Every customization you make goes into {file}`.meta.toml`. When you re-run
`config-package`, it reads this file and regenerates all other files
accordingly.

:::{important}
Never directly edit the generated configuration files.
Your changes will be overwritten the next time someone runs `config-package`.
All customization goes into {file}`.meta.toml`.
:::

## Try a customization

Add extra lines to the {file}`.flake8` configuration by editing {file}`.meta.toml`:

```toml
[flake8]
extra_lines = """
per-file-ignores =
    setup.py:T20
"""
```

Now re-run `config-package` using the current branch:

```shell
uvx --from=plone.meta config-package --branch current .
```

Check the {file}`.flake8` file -- your custom lines appear below the standard configuration.

## Run the generated tox environments

The generated {file}`tox.ini` provides several environments. Try them:

```shell
# Run the test suite
tox -e test

# Check code formatting
tox -e lint

# Check if the package is release-ready
tox -e release-check
```

## Summary

You have learned:

- How to run `config-package` on a repository
- What files it generates and why you should not edit them directly
- How {file}`.meta.toml` controls customization
- How to re-run `config-package` after changing {file}`.meta.toml`
- What tox environments are available
