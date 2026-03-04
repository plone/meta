---
myst:
  html_meta:
    "description": "CLI reference for multi-call bulk update command"
    "property=og:description": "CLI reference for multi-call bulk update command"
    "property=og:title": "multi-call CLI *(experimental)*"
    "keywords": "plone.meta, multi-call, CLI, bulk update"
---

# multi-call CLI *(experimental)*

<!-- diataxis: reference -->

:::{warning}
This tool originates from `zope.meta` and has not been extensively tested
in the `plone.meta` context. The default branch is `master` instead of
`main`. Use with caution.
:::

## Synopsis

```
multi-call SCRIPT PACKAGES_FILE CLONES_DIR [SCRIPT_ARGS...]
```

## Positional arguments

`SCRIPT`
: Path to the Python script to run on each package
  (typically `config-package`).

`PACKAGES_FILE`
: Path to a text file listing repository names, one per line.
  Lines starting with `#` are skipped.

`CLONES_DIR`
: Directory where repositories are cloned. If a repository does not
  exist here, it is cloned from GitHub. If it already exists, it is
  cleaned, switched to `master`, and pulled.

`SCRIPT_ARGS`
: Additional arguments passed to `SCRIPT` for each package.

## Behavior

For each package listed in `PACKAGES_FILE`:

1. If no clone exists in `CLONES_DIR`, the repository is cloned.
2. If a clone exists, uncommitted changes are stashed, the `master`
   branch is checked out, and the latest changes are pulled.
3. The specified script is run with the package path and any extra arguments.

:::{caution}
Uncommitted changes are stashed automatically.
Use `git stash pop` to recover them.
:::
