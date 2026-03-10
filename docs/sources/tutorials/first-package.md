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

Run `config-package` on a Plone repository, inspect the generated files, and customize via {file}`.meta.toml`.
This workflow is especially useful for [collective](https://github.com/collective) repositories adopting standard Plone tooling.

## Prerequisites

- Python 3.10 or later (with [uv](https://docs.astral.sh/uv/) recommended)
- Git
- A Plone Python package repository to configure (or you can use any
  single-package Python repository)

## Run config-package

Pick a target repository.
For this example, use `plone.api`:

```shell
git clone https://github.com/plone/plone.api.git
```

Run `config-package` using `uvx`:

```shell
uvx --from=plone.meta config-package plone.api
```

:::{note}
If you prefer a local installation instead of `uvx`, see
{doc}`/how-to/install` for the virtual environment approach, then run
`.venv/bin/config-package plone.api`.
:::

The output shows:
1. A new git branch (named `config-with-default-template-<hash>`)
2. Configuration files written
3. A commit created

## Inspect the results

Look at the generated files:

```shell
cd plone.api
git log --oneline -1
git diff HEAD~1 --stat
```

`config-package` created or updated these files:

- {file}`.meta.toml` -- plone.meta's own configuration
- {file}`.editorconfig` -- editor settings
- {file}`.flake8` -- flake8 linting rules
- {file}`.gitignore` -- git ignore patterns
- {file}`.github/workflows/meta.yml` -- GitHub Actions CI (for GitHub-hosted repos)
- {file}`.pre-commit-config.yaml` -- pre-commit hooks
- {file}`pyproject.toml` -- Python tooling configuration
- {file}`tox.ini` -- tox test environments

## Understand .meta.toml

Open {file}`.meta.toml`, the central configuration file:

```toml
[meta]
template = "default"
commit-id = "a1b2c3d4"

[tox]
test_runner = "zope.testrunner"
```

All your customizations go into {file}`.meta.toml`.
Re-running `config-package` reads this file and regenerates everything else.

:::{important}
Do not edit generated files directly.
They are overwritten each time `config-package` runs.
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

Re-run `config-package` on the current branch:

```shell
uvx --from=plone.meta config-package --branch current .
```

Check {file}`.flake8` -- your custom lines appear below the standard configuration.

## Run the generated tox environments

The generated {file}`tox.ini` provides several environments:

```shell
# Run the test suite
tox -e test

# Check code formatting
tox -e lint

# Check if the package is release-ready
tox -e release-check
```

## Summary

You now know how to:

- Run `config-package` on a repository
- Inspect the generated files
- Customize behaviour through {file}`.meta.toml`
- Re-run `config-package` after configuration changes
- Use the generated tox environments
