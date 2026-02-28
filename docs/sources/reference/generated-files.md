# Generated Files

<!-- diataxis: reference -->

`plone.meta` generates the following files in the target repository.
Each file is rendered from a Jinja2 template in `src/plone/meta/default/`.

:::{important}
Do not edit these files directly. All customization goes into `.meta.toml`.
:::

## .meta.toml

**Template:** Created programmatically
**Purpose:** plone.meta's own configuration file. Stores the template type,
commit ID, and all per-repository customizations. This is the *only* file
you should edit.

## .editorconfig

**Template:** `editorconfig.j2`
**Purpose:** Editor configuration for consistent formatting across IDEs.
Sets 4-space indentation for Python, 2-space for XML/YAML/ZCML, and
Unix line endings.

## .flake8

**Template:** `flake8.j2`
**Purpose:** Flake8 configuration. Ignores rules that conflict with Black
(E501, W503, E203, E231) and enables doctests.

## .gitignore

**Template:** `gitignore.j2`
**Purpose:** Git ignore patterns for Python projects, build artifacts,
test output, editor files, Buildout directories, and mxdev artifacts.

## .github/workflows/meta.yml

**Template:** `meta.yml.j2`
**Purpose:** GitHub Actions workflow for repositories hosted on GitHub.
Uses `workflow_call` to reference reusable workflows from the plone/meta
repository (qa, test, coverage, dependencies, release_ready, circular).

Only generated for GitHub-hosted repositories.

## .gitlab-ci.yml

**Template:** `gitlab-ci.yml.j2`
**Purpose:** GitLab CI pipeline configuration. Defines jobs for linting,
testing, coverage, dependency checking, and release readiness.

Only generated for GitLab-hosted repositories.

## .pre-commit-config.yaml

**Template:** `pre-commit-config.yaml.j2`
**Purpose:** Pre-commit hook configuration. Includes pyupgrade, isort,
black, zpretty, flake8, codespell, check-manifest, pyroma,
check-python-versions, and i18ndude.

## pyproject.toml

**Template:** `pyproject.toml.j2`
**Purpose:** Python tooling configuration for isort, black, codespell,
check-manifest, and z3c.dependencychecker. Also includes towncrier
configuration if a `news/` folder exists.

:::{note}
plone.meta manages only the `[tool.*]` sections. The `[project]` and
`[build-system]` sections are left untouched if they already exist.
:::

## tox.ini

**Template:** `tox.ini.j2`
**Purpose:** Tox environment definitions for testing, linting, coverage,
dependency checking, release readiness, and circular dependency detection.
This is considered the most important generated file.

## .github/dependabot.yml

**Template:** `dependabot.yml` (static)
**Purpose:** Dependabot configuration for automatic GitHub Actions updates
on a weekly schedule.

## news/.changelog_template.jinja

**Template:** `changelog_template.jinja` (static)
**Purpose:** Towncrier template for Markdown-formatted changelogs.
Only generated if a `news/` folder exists and `CHANGES.md` is used.
