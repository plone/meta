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

plone.meta provides reusable GitHub Actions workflows and composite actions for use by Cookieplone-based projects.
These are **not** used by the `config-package` tool; they are designed to be called directly from downstream project workflows.

All workflows and actions are located in the plone.meta repository and referenced via `uses:` in your project's workflow files.

## Permissions

None of the reusable workflows declare a `permissions:` block of their own.
A reusable workflow cannot grant more access than its caller already has, so the **caller** is responsible for declaring the permissions each workflow needs, either at the workflow level or on the calling job.

The workflows that need more than the default read access say so in their own section below.

(shared-workflows-quoting)=

## Passing values to string inputs

Some inputs are forwarded to a shell command as an environment variable and expanded **unquoted**, so that a single input can supply several command-line arguments.
This has consequences worth knowing before you write such a value:

- The value is split on whitespace, and each resulting word becomes a separate argument.
- Quote characters are **not** removed.
  A value wrapped in `"` or `'` reaches the tool with those characters still attached, which usually changes the meaning of the argument.
- Glob metacharacters (`*`, `?`, `[`) are expanded against the working directory.

Write these values **without quotes**:

```yaml
# Correct: the shell splits this into two arguments.
zpretty-options: --extend-exclude /rss/(rss\.xml|search-rss)\.pt$

# Wrong: zpretty receives the argument with literal " characters around it,
# so the pattern matches nothing.
zpretty-options: '--extend-exclude "/rss/(rss\.xml|search-rss)\.pt$"'
```

There is currently no way to pass an argument that itself contains whitespace.

The inputs that behave this way are marked *word-split* in the tables below: {ref}`backend-lint <shared-workflows-backend-lint>`'s `zpretty-options` and {ref}`coverage <shared-workflows-coverage>`'s `os-packages`.

## Composite Actions

### setup_backend_uv

