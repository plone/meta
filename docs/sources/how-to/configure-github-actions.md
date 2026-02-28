# Configure GitHub Actions

<!-- diataxis: how-to -->

`plone.meta` generates a `.github/workflows/meta.yml` file that references
reusable workflows from the plone/meta repository.

## Select CI jobs

Choose which jobs to include:

```toml
[github]
jobs = [
    "qa",
    "test",
    "coverage",
    "dependencies",
    "release_ready",
    "circular",
]
```

Available jobs:

qa
: Runs `tox -e lint` for code quality checks.

test
: Runs `tox -e test` with a configurable Python version matrix.

coverage
: Runs `tox -e coverage` and outputs a coverage report.

dependencies
: Validates dependencies with `z3c.dependencychecker`.

release_ready
: Checks if the package is ready for release.

circular
: Detects circular dependencies.

## Pin the workflow version

By default, workflows reference the `2.x` branch of plone/meta.
Pin to a specific tag:

```toml
[github]
ref = "v3"
```

## Set environment variables

```toml
[github]
env = """
  debug: 1
  image-name: 'org/image'
  image-tag: 'latest'
"""
```

## Install OS-level dependencies

Specify Ubuntu package names:

```toml
[github]
os_dependencies = "git libxml2 libxslt1-dev"
```

## Override Python versions

```toml
[github]
py_versions = "[\"3.13\", \"3.12\", \"3.11\"]"
```

:::{note}
The GitHub Action expects a JSON array string.
Quotes must be escaped in TOML.
:::

## Required repository variables

The GitHub Actions workflow expects these variables to exist at the
organization or repository level:

`TEST_OS_VERSIONS`
: List of OS names, e.g. `["ubuntu-latest"]`

`TEST_PYTHON_VERSIONS`
: List of Python versions, e.g. `["3.13", "3.12", "3.11"]`

See the [GitHub documentation on variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables).

## Add extra workflow jobs

```toml
[github]
extra_lines = """
  another:
    uses: org/repo/.github/workflows/file.yml@main
"""
```
