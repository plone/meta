---
myst:
  html_meta:
    "description": "Customize generated files via .meta.toml"
    "property=og:description": "Customize generated files via .meta.toml"
    "property=og:title": "Customize via .meta.toml"
    "keywords": "plone.meta, .meta.toml, customization, configuration"
---

# Customize via .meta.toml

<!-- diataxis: how-to -->

All customizations for generated files go into {file}`.meta.toml` in the target repository.

:::{tip}
All available configuration options are also documented as comments in each Jinja2 template file under {file}`src/plone/meta/default/`. Browsing the templates is a good way to discover options.
:::

## General pattern

Most configuration files support an `extra_lines` key that appends your custom configuration to the generated output:

```toml
[section_name]
extra_lines = """
your custom configuration here
"""
```

:::{important}
Never directly edit the generated files. Your changes will be overwritten the next time `config-package` runs.
:::

## .editorconfig

```toml
[editorconfig]
extra_lines = """
[*.{json,jsonl,js,jsx,ts,tsx,css,less,scss}]
indent_size = 4
"""
```

## .flake8

```toml
[flake8]
extra_lines = """
per-file-ignores =
    setup.py:T20
"""
```

## .gitignore

```toml
[gitignore]
extra_lines = """
my-custom-folder/
*.sqlite
"""
```

## .pre-commit-config.yaml

General extra lines:

```toml
[pre_commit]
extra_lines = """
-   repo: https://github.com/my/hook
    rev: v1.0
    hooks:
    -   id: my-hook
"""
```

Tool-specific extensions:

```toml
[pre_commit]
zpretty_extra_lines = """
        args: ['--indent', '4']
"""

codespell_extra_lines = """
        args: ['--skip', '*.po']
"""

flake8_extra_lines = """
        additional_dependencies:
          - flake8-debugger
          - flake8-deprecated
"""

i18ndude_extra_lines = """
        additional_dependencies:
          - toml
"""
```

To disable the i18ndude check:

```toml
[pre_commit]
i18ndude_extra_lines = """
        pass_filenames: false
"""
```

## pyproject.toml

General extra lines:

```toml
[pyproject]
extra_lines = """
[tool.mypy]
ignore_missing_imports = true
"""
```

Specific tool configuration:

```toml
[pyproject]
codespell_ignores = "foo,bar"
codespell_skip = "*.po,*.map,package-lock.json"

dependencies_ignores = "['zestreleaser.towncrier']"
dependencies_mappings = [
  "gitpython = ['git']",
  "pygithub = ['github']",
]

check_manifest_ignores = """
    "*.map.js",
    "*.pyc",
"""

black_extra_lines = """
target-version = ["py312"]
"""

isort_extra_lines = """
known_third_party = ["plone"]
"""
```

### Towncrier configuration

If your project has a {file}`news/` folder, towncrier configuration is generated automatically.

Custom issue format:

```toml
[pyproject]
towncrier_issue_format = "[#{issue}](https://github.com/myorg/myrepo/issues/{issue})"
```

Extra towncrier configuration:

```toml
[pyproject]
towncrier_extra_lines = """
[[tool.towncrier.type]]
directory = "deprecation"
name = "Deprecations"
showcontent = true
"""
```

## tox.ini

Test runner selection:

```toml
[tox]
test_runner = "pytest"
# or leave unset for zope.testrunner (default)
```

Test path:

```toml
[tox]
test_path = "src"
```

Additional tox environments:

```toml
[tox]
envlist_lines = """
    my_custom_env
"""
```

Extra test dependencies:

```toml
[tox]
test_extras = """
    tests
    widgets
"""
```

Custom constraints files (per Plone version):

```
[tox]
constraints_files = {
    "6.1" = "https://dist.plone.org/release/6.1-latest/constraints.txt",
    "6.0" = "https://dist.plone.org/release/6.0-latest/constraints.txt",
}
```

Test matrix configuration:

```
[tox]
use_test_matrix = true
test_matrix = {
    "6.2" = ["3.14", "3.13", "3.12", "3.11", "3.10"],
    "6.1" = ["3.13", "3.12", "3.11", "3.10"],
    "6.0" = ["3.13", "3.12", "3.11", "3.10"],
}
```

Set `use_test_matrix = false` to disable the matrix and use a single test environment.

Skip the test extra (for packages that do not define a `test` extra):

```toml
[tox]
skip_test_extra = true
```

Test environment variables:

```toml
[tox]
test_environment_variables = """
    PIP_EXTRA_INDEX_URL=https://my-pypi.example.com/
"""
```

mxdev support for source checkouts:

```toml
[tox]
use_mxdev = true
test_deps_additional = """
    -esources/my.package[test]
"""
```

General extra lines:

```toml
[tox]
extra_lines = """
[testenv:custom]
commands = python -c "print('hello')"
"""
```

Top-level tox configuration:

```toml
[tox]
config_lines = """
my_extra_config = value
"""
```

Override default testenv options:

```toml
[tox]
testenv_options = """
basepython = /usr/bin/python3.11
"""
```
