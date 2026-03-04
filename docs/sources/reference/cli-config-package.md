---
myst:
  html_meta:
    "description": "CLI reference for config-package command"
    "property=og:description": "CLI reference for config-package command"
    "property=og:title": "config-package CLI"
    "keywords": "plone.meta, config-package, CLI, reference"
---

# config-package CLI

<!-- diataxis: reference -->

## Synopsis

```
config-package [OPTIONS] PATH
```

`PATH` is the filesystem path to the target Python package repository.

## Options

`--branch BRANCH_NAME`
: Git branch name to create for the changes.
  Default: auto-generated as `config-with-<type>-template-<commit-hash>`.

  :::{important}
  Use `--branch current` to update the current branch instead of creating
  a new one. This is essential when re-running `config-package` after
  changing {file}`.meta.toml`.
  :::

`--commit-msg MSG`
: Custom commit message.
  Default: an auto-generated message describing the configuration update.

`--no-commit`
: Do not automatically commit changes after the configuration run.
  Useful for reviewing changes before committing.

`--push`
: Push changes to the remote after the configuration run.
  Default: changes are *not* pushed.

`--tox`
: Run `tox` on the repository after applying configuration.
  Default: tox is *not* run.

`--track`
: Add the package to {file}`packages.txt` in the plone.meta repository.
  Default: packages are *not* tracked.

`-t, --type TYPE`
: Configuration type. Currently only `default` is available.
  Only needed the first time; the value is stored in {file}`.meta.toml`.

`-h, --help`
: Display help and exit.

## Behavior

1. Creates a new git branch from the current branch (unless `--branch current`).
2. Reads {file}`.meta.toml` if present, or creates it with defaults.
3. Renders Jinja2 templates into configuration files.
4. Validates generated files (TOML, YAML, INI, editorconfig).
5. Creates a towncrier news entry.
6. Commits changes (unless `--no-commit`).
7. Optionally pushes and/or runs tox.

## Exit codes

`0`
: Success.

Non-zero
: An error occurred during configuration. The error message is printed to
  stderr. You are prompted to proceed or abort.
