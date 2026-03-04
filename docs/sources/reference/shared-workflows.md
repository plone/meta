---
myst:
  html_meta:
    "description": "Reusable GitHub Actions workflows and composite actions from plone.meta"
    "property=og:description": "Reusable GitHub Actions workflows and composite actions from plone.meta"
    "property=og:title": "Shared Workflows & Actions"
    "keywords": "plone.meta, GitHub Actions, workflows, composite actions"
---

# Shared Workflows & Actions

<!-- diataxis: reference -->

plone.meta provides reusable GitHub Actions workflows and composite actions
for use by Cookieplone-based projects.
These are **not** used by the `config-package` tool; they are designed to be
called directly from downstream project workflows.

All workflows and actions are located in the plone.meta repository and
referenced via `uses:` in your project's workflow files.

## Composite Actions

### setup_backend_uv

Sets up a Python backend environment using [uv](https://docs.astral.sh/uv/)
as the package installer.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | No | `"3.12"` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: plone/meta/.github/actions/setup_backend_uv@2.x
    with:
      python-version: "3.13"
```

### setup_frontend

Sets up a Node.js frontend environment with dependency installation.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | No | `"22.x"` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: plone/meta/.github/actions/setup_frontend@2.x
    with:
      node-version: "22.x"
```

### setup_uv

Sets up the [uv](https://docs.astral.sh/uv/) package installer.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `uv-version` | Version of uv to install | No | `"latest"` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: plone/meta/.github/actions/setup_uv@2.x
```

## Backend Workflows

### backend-lint

Runs backend linting checks.

**Example usage:**

```yaml
jobs:
  backend-lint:
    uses: plone/meta/.github/workflows/backend-lint.yml@2.x
```

### backend-pytest

Runs backend tests with pytest.

**Example usage:**

```yaml
jobs:
  backend-pytest:
    uses: plone/meta/.github/workflows/backend-pytest.yml@2.x
```

### backend-pytest-coverage

Runs backend tests with coverage reporting.

**Example usage:**

```yaml
jobs:
  backend-pytest-coverage:
    uses: plone/meta/.github/workflows/backend-pytest-coverage.yml@2.x
```

## Documentation Workflows

### docs-build

Builds project documentation.

**Example usage:**

```yaml
jobs:
  docs-build:
    uses: plone/meta/.github/workflows/docs-build.yml@2.x
```

## Frontend Workflows

### frontend-acceptance

Runs frontend acceptance (end-to-end) tests.

**Example usage:**

```yaml
jobs:
  frontend-acceptance:
    uses: plone/meta/.github/workflows/frontend-acceptance.yml@2.x
```

### frontend-code

Runs frontend code quality checks (linting, formatting).

**Example usage:**

```yaml
jobs:
  frontend-code:
    uses: plone/meta/.github/workflows/frontend-code.yml@2.x
```

### frontend-i18n

Validates frontend internationalization (i18n) setup.

**Example usage:**

```yaml
jobs:
  frontend-i18n:
    uses: plone/meta/.github/workflows/frontend-i18n.yml@2.x
```

### frontend-storybook

Builds and validates Storybook stories.

**Example usage:**

```yaml
jobs:
  frontend-storybook:
    uses: plone/meta/.github/workflows/frontend-storybook.yml@2.x
```

### frontend-unit

Runs frontend unit tests.

**Example usage:**

```yaml
jobs:
  frontend-unit:
    uses: plone/meta/.github/workflows/frontend-unit.yml@2.x
```

## Container Image Workflows

### container-image-build-push

Builds and pushes a container image in a single workflow.
Combines the build and push steps for convenience.

**Secrets:**

| Secret | Description | Required |
|--------|-------------|----------|
| `registry-username` | Container registry username | Yes |
| `registry-password` | Container registry password or token | Yes |

**Example usage:**

```yaml
jobs:
  container-image:
    uses: plone/meta/.github/workflows/container-image-build-push.yml@2.x
    secrets:
      registry-username: ${{ secrets.REGISTRY_USERNAME }}
      registry-password: ${{ secrets.REGISTRY_PASSWORD }}
```

### container-image-build

Builds a container image without pushing.
Useful for validation in pull requests.

**Example usage:**

```yaml
jobs:
  container-image-build:
    uses: plone/meta/.github/workflows/container-image-build.yml@2.x
```

### container-image-push

Pushes a previously built container image to a registry.

**Secrets:**

| Secret | Description | Required |
|--------|-------------|----------|
| `registry-username` | Container registry username | Yes |
| `registry-password` | Container registry password or token | Yes |

**Example usage:**

```yaml
jobs:
  container-image-push:
    uses: plone/meta/.github/workflows/container-image-push.yml@2.x
    secrets:
      registry-username: ${{ secrets.REGISTRY_USERNAME }}
      registry-password: ${{ secrets.REGISTRY_PASSWORD }}
```

## Version pinning

All examples above use `@2.x` to track the latest 2.x release.
You can pin to a specific tag (e.g., `@v2.4.0`) for reproducible builds:

```yaml
uses: plone/meta/.github/workflows/backend-lint.yml@v2.4.0
```
