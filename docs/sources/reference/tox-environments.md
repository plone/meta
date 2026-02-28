# tox Environments

<!-- diataxis: reference -->

The generated `tox.ini` provides the following environments.

## `test`

Runs the test suite using the configured test runner.

- **zope.testrunner** (default): `zope-testrunner --all --test-path=<test_path>`
- **pytest**: `pytest <test_path>`

Installs the package with the `test` extra (unless `skip_test_extra` is
set) and any additional extras specified in `test_extras`.

Automatically detects and primes Playwright if
`plone.app.robotframework` is a dependency.

### Test matrix

When `use_test_matrix` is enabled (the default), the `test` environment
is expanded into a matrix of environments combining Plone versions with
Python versions. Environment names follow the pattern
`py<python_version>-plone<plone_version>`, for example:

- `py314-plone62`
- `py313-plone62`
- `py313-plone61`
- `py312-plone61`
- `py312-plone60`
- `py310-plone60`

Each generated environment uses the appropriate constraints file for its
Plone version (configured via `constraints_files` in the `[tox]` section).

The matrix is configured via the `[tox] test_matrix` option in
`.meta.toml`. See {doc}`/reference/meta-toml` for details.

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
