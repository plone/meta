---
myst:
  html_meta:
    "description": "Architecture of plone.meta: templates, rendering pipeline, and validation"
    "property=og:description": "Architecture of plone.meta: templates, rendering pipeline, and validation"
    "property=og:title": "Architecture"
    "keywords": "plone.meta, architecture, Jinja2, templates"
---

# Architecture

<!-- diataxis: explanation -->

## Overview

plone.meta is a code generation tool. It reads per-repository configuration
from {file}`.meta.toml`, renders Jinja2 templates, validates the output, and
manages git operations.

## Components

### Template engine

The core of plone.meta is a set of Jinja2 templates stored in
{file}`src/plone/meta/default/`. Each template corresponds to a configuration
file in the target repository.

Templates use `%(variable)s` style placeholders (Python string formatting
syntax within the Jinja2 context) for inserting configuration values. The
template engine has `trim_blocks` and `lstrip_blocks` enabled for clean
output, and `keep_trailing_newline` preserves proper file endings.

#### Modular tox templates

The {file}`tox.ini.j2` template uses a modular architecture with Jinja2
`{% include %}` directives. Rather than a single monolithic template,
the tox configuration is composed from focused sub-templates:

- {file}`tox-init.j2` -- tox initialization and configuration header
- {file}`tox-base.j2` -- base test environment definition
- {file}`tox-test-runner-specifics.j2` -- test runner specific settings
- {file}`tox-test-coverage.j2` -- coverage environment configuration
- {file}`tox-qa.j2` -- linting and formatting environments
- {file}`tox-plone-depending-qa.j2` -- Plone-specific QA environments

This modular structure makes the templates easier to maintain and extend.

### PackageConfiguration class

The {file}`config_package.py` module contains the `PackageConfiguration` class,
which orchestrates the entire process:

1. **Read** {file}`.meta.toml` from the target repository
2. **Detect** whether the repository is GitHub or GitLab hosted
   (based on the git remote URL)
3. **Render** each template with the configuration values
4. **Validate** generated files (TOML via `tomlkit`, YAML via `pyyaml`,
   INI via `configparser`, editorconfig via the `editorconfig` library)
5. **Write** files with meta hint comments
6. **Create** a towncrier news entry
7. **Commit** and optionally push

### File validation

Every generated file is validated before being written:

- **TOML files** are parsed with `tomlkit` and additionally validated
  with `validate-pyproject` for {file}`pyproject.toml`
- **YAML files** are parsed with `pyyaml`
- **INI files** are parsed with `configparser`
- **editorconfig files** are parsed with the `editorconfig` library

If validation fails, you are prompted to proceed or abort.

### Git workflow

`config-package` manages git operations:

1. Creates a new branch (or checks out an existing one)
2. Commits all changes with a descriptive message
3. Optionally pushes to the remote

Branch names follow the pattern `config-with-<type>-template-<commit-hash>`,
where the commit hash refers to the plone.meta repository, making it clear
which version of the templates was used.

## GitHub Actions workflow architecture

Rather than generating complete CI workflows inline, plone.meta generates
a thin {file}`meta.yml` that uses GitHub's `workflow_call` to reference reusable
workflows stored in the plone/meta repository itself. This means:

- Workflow logic is maintained in one place
- Repositories only need a small dispatch file
- Updates to CI logic do not require re-running `config-package`
  (as long as the `ref` points to a branch like `2.x`)

## Test matrix

A key architectural feature of plone.meta 2.x is the test matrix. Rather
than testing against a single Python version, plone.meta generates test
environments for all combinations of Plone versions and Python versions.
The default matrix covers Plone 6.0, 6.1, and 6.2 across Python 3.10
through 3.14.

The test matrix is reflected in multiple generated outputs:

- **tox.ini**: Environments named `py<version>-plone<version>` (e.g.,
  `py314-plone62`, `py312-plone61`)
- **GitHub Actions**: A dedicated {file}`test-matrix.yml` workflow runs all
  matrix combinations in CI
- **GitLab CI**: Matrix jobs are generated in {file}`.gitlab-ci.yml`

Each combination uses its own constraints file, allowing different Plone
versions to pin different dependency versions.

## Data flow

```
.meta.toml  ──>  PackageConfiguration  ──>  Jinja2 templates  ──>  Rendered files
                      │                                                  │
                      │                                                  v
                      └── git branch ──> commit ──> (push)        Validation
```
