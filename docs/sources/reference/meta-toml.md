# .meta.toml Options

<!-- diataxis: reference -->

`.meta.toml` is the per-repository configuration file for plone.meta. It
controls how each generated file is customized.

## `[meta]`

Managed by plone.meta itself. Do not edit manually.

`template`
: Configuration template type. Currently always `"default"`.

`commit-id`
: 8-character commit hash of the plone.meta version used.

## `[editorconfig]`

`extra_lines`
: Additional editorconfig rules appended to the generated file.

## `[flake8]`

`extra_lines`
: Additional flake8 configuration appended to the generated file.

## `[gitignore]`

`extra_lines`
: Additional gitignore patterns appended to the generated file.

## `[github]`

`jobs`
: List of CI jobs to enable. Available: `"qa"`, `"test"`, `"coverage"`,
  `"dependencies"`, `"release_ready"`, `"circular"`.

`ref`
: Branch or tag of plone/meta to reference for workflow files.
  Default: `"2.x"`.

`env`
: YAML-formatted environment variables for all jobs.

`os_dependencies`
: Space-separated Ubuntu package names to install before tests.

`py_versions`
: JSON array string of Python versions for the test matrix.

`extra_lines`
: Additional YAML appended to the workflow file.

## `[gitlab]`

`jobs`
: List of CI jobs. Available: `"lint"`, `"release-ready"`,
  `"dependencies"`, `"circular-dependencies"`, `"testing"`, `"coverage"`.

`custom_image`
: Docker image for CI jobs. Default: `"python:3.11-bullseye"`.

`os_dependencies`
: YAML-formatted apt-get install commands.

`extra_lines`
: Additional YAML appended to the CI configuration.

## `[pre_commit]`

`extra_lines`
: Additional pre-commit hook configuration.

`zpretty_extra_lines`
: Extra configuration for the zpretty hook.

`codespell_extra_lines`
: Extra configuration for the codespell hook.

`flake8_extra_lines`
: Extra configuration for the flake8 hook (e.g., additional_dependencies).

`i18ndude_extra_lines`
: Extra configuration for the i18ndude hook. Set `pass_filenames: false`
  to disable the check.

## `[pyproject]`

`extra_lines`
: Additional pyproject.toml tool configuration.

`codespell_ignores`
: Comma-separated words to ignore in codespell.

`codespell_skip`
: Comma-separated file patterns to skip in codespell.

`dependencies_ignores`
: Python list string of packages to ignore in dependency checks.

`dependencies_mappings`
: List of import-to-package mappings for z3c.dependencychecker.

`check_manifest_ignores`
: Additional patterns for check-manifest to ignore.

`check_manifest_extra_lines`
: Extra check-manifest configuration.

`black_extra_lines`
: Additional Black formatter configuration.

`isort_extra_lines`
: Additional isort configuration.

`towncrier_issue_format`
: Custom issue URL format for towncrier.

`towncrier_extra_lines`
: Extra towncrier configuration.

## `[tox]`

`test_runner`
: Test runner to use. `"pytest"` or `"zope.testrunner"` (default).

`test_path`
: Root path for test discovery. Auto-detected from `tests/` or `src/`
  if not set.

`test_extras`
: Additional extras to install for the test and coverage environments.

`test_deps_additional`
: Additional test dependencies (typically with mxdev source checkouts).

`test_environment_variables`
: Environment variables for test and coverage environments.

`constraints_file`
: URL or path to a custom pip constraints file.

`use_mxdev`
: Set to `true` to enable mxdev source checkout support.

`envlist_lines`
: Additional tox environment names to include.

`config_lines`
: Extra top-level tox configuration.

`testenv_options`
: Override default testenv options (e.g., basepython).

`extra_lines`
: Additional tox configuration sections.
