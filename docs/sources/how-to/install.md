# Install plone.meta

<!-- diataxis: how-to -->

## From source (recommended)

Clone the repository and install in a virtual environment:

```shell
git clone https://github.com/plone/meta.git
cd meta
python3 -m venv venv
venv/bin/pip install -e .
```

The commands `config-package`, `multi-call`, and `re-enable-actions` are now
available under `venv/bin/`.

## From PyPI

```shell
pip install plone.meta
```

## Verify the installation

```shell
venv/bin/config-package --help
```

You should see the help output listing all available options.