Sets up a Python backend environment using [uv](https://docs.astral.sh/uv/) as the package installer.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | `"3.12"` |
| `plone-version` | Plone version to install | Yes | `"6.2.0"` |
| `working-directory` | Directory to run the installation in | No | `"."` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v7
  - uses: plone/meta/.github/actions/setup_backend_uv@2.x
    with:
      python-version: "3.13"
      plone-version: "6.2.0"
```

### setup_frontend

Sets up a Node.js frontend environment with dependency installation.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | `"22.x"` |
| `working-directory` | Directory to run the installation in | No | `"."` |
| `cache` | Package-manager cache to enable | No | `"pnpm"` |
| `cache-dependency-path` | Lockfile glob used as the cache key | No | `"**/pnpm-lock.yaml"` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v7
  - uses: plone/meta/.github/actions/setup_frontend@2.x
    with:
      node-version: "22.x"
```

### setup_uv

Sets up the [uv](https://docs.astral.sh/uv/) package installer, without installing a project.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | `"3.12"` |
| `working-directory` | Directory to run `uv` in | No | `"."` |

**Example usage:**

```yaml
steps:
  - uses: actions/checkout@v7
  - uses: plone/meta/.github/actions/setup_uv@2.x
```

## Backend Workflows

(shared-workflows-backend-lint)=

### backend-lint

Runs backend linting checks: `ruff` (format and lint), `zpretty` (XML / ZCML), `pyroma` (package metadata), `check-python-versions`, and optionally `mypy` (typing).

Every check runs even if an earlier one fails, and the results are collected into a job summary table.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | |
| `plone-version` | Plone version to install | Yes | |
| `working-directory` | Directory to run the checks in | No | `"."` |
| `check-typing` | Run `mypy` type checking on `src` | No | `false` |
| `version-ruff` | Version of `ruff` to use | No | `"latest"` |
| `version-zpretty` | Version of `zpretty` to use | No | `"latest"` |
| `version-pyroma` | Version of `pyroma` to use | No | `"latest"` |
| `version-check-python` | Version of `check-python-versions` to use | No | `"latest"` |
| `zpretty-check-path` | Path checked by `zpretty` | No | `"src"` |
| `zpretty-options` | Additional command-line options passed to `zpretty` (*word-split*, see {ref}`shared-workflows-quoting`) | No | `""` |

**Example usage:**

```yaml
jobs:
  backend-lint:
    uses: plone/meta/.github/workflows/backend-lint.yml@2.x
    with:
      python-version: "3.12"
      plone-version: "6.1"
      zpretty-check-path: "src"
      zpretty-options: --extend-exclude /rss/(rss\.xml|search-rss)\.pt$
```

### backend-pytest

Runs the backend test suite by calling the project's `make test` target.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | |
| `plone-version` | Plone version to install | Yes | |
| `working-directory` | Directory to run the tests in | No | `"."` |

**Example usage:**

```yaml
jobs:
  backend-pytest:
    uses: plone/meta/.github/workflows/backend-pytest.yml@2.x
    with:
      python-version: "3.12"
      plone-version: "6.1"
```

### backend-pytest-coverage

Runs the backend test suite with coverage by calling the project's `make test-coverage` target, and writes the coverage report to the job summary.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | |
| `plone-version` | Plone version to install | Yes | |
| `working-directory` | Directory to run the tests in | No | `"."` |

**Example usage:**

```yaml
jobs:
  backend-pytest-coverage:
    uses: plone/meta/.github/workflows/backend-pytest-coverage.yml@2.x
    with:
      python-version: "3.12"
      plone-version: "6.1"
```

## Documentation Workflows

### docs-build

Builds project documentation with the project's `make install`, `make build`, `make linkcheckbroken` and `make vale` targets.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `python-version` | Python version to install | Yes | `"3.12"` |
| `working-directory` | Directory holding the documentation | No | `"."` |
| `check-links` | Run the broken-link check | No | `true` |
| `check-vale` | Run the Vale prose checks | No | `true` |

**Example usage:**

```yaml
jobs:
  docs-build:
    uses: plone/meta/.github/workflows/docs-build.yml@2.x
    with:
      python-version: "3.12"
      working-directory: "docs"
```

## Frontend Workflows

### frontend-acceptance

Runs frontend acceptance (end-to-end) tests with Cypress, against servers started by the workflow.
Screenshots and videos are uploaded as artifacts when the run fails.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | |
| `working-directory` | Directory to run the tests in | No | `"."` |

**Example usage:**

```yaml
jobs:
  frontend-acceptance:
    uses: plone/meta/.github/workflows/frontend-acceptance.yml@2.x
    with:
      node-version: "22.x"
```

### frontend-code

Runs frontend code quality checks by calling the project's `make lint` target.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | |
| `working-directory` | Directory to run the checks in | No | `"."` |

**Example usage:**

```yaml
jobs:
  frontend-code:
    uses: plone/meta/.github/workflows/frontend-code.yml@2.x
    with:
      node-version: "22.x"
```

### frontend-i18n

Validates the frontend internationalization setup by calling the project's `make i18n` target.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | |
| `working-directory` | Directory to run the check in | No | `"."` |

**Example usage:**

```yaml
jobs:
  frontend-i18n:
    uses: plone/meta/.github/workflows/frontend-i18n.yml@2.x
    with:
      node-version: "22.x"
```

### frontend-storybook

Builds Storybook with the project's `make storybook-build` target, and optionally publishes it to the `gh-pages` branch.

The deployment step only runs when `deploy` is `true` **and** the workflow is running on `refs/heads/main`.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | |
| `working-directory` | Directory to build Storybook in | No | `"."` |
| `deploy` | Publish the build to the `gh-pages` branch | No | `false` |

**Permissions required from the caller:**

| Scenario | Permissions the caller must grant |
|----------|-----------------------------------|
| `deploy: false` | none beyond the default |
| `deploy: true` | `contents: write` |

**Example usage:**

```yaml
jobs:
  frontend-storybook:
    uses: plone/meta/.github/workflows/frontend-storybook.yml@2.x
    permissions:
      contents: write
    with:
      node-version: "22.x"
      deploy: true
```

### frontend-unit

Runs frontend unit tests by calling the project's `make ci-test` target.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install | Yes | |
| `working-directory` | Directory to run the tests in | No | `"."` |

**Example usage:**

```yaml
jobs:
  frontend-unit:
    uses: plone/meta/.github/workflows/frontend-unit.yml@2.x
    with:
      node-version: "22.x"
```

## Container Image Workflows

The three container workflows share the same inputs and secrets.
Use `container-image-build` to validate a build, `container-image-push` to build and publish with a registry cache, or `container-image-build-push` for the simpler combined case.

```{note}
The registry credentials are named `username` and `password`, not `registry-username` and `registry-password`.
```

### container-image-build-push

Builds a container image and pushes it in a single job.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `base-tag` | Base tag applied to the image | Yes | |
| `working-directory` | Build context directory | Yes | `"."` |
| `image-name-prefix` | Prefix of the image name | Yes | |
| `image-name-suffix` | Suffix of the image name | Yes | |
| `platforms` | Target platforms to build for | No | `"linux/amd64"` |
| `dockerfile` | Dockerfile to build | No | `"Dockerfile"` |
| `registry` | Container registry to log in to | No | `"ghcr.io"` |
| `build-args` | Build arguments passed to `docker/build-push-action` | No | `""` |
| `push` | Push the image after building it | Yes | |

**Secrets:**

| Secret | Description | Required |
|--------|-------------|----------|
| `username` | Container registry username | Yes |
| `password` | Container registry password or token | Yes |

**Example usage:**

```yaml
jobs:
  container-image:
    uses: plone/meta/.github/workflows/container-image-build-push.yml@2.x
    with:
      base-tag: "1.0.0"
      working-directory: "backend"
      image-name-prefix: "ghcr.io/plone"
      image-name-suffix: "backend"
      push: true
    secrets:
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

### container-image-build

Builds a container image and writes a registry-backed build cache, without publishing the image itself.
Useful for validation in pull requests.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `base-tag` | Base tag applied to the image | Yes | |
| `working-directory` | Build context directory | Yes | `"."` |
| `image-name-prefix` | Prefix of the image name | Yes | |
| `image-name-suffix` | Suffix of the image name | Yes | |
| `image-cache-suffix` | Suffix of the image used to store the build cache | No | `"buildcache"` |
| `platforms` | Target platforms to build for | No | `"linux/amd64"` |
| `dockerfile` | Dockerfile to build | No | `"Dockerfile"` |
| `registry` | Container registry to log in to | No | `"ghcr.io"` |
| `build-args` | Build arguments passed to `docker/build-push-action` | No | `""` |
| `cache-key` | Cache key used for the build cache | No | `${{ github.ref_name }}` |

**Secrets:**

| Secret | Description | Required |
|--------|-------------|----------|
| `username` | Container registry username | Yes |
| `password` | Container registry password or token | Yes |

**Example usage:**

```yaml
jobs:
  container-image-build:
    uses: plone/meta/.github/workflows/container-image-build.yml@2.x
    with:
      base-tag: "1.0.0"
      working-directory: "backend"
      image-name-prefix: "ghcr.io/plone"
      image-name-suffix: "backend"
    secrets:
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

### container-image-push

Builds a container image reusing the cache written by `container-image-build`, and pushes it to the registry.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `base-tag` | Base tag applied to the image | Yes | |
| `working-directory` | Build context directory | Yes | `"."` |
| `image-name-prefix` | Prefix of the image name | Yes | |
| `image-name-suffix` | Suffix of the image name | Yes | |
| `image-cache-suffix` | Suffix of the image holding the build cache | No | `"buildcache"` |
| `platforms` | Target platforms to build for | No | `"linux/amd64"` |
| `dockerfile` | Dockerfile to build | No | `"Dockerfile"` |
| `registry` | Container registry to log in to | No | `"ghcr.io"` |
| `build-args` | Build arguments passed to `docker/build-push-action` | No | `""` |
| `cache-key` | Cache key used for the build cache | No | `${{ github.ref_name }}` |

**Secrets:**

| Secret | Description | Required |
|--------|-------------|----------|
| `username` | Container registry username | Yes |
| `password` | Container registry password or token | Yes |

**Example usage:**

```yaml
jobs:
  container-image-push:
    uses: plone/meta/.github/workflows/container-image-push.yml@2.x
    with:
      base-tag: "1.0.0"
      working-directory: "backend"
      image-name-prefix: "ghcr.io/plone"
      image-name-suffix: "backend"
    secrets:
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

## tox Workflows

These workflows target packages configured by the `config-package` tool, and drive the {doc}`tox environments <tox-environments>` that it generates.
Each one runs the `init` environment first when the package defines it.

Unlike the workflows above, they take no `working-directory` input: they run at the root of the checkout.

(shared-workflows-coverage)=

### coverage

Runs the `coverage` tox environment and writes its report to the job summary.

**Inputs:**

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `os-packages` | Debian packages to install with `apt-get` before running the tests (*word-split*, see {ref}`shared-workflows-quoting`) | No | `""` |

**Example usage:**

```yaml
jobs:
  coverage:
    uses: plone/meta/.github/workflows/coverage.yml@2.x
    with:
      os-packages: libxml2-dev libxslt1-dev
```

### circular

Runs the `circular` tox environment to report circular dependencies.
The workflow installs `libgraphviz-dev` for you.

**Example usage:**

```yaml
jobs:
  circular:
    uses: plone/meta/.github/workflows/circular.yml@2.x
```

### dependencies

Runs the `dependencies` tox environment to report on the package's dependencies.

**Example usage:**

```yaml
jobs:
  dependencies:
    uses: plone/meta/.github/workflows/dependencies.yml@2.x
```

### qa

Runs the `lint` tox environment.

**Example usage:**

```yaml
jobs:
  qa:
    uses: plone/meta/.github/workflows/qa.yml@2.x
```

### release_ready

Runs the `release-check` tox environment to report whether the package is ready to be released.

**Example usage:**

```yaml
jobs:
  release_ready:
    uses: plone/meta/.github/workflows/release_ready.yml@2.x
```

## Version pinning

All examples above use `@2.x` to track the latest 2.x release.
You can pin to a specific tag (e.g., `@v2.4.0`) for reproducible builds:

```yaml
uses: plone/meta/.github/workflows/backend-lint.yml@v2.4.0
```
