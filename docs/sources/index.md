---
myst:
  html_meta:
    "description": "plone.meta - standardize configuration across Plone Python packages"
    "property=og:description": "plone.meta - standardize configuration across Plone Python packages"
    "property=og:title": "plone.meta"
    "keywords": "plone.meta, Plone, configuration, CI/CD, tox, GitHub Actions"
---

# plone.meta

<!-- diataxis: landing -->

Standardize configuration files across Plone-related Python repositories.

`plone.meta` generates and manages a consistent set of configuration files --
from CI pipelines and linting to tox environments and editor settings --
so every Plone package provides the same developer experience.

**Key capabilities:**

- Generate `.editorconfig`, `.flake8`, `.gitignore`, `pyproject.toml`, `tox.ini`, `.pre-commit-config.yaml` from Jinja2 templates
- GitHub Actions and GitLab CI workflows, centrally managed
- Test matrix: automatically test all combinations of Plone versions (6.0, 6.1, 6.2) and Python versions (3.10--3.14)
- Shared reusable GitHub Actions workflows and composite actions for Cookieplone projects
- Per-repository customization via `.meta.toml` without editing generated files
- Bulk updates across 100+ Plone packages with a single command
- Validation of generated TOML, YAML, INI, and editorconfig files
- Install from PyPI: `pip install plone.meta`

**Requirements:** Python 3.9+

## Documentation

::::{grid} 2
:gutter: 3

:::{grid-item-card} Tutorials
:link: tutorials/index
:link-type: doc

**Learning-oriented** -- Step-by-step lessons to get started.

*Start here if you are new to plone.meta.*
:::

:::{grid-item-card} How-To Guides
:link: how-to/index
:link-type: doc

**Goal-oriented** -- Solutions to specific problems.

*Use these when you need to accomplish something.*
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc

**Information-oriented** -- Configuration options and CLI details.

*Consult when you need detailed information.*
:::

:::{grid-item-card} Explanation
:link: explanation/index
:link-type: doc

**Understanding-oriented** -- Architecture, design decisions, and philosophy.

*Read to deepen your understanding of how and why it works.*
:::

::::

## Quick Start

1. {doc}`Install plone.meta <how-to/install>`
2. {doc}`Configure your first package <tutorials/first-package>`
3. {doc}`Customize via .meta.toml <how-to/customize-meta-toml>`

```{toctree}
---
maxdepth: 3
caption: Documentation
titlesonly: true
hidden: true
---
tutorials/index
how-to/index
reference/index
explanation/index
```
