---
myst:
  html_meta:
    "description": "Configuration philosophy: sane defaults with simple extensibility"
    "property=og:description": "Configuration philosophy: sane defaults with simple extensibility"
    "property=og:title": "Configuration Philosophy"
    "keywords": "plone.meta, configuration, philosophy, defaults"
---

# Configuration Philosophy

<!-- diataxis: explanation -->

## Sane defaults with simple extensibility

plone.meta is designed around two principles:

1. **Provide sane defaults** that work for the majority of Plone packages.
2. **Allow extension** without complexity.

## The extra_lines approach

Rather than adding a configuration option for every possible customization, almost all generated files support an `extra_lines` key in {file}`.meta.toml`.
This key accepts raw configuration text that is appended to the generated file.

This approach has several advantages:

- **Simplicity:** No need to learn a custom configuration DSL. You write
  the same syntax the target file expects.
- **Flexibility:** Anything the target format supports can be added.
- **Low maintenance:** New configuration options in tools (flake8, tox,
  isort, etc.) do not require changes to plone.meta itself.

The tradeoff is that `extra_lines` content is not validated against the template -- it is simply appended.
But this is intentional: it keeps the tool simple and avoids becoming a configuration management framework.

## When extra_lines is not enough

For cases where appending text is insufficient -- where the configuration needs to *change* the template output rather than extend it -- plone.meta provides specific configuration keys. Examples:

- `test_runner` to switch between pytest and zope.testrunner
- `constraints_file` to override the default pip constraints URL
- `custom_image` to change the GitLab CI Docker image
- `jobs` to select which CI jobs are enabled

These options are added conservatively.
If you need a customization that plone.meta does not support, you can [request it](https://github.com/plone/meta/issues/new).

## Don't edit generated files

This is the cardinal rule of plone.meta: **never directly edit the files that plone.meta manages.** Any changes will be overwritten the next time `config-package` runs.

All customization goes through {file}`.meta.toml`.
This single file captures the complete delta between the defaults and your repository's needs, making it easy to review, maintain, and update.
