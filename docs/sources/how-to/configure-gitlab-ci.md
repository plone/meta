# Configure GitLab CI

<!-- diataxis: how-to -->

For repositories hosted on GitLab, `plone.meta` generates a `.gitlab-ci.yml`
file instead of GitHub Actions workflows.

## Select CI jobs

```toml
[gitlab]
jobs = [
    "lint",
    "release-ready",
    "dependencies",
    "circular-dependencies",
    "testing",
    "coverage",
]
```

## Use a custom Docker image

```toml
[gitlab]
custom_image = "python:3.11-bullseye"
```

The default image is `python:3.11-bullseye`.

## Install OS-level dependencies

```toml
[gitlab]
os_dependencies = """
    - apt-get install libxslt libxml2
"""
```

## Add extra configuration

```toml
[gitlab]
extra_lines = """
deploy:
  stage: deploy
  script:
    - echo "deploying"
"""
```
