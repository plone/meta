---
myst:
  html_meta:
    "description": "How-to guides for common plone.meta tasks"
    "property=og:description": "How-to guides for common plone.meta tasks"
    "property=og:title": "How-To Guides"
    "keywords": "plone.meta, how-to, guides"
---

# How-To Guides

<!-- diataxis: how-to -->

Goal-oriented recipes for common tasks.
Each guide answers a specific "how do I..." question.

::::{grid} 2
:gutter: 3

:::{grid-item-card} Install plone.meta
:link: install
:link-type: doc

Clone the repository and install plone.meta into a virtual environment.
:::

:::{grid-item-card} Customize via .meta.toml
:link: customize-meta-toml
:link-type: doc

Add custom configuration for flake8, tox, pyproject.toml, pre-commit, and more without editing generated files.
:::

:::{grid-item-card} Configure GitHub Actions
:link: configure-github-actions
:link-type: doc

Set up CI jobs, Python version matrices, OS dependencies, and environment variables for GitHub-hosted repositories.
:::

:::{grid-item-card} Configure GitLab CI
:link: configure-gitlab-ci
:link-type: doc

Set up CI pipelines for GitLab-hosted repositories, including custom Docker images and OS dependencies.
:::

:::{grid-item-card} Re-enable GitHub Actions
:link: re-enable-actions
:link-type: doc

Re-enable GitHub Actions workflows that were auto-disabled due to repository inactivity.
:::

:::{grid-item-card} Use a Custom Branch Name
:link: custom-branch
:link-type: doc

Control the git branch name created by config-package, or update the current branch.
:::

:::{grid-item-card} Write Custom Templates
:link: write-custom-templates
:link-type: doc

Create a custom configuration type with your own Jinja2 templates when `extra_lines` is not enough.
:::

::::

```{toctree}
---
hidden: true
---
install
customize-meta-toml
configure-github-actions
configure-gitlab-ci
re-enable-actions
custom-branch
write-custom-templates
```
