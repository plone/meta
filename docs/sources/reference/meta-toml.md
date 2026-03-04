---
myst:
  html_meta:
    "description": "Complete reference of .meta.toml configuration options"
    "property=og:description": "Complete reference of .meta.toml configuration options"
    "property=og:title": ".meta.toml Options"
    "keywords": "plone.meta, .meta.toml, options, reference"
---

# .meta.toml Options

<!-- diataxis: reference -->

`.meta.toml` is the per-repository configuration file for plone.meta. It
controls how each generated file is customized.

:::{tip}
The Jinja2 template files in `src/plone/meta/default/` contain comments
documenting each available option. Check the templates for the most
up-to-date list.
:::

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
: List of CI jobs to enable in `meta.yml`. Available: `"qa"`, `"test"`,
  `"coverage"`, `"dependencies"`, `"release_ready"`, `"circular"`.
  Default: `["qa", "coverage", "dependencies", "release_ready", "circular"]`.

  :::{note}
  `"test"` is no longer included in the default jobs list. Testing is now
  handled by the separate `test-matrix.yml` workflow, which is generated
  automatically when `use_test_matrix` is enabled (the default).
  You can still add `"test"` to the jobs list if you need the legacy
  single-version test job.
  :::

`ref`
: Branch or tag of plone/meta to reference for workflow files.
  Default: `"2.x"`.

`env`
: YAML-formatted environment variables for all jobs.

`os_dependencies`
: Space-separated Ubuntu package names to install before tests.

`extra_lines_after_os_dependencies`
: Additional YAML lines inserted after the OS dependency installation step
  in the workflow. Useful for custom setup steps that need to run before
  tests (e.g., installing additional tools or configuring the environment).

`extra_lines`
: Additional YAML appended to the workflow file.

## `[gitlab]`

`jobs`
: List of CI jobs. Available: `"lint"`, `"release-ready"`,
  `"dependencies"`, `"circular-dependencies"`, `"testing"`, `"coverage"`.

`custom_images`
: Dictionary of Docker images keyed by Python version. Allows specifying
  different images for different Python versions in the CI matrix.

  Example:

  ```toml
  [gitlab]
  custom_images = {"3.14" = "python:3.14-trixie", "3.13" = "python:3.13-trixie"}
  ```

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

`constraints_files`
: Dictionary of pip constraints file URLs keyed by Plone version.
  This allows specifying different constraints for each Plone version
  in the test matrix.

  Example:

  ```
  [tox]
  constraints_files = {
      "6.1" = "https://dist.plone.org/release/6.1-latest/constraints.txt",
      "6.0" = "https://dist.plone.org/release/6.0-latest/constraints.txt",
  }
  ```

`use_test_matrix`
: Boolean. When `true` (the default), generates test environments for
  all combinations of Plone versions and Python versions defined in
  `test_matrix`. Set to `false` to disable the test matrix and use a
  single test environment instead.

`test_matrix`
: Dictionary defining which Python versions to test against each Plone
  version. Only used when `use_test_matrix` is `true`.

  Default:

  ```
  [tox]
  test_matrix = {
      "6.2" = ["3.14", "3.13", "3.12", "3.11", "3.10"],
      "6.1" = ["3.13", "3.12", "3.11", "3.10"],
      "6.0" = ["3.13", "3.12", "3.11", "3.10"],
  }
  ```

`skip_test_extra`
: Boolean. Set to `true` for packages that do not define a `test` extra
  in their packaging metadata. When enabled, the test environments will
  not attempt to install `[test]` extras.

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
