# plone.meta

`plone.meta` standardizes configuration files across Plone-related Python repositories.

It generates and manages `.editorconfig`, `.flake8`, `.gitignore`, `pyproject.toml`, `tox.ini`, `.pre-commit-config.yaml`, and CI pipelines (GitHub Actions, GitLab CI) from Jinja2 templates, with per-repository customization via `.meta.toml`.


## Quick Start

```shell
python3 -m venv venv
venv/bin/pip install plone.meta
venv/bin/config-package /path/to/your/package
```


## Documentation

Full documentation is available at **https://plone.github.io/meta/**

-   [Tutorials](https://plone.github.io/meta/tutorials/) -- Step-by-step lessons to get started
-   [How-To Guides](https://plone.github.io/meta/how-to/) -- Solutions to specific problems
-   [Reference](https://plone.github.io/meta/reference/) -- Configuration options and CLI details
-   [Explanation](https://plone.github.io/meta/explanation/) -- Architecture, design decisions, and philosophy


## Commands

-   `config-package` -- Generate configuration files for a single repository
-   `multi-call` -- Apply configuration across multiple repositories
-   `re-enable-actions` -- Re-enable auto-disabled GitHub Actions


## GitHub Actions Shared Automations

`plone/meta` also provides reusable workflows and composite actions for GitHub Actions.
See the [full documentation](https://plone.github.io/meta/reference/shared-workflows/) for details.


## Scope

`plone/meta` covers single-package Python repositories.
It does not cover:

-   Volto or other JavaScript-based projects
-   Monorepo projects (backend + frontend)
-   Projects supporting multiple Plone versions in the same branch


## License

GPLv2. See [LICENSE](LICENSE).
