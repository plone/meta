# Install plone.meta

<!-- diataxis: how-to -->

## From PyPI (recommended)

Install plone.meta from PyPI into a virtual environment:

```shell
python3 -m venv venv
venv/bin/pip install plone.meta
```

The commands `config-package`, `multi-call`, `switch-to-pep420`, and
`re-enable-actions` are now available under `venv/bin/`.

## From source

Clone the repository and install in editable mode:

```shell
git clone https://github.com/plone/meta.git
cd meta
python3 -m venv venv
venv/bin/pip install -e .
```

This is useful for contributing to plone.meta or testing unreleased changes.

## Verify the installation

```shell
venv/bin/config-package --help
```

You should see the help output listing all available options.
