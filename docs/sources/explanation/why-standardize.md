---
myst:
  html_meta:
    "description": "Why standardize configuration across Plone packages"
    "property=og:description": "Why standardize configuration across Plone packages"
    "property=og:title": "Why Standardize?"
    "keywords": "plone.meta, standardization, consistency, developer experience"
---

# Why Standardize?

<!-- diataxis: explanation -->

## The problem

The Plone ecosystem consists of over 100 Python packages, each maintained by
different people at different times.
Without coordination, each repository develops its own approach to:

- Test configuration and runners
- Code formatting and linting rules
- CI pipeline setup
- Pre-commit hooks
- Editor settings
- Release processes

This leads to fragmentation.
A developer picking up a new package has to figure out from scratch how to
run tests, what formatting rules apply, and whether the CI pipeline is current.
Contributions become harder because the answer to "how do I run the tests?"
differs for every package.

## What plone.meta solves

By using plone.meta, every Plone package answers the same set of questions
in the same way:

- **Do the tests pass?** `tox -e test`
- **What's the test coverage?** `tox -e coverage`
- **Is the package release-ready?** `tox -e release-check`
- **Are dependencies declared correctly?** `tox -e dependencies`
- **Are there circular dependencies?** `tox -e circular`
- **Is the code formatted?** `tox -e format`
- **Do quality checks pass?** `tox -e lint`

The developer experience is identical everywhere.

## Centralized updates

Tooling evolves.
Linting rules change.
New Python versions are released.
CI providers update their APIs.
Without centralization, updating 100+
repositories is impractical -- each one needs manual changes, review, and
testing.

With plone.meta, a tooling update happens in one place (the templates),
and is then rolled out to all packages via `config-package` or `multi-call`.
This makes it practical to:

- Adopt new tools (e.g., switching formatters)
- Update CI pipelines for new Python versions
- Fix a security issue in a CI configuration

## Adoption

plone.meta is mandatory for repositories under the
[GitHub Plone organization](https://github.com/plone).
It is encouraged for repositories under the
[collective Plone organization](https://github.com/collective) and for
private packages.
