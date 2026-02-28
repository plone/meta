# Scope and Limitations

<!-- diataxis: explanation -->

## What plone.meta covers

plone.meta manages configuration files for **single-package Python
repositories** in the Plone ecosystem. This includes:

- Development tool configuration (linting, formatting, editor settings)
- Test environment setup (tox)
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Pre-commit hooks
- Release readiness checks
- Dependency validation

## What plone.meta does not cover

### JavaScript and frontend projects

Volto and other JavaScript-based projects have their own ecosystem with
different tooling (ESLint, Prettier, Jest, etc.). plone.meta is strictly
for Python projects.

### Monorepo projects

Repositories with both backend and frontend code bases -- such as those
created by [Cookieplone](https://github.com/plone/cookieplone) -- are
not supported. plone.meta expects a single Python package at the top level
of the repository.

### Multi-version support

Projects that support multiple versions of Plone in the same branch
(e.g., using different dependency sets for Plone 5 and Plone 6) are not
supported. plone.meta assumes one Plone version per branch.

### Package scaffolding

plone.meta does not create new packages. It configures existing ones.
For creating new Plone packages, use
[Cookieplone](https://github.com/plone/cookieplone) or
[plonecli](https://pypi.org/project/plonecli/).

### Custom CI logic

plone.meta generates standardized CI pipelines. If your package needs
significantly custom CI logic (custom Docker builds, deployment steps,
integration tests with external services), you can extend via `extra_lines`,
but at some point it may make more sense to maintain CI configuration
manually.
