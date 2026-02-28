# tox Environments

<!-- diataxis: reference -->

The generated `tox.ini` provides the following environments.

## `test`

Runs the test suite using the configured test runner.

- **zope.testrunner** (default): `zope-testrunner --all --test-path=<test_path>`
- **pytest**: `pytest <test_path>`

Installs the package with the `test` extra and any additional extras
specified in `test_extras`.

Automatically detects and primes Playwright if
`plone.app.robotframework` is a dependency.

## `coverage`

Runs the test suite with coverage measurement and generates reports
in Markdown, XML, and HTML formats.

## `release-check`

Validates the package is ready for release:

- Runs `towncrier --draft` to check changelog entries
- Builds the distribution with `python -m build`
- Checks the distribution with `twine check`

## `lint`

Runs code quality and formatting checks via `pre-commit run --all-files`.

## `format`

Applies auto-formatting via `pre-commit run --all-files` with formatters
only (isort, black, zpretty).

## `dependencies`

Validates that all dependencies are properly declared using
`z3c.dependencychecker`.

## `dependencies-graph`

Generates a visual dependency graph using `pipdeptree` and
`graphviz`.

## `circular`

Checks for circular dependencies using `pipdeptree` and `pipforester`.
Requires `libgraphviz-dev` for graph visualization.
