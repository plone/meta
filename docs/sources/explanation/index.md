---
myst:
  html_meta:
    "description": "Background knowledge, design decisions, and philosophy of plone.meta"
    "property=og:description": "Background knowledge, design decisions, and philosophy of plone.meta"
    "property=og:title": "Explanation"
    "keywords": "plone.meta, explanation, design decisions"
---

# Explanation

<!-- diataxis: explanation -->

Background knowledge, design decisions, and project philosophy.
These pages help you understand *why* plone.meta works the way it does.

::::{grid} 2
:gutter: 3

:::{grid-item-card} Why Standardize?
:link: why-standardize
:link-type: doc

The motivation behind plone.meta: what problems it solves, what it replaces, and why centralized configuration management matters for the Plone ecosystem.
:::

:::{grid-item-card} Architecture
:link: architecture
:link-type: doc

How plone.meta works internally: template rendering, file generation, validation, and the git workflow.
:::

:::{grid-item-card} Configuration Philosophy
:link: configuration-philosophy
:link-type: doc

The design principles behind the `extra_lines` approach: sane defaults with simple extensibility.
:::

:::{grid-item-card} Scope and Limitations
:link: scope
:link-type: doc

What plone.meta covers and what it intentionally does not cover.
Projects that should not use plone.meta.
:::

::::

```{toctree}
---
hidden: true
---
why-standardize
architecture
configuration-philosophy
scope
```
