# Architecture

<!-- diataxis: explanation -->

## Overview

plone.meta is a code generation tool. It reads per-repository configuration
from `.meta.toml`, renders Jinja2 templates, validates the output, and
manages git operations.

## Components

### Template engine

The core of plone.meta is a set of Jinja2 templates stored in
`src/plone/meta/default/`. Each template corresponds to a configuration
file in the target repository.

Templates use `%(variable)s` style placeholders (Python string formatting
syntax within the Jinja2 context) for inserting configuration values. The
template engine has `trim_blocks` and `lstrip_blocks` enabled for clean
output, and `keep_trailing_newline` preserves proper file endings.

### PackageConfiguration class

The `config_package.py` module contains the `PackageConfiguration` class,
which orchestrates the entire process:

1. **Read** `.meta.toml` from the target repository
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
  with `validate-pyproject` for `pyproject.toml`
- **YAML files** are parsed with `pyyaml`
- **INI files** are parsed with `configparser`
- **editorconfig files** are parsed with the `editorconfig` library

If validation fails, the user is prompted to proceed or abort.

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
a thin `meta.yml` that uses GitHub's `workflow_call` to reference reusable
workflows stored in the plone/meta repository itself. This means:

- Workflow logic is maintained in one place
- Repositories only need a small dispatch file
- Updates to CI logic do not require re-running `config-package`
  (as long as the `ref` points to a branch like `2.x`)

## Data flow

```
.meta.toml  ──>  PackageConfiguration  ──>  Jinja2 templates  ──>  Rendered files
                      │                                                  │
                      │                                                  v
                      └── git branch ──> commit ──> (push)        Validation
```
