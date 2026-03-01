# tox Environments

<!-- diataxis: reference -->

The generated `tox.ini` provides the following environments.

## `test`

Runs the test suite using the configured test runner. plone.meta chooses
the runner based on the `test_runner` option in `.meta.toml`: either
`pytest` or `zope.testrunner` (the default). The exact commands are
managed by tox and may change between releases.

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
- `py312-plone61`

Each generated environment uses the appropriate constraints file for its
Plone version (configured via `constraints_files` in the `[tox]` section).

The matrix is configured via the `[tox] test_matrix` option in
`.meta.toml`. See {doc}`/reference/meta-toml` for details.

## `coverage`

Runs the test suite with coverage measurement and generates reports
in Markdown, XML, and HTML formats.

## `release-check`

Validates the package is ready for release by checking changelog entries,
building the distribution, and verifying the result.

## `lint`

Runs code quality and formatting checks via `pre-commit run --all-files`.

## `format`

Applies auto-formatting by running each formatter individually via
`pre-commit run <formatter>`. Each formatter is invoked separately so
that its changes can be committed and inspected independently. This is
particularly useful when porting old code, where subtle autoformatter
changes might break the test suite.

## `dependencies`

Validates that all dependencies are properly declared using
`z3c.dependencychecker`.

## `dependencies-graph`

Generates a visual dependency graph using `pipdeptree` and
`graphviz`.

## `circular`

Checks for circular dependencies using `pipdeptree` and `pipforester`.
Requires `libgraphviz-dev` for graph visualization.
