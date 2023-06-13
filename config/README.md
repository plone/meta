# Config

## Purpose

Bring the configuration of the Plone packages into a common state and keep it there.

## Contents

The `default` directory contains the following files:

- editorconfig
  - This file is copied to `.editorconfig` and allows developers to have a
    common editor configuration experience in all repos
- packages.txt
  - Lists the packages have been configured to use these set of configuration files
- pre-commit-config.yaml
  - Configuration for [pre-commit](https://pypi.org/project/pre-commit/)
- pyproject.toml.j2
  - Configuration for various python related tools
- setup.cfg.j2
  - Another typical configuration file for various python tools
- tox.ini.j2
  - [`tox`](https://pypi.org/project/tox/) configuration, which should be copied to the repository of the package

## Usage

### Preparation

The script needs a `venv` with some packages installed:

```shell
python3.11 -m venv .
bin/pip install -r requirements.txt
```

To use the configuration provided here in a package call the following script:

```shell
bin/python config-package.py <path-to-package> [<additional-options>]
```

See `--help` for details.

The script does the following steps:

1. Add the package name to `packages.txt`
2. Copies various files to the repository
3. Remove a possibly existing `.travis.yml` and `bootstrap.py`
4. Run all `tox` _targets_. The `tox` script may be either on the current
   `$PATH` or in the `bin` subfolder of the current working directory.
5. Create a branch and a few commits with all the changes

After running the script you should manually do the following steps:

1. Double check the changes and adapt the code to them
2. Add a news entry
3. Check in possible changes in the `plone/meta` repository itself

### CLI arguments

The following arguments are supported.

`--commit-msg=MSG`: use `MSG` as commit message instead of the default one

`--no-commit`: don't automatically commit changes after the configuration run

`--push`: push changes at the end of the configuration run.
By default, the changes are __not__ pushed

`--branch`: define a specific git branch name to be created for the changes.
By default, the script creates one which includes the name of the configuration type.
Use "current" to update the current branch.

The following options are only needed one time
as their values are stored in `.meta.toml.`.

`--type`: define the configuration type, by now `default` is the only option

### Options

There is almost no options to configure so far,
but that does not mean it has to be this way!

See [`zopefoundation/meta`](https://github.com/zopefoundation/meta)
for plenty of examples of options that can be added to the configuration files.

`.meta.toml` file is added inside the package repository.
This file stores the template name and commit id
of the _meta_ repository at the time of the run.
This file is generated during the configuration run,
if it does not exist or at least gets updated.

Example:

```ini
[meta]
template = "default"
commit-id = "< commit-hash >"

[test]
runner = "pytest"
path = "/tests"

[dependencies]
mappings = [
    "Zope = ['Products.Five', 'ZTUtils']",
    ]
ignores = "['plone.app.locales', 'plone.batching']"

[check-manifest]
additional-ignores = [
    ".tox",
    "lint-requirements.txt",
    ]

[codespell]
additional-ignores = "typo,wurd"
skip = "*.zcml"
```

#### Meta Options

`template`: Name of the configuration type, to be used as the template for the
  repository. Currently read-only.

`commit-id`: Commit of the meta repository, which was used for the last configuration run.
  Currently read-only.

#### Test Options

`runner`: Name of the test runner used by tox, by default we use `zope.testrunner`, but
`pytest` is also supported.

`path`: Base path to run tests. Default values are top-level `/tests` or `/src`.


#### Dependencies

Options to configure `z3c.dependencychecker`.

`ignores`: Text line of a list of packages that should be ignored.

`mappings`: List of text lines with mappings of imports and packages providing them.
  Note the, by default, there are already mappings for
  `Zope`, `Products.CMFCore` and `plone.base`.

#### Check-manifest

Options to configure `check-manifest`.

`additional-ignores`: List of text lines
  to be added on `check-manifest` configuration for files to be ignored.

#### Codespell

Options to configure `codespell`. See [its documentation](https://pypi.org/project/codespell/).

`additional-ignores`: List of words that should be ignored.

`skip`: List of file patterns to ignore, i.e. ignore translation files.

## Hints

Call `bin/check-python-versions <path-to-package> -h` to see
how to fix version mismatches in the *lint* tox environment.

## Calling a script on multiple repositories

The `config-package.py` script only runs on a single repository.
To update multiple repositories at once you can use `multi-call.py`.
It runs a given script on all repositories listed in a `packages.txt` file.

### Usage

To run a script on all packages listed in a `packages.txt` file call
`multi-call.py` the following way::

```shell
bin/python multi-call.py <name-of-the-script.py> <path-to-packages.txt> <path-to-clones> <arguments-for-script>
```

See `--help` for details.

The script does the following steps for each line in the given `packages.txt`
which does not start with `#`:

1. Check if there is a repository in `<path-to-clones>` with the name of the
   repository. If it does not exist: clone it. If it exists: clean the clone
   from changes, switch to `master` branch and pull from origin.
2. Call the given script with the package name and arguments for the script.

__CAUTION:__

Running this script stashes any uncommitted changes in the repositories,
run `git stash pop` to recover them.

## Re-enabling GitHub Actions

After a certain period of time (currently 60 days) without commits GitHub
automatically disables Actions. They can be re-enabled manually per repository.
There is a script to do this for all repositories. It does no harm if Actions
is already enabled for a repository.

### Preparation

- Install GitHub's CLI application, see https://github.com/cli/cli.
- Authorize using the application:
  - `gh auth login`
  - It is probably enough to do it once.

### Usage

To run the script just call it:

```shell
bin/python re-enable-actions.py
```

## Dropping support for legacy Python versions

To drop support for Python 2.7 up to 3.6 several steps have to be done as
documented at https://zope.dev/developer/python2.html#how-to-drop-support.
There is a script to ease this process.

### Preparation

- The package to remove legacy python support from has to have a `.meta.toml`
  file, aka it must be under control of the `config-package.py` script.

### Usage

To run the script call:

```shell
bin/python drop-legacy-python.py <path-to-package>
```

Additional optional parameters, see above at `config-package.py` for a
descriptions of them:

* `--branch`

You can call the script interactively by passing the argument
`--interactive`, this will let the various scripts prompt for information and
prevent automatic commits and pushes. That way all changes can be viewed before
committing them.
