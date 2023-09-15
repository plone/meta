# Configure a package

The `config-package.py` is the script that configures a given repository
to follow the standards agreed upon by the Plone community.

## Quick start

To configure a repository run the following commands:

```shell
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python config-package.py PATH/TO/PACKAGE
```

That's it. :-)

Now, you can use the `tox` commands
to adapt the repository just configured!

## Configuration files

In a nutshell `plone/meta`, puts some configuration files on the repository.

Currently the files managed by `plone/meta` are the following.

- `.meta.toml`: `plone/meta`'s configuration file
- `.editorconfig`: configuration meant to be read by code editors
- `.flake8`: [`flake8`](https://pypi.org/project/flake8) configuration
- `.gitignore`: list of file/folders patterns that `git` should ignore
- `.github/workflows/meta.yml`: GitHub Actions to run the testing and QA tools on GitHub (if the repository is hosted in GitHub.com)
- `.gitlab-ci.yml`: GitLab CI configuration (if the repository is hosted in GitLab.com)
- `.pre-commit-config.yaml`: [`pre-commit`](https://pypi.org/project/pre-commit) configuration
- `pyproject.toml`: configuration options for a wide variety of Python tooling
- `tox.ini`: [`tox`](https://pypi.org/project/tox) configuration, __the most important file__

You can find the _template_ files for each of these files
in the `config/default` folder of this `plone/meta` repository.

You will notice that they have a `.jinja` extension.
That's because the files are not merely copied over to the target repository,
but rather they are enhanced and adapted on the way there.

See the next section about how to extend and modify these configuration files.

## Configuration options

It is one thing to standardize, yet another to be flexible enough to adapt to each repository's particular needs.

Fortunately `plone/meta` tries its best to accomplish both:

- it provides sane defaults
- it allows extension of the defaults with custom configuration

The files mentioned above have comments all over them
with instructions on how to extend, modify, and influence
what `plone/meta` ends up adding on those files.

Those options are to be stored,
as it is mentioned on the comments themselves,
in `.meta.toml`.

This way, when the configuration files get regenerated,
`plone/meta` reads the configuration in `.meta.toml`
and reapplies the specific configuration on the other files.

See the specific configuration files sections below on how to extend and modify each configuration file.

### Configuration philosophy

The idea behind the configuration system
in `plone/meta` controlled configuration files is to make it as simple as possible.

Rather than adding plenty of configuration options,
almost all configuration files have an `extra_lines` section
that allows you to paste as much configuration as you want there.

In this way, it provides a simple, yet powerful, extension mechanism.

There are a few, and growing, other configuration options in a few files,
where the simple approach described above is not enough.

### More configuration options

Please use the [issue tracker](https://github.com/plone/meta/issues/new)
to ask for more extension points whenever `plone/meta`
does not fulfill all your needs.

### `.editorconfig`

Add the `[editorconfig]` TOML table in `.meta.toml`,
and set extra configuration for `editorconfig` under the `extra_lines` key.

```toml
[editorconfig]
extra_lines = """
_your own configuration lines_
"""
```

### `.flake8`

Add the `[flake8]` TOML table in `.meta.toml`,
and set the extra configuration for `flake8` under the `extra_lines` key.

```toml
[flake8]
extra_lines = """
_your own configuration lines_
"""
```

### `.gitignore`

Add the `[gitignore]` TOML table in `.meta.toml`,
and set the extra configuration for `git` under the `extra_lines` key.

```toml
[gitignore]
extra_lines = """
_your own configuration lines_
"""
```

### `.github/workflows/meta.yml`

Add the `[github]` TOML table in `.meta.toml`,
and set the enabled jobs with the `jobs` key.

```toml
[github]
jobs = [
    "qa",
    "test",
    "coverage",
    "dependencies",
    "release_ready",
    "circular",
    ]
```

It is possible to configure from which branch/tag of `plone/meta`
to get the workflow files by setting the value of the `ref` key:

```toml
[github]
ref = "master"
```

In the previous example, all GitHub workflows would come from
the `master` branch, instead of the default `main` branch.

To set environment variables to be used by all jobs,
specify the following key:

```toml
[github]
env = """
  debug: 1
  image-name: 'org/image'
  image-tag: 'latest'
"""
```

To install specific OS level dependencies,
note that they have to be Ubuntu package names, specify the following key:

```toml
[github]
os_dependencies = "git libxml2"
```

Extend github workflow configuration with additional jobs
by setting the values for the `extra_lines` key.

```toml
[github]
extra_lines = """
  another:
    uses: org/repo/.github/workflows/file.yml@main
"""
```

### `.gitlab-ci.yml`

Add the `[gitlab]` TOML table in `.meta.toml`,
and set the extra configuration for GitLab CI under the `extra_lines` key.

```toml
[gitlab]
extra_lines = """
_your own configuration lines_
"""
```

Specify a custom docker image if the default does not fit your needs on the `custom_image` key.

```toml
[gitlab]
custom_image = "python:3.11-bullseye"
```

To install test/coverage specific dependencies, add the following:

```toml
[gitlab]
os_dependencies = """
    - apt-get install libxslt libxml2
"""
```

You can customize the enabled gitlab jobs with the `jobs` key:

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

### `.pre-commit-config.yaml`

Add the `[pre_commit]` TOML table in `.meta.toml`,
and set the extra configuration for `pre-commit` under the `extra_lines` key.

```toml
[pre_commit]
extra_lines = """
_your own configuration lines_
"""
```

Extend [`zpretty`](https://pypi.org/project/zpretty) configuration
by setting the values on the `zpretty_extra_lines` key.

```toml
[pre_commit]
zpretty_extra_lines = """
_your own configuration lines_
"""
```

Extend [`codespell`](https://pypi.org/project/codespell) configuration
by setting the values on the `codespell_extra_lines` key.

```toml
[pre_commit]
codespell_extra_lines = """
_your own configuration lines_
"""
```

Extend [`flake8`](https://pypi.org/project/flake8) configuration
by setting the values on the `flake8_extra_lines` key.

Like to add extra plugins:

```toml
[pre_commit]
flake8_extra_lines = """
        additional_dependencies:
          - flake8-debugger
          - flake8-deprecated
"""
```

Extend [`i18ndude`](https://pypi.org/project/i18ndude) configuration
by setting the values on the `i18ndude_extra_lines` key.

Like to add extra plugins:

```toml
[pre_commit]
i18ndude_extra_lines = """
        additional_dependencies:
          - toml
"""
```

### `pyproject.toml`

`towncrier` configuration: depending on the extension of your `CHANGES` file,
`plone/meta` will adapt the configuration for `towncrier`.

It's automatic, you don't need to do anything!

Add the `[pyproject]` TOML table in `.meta.toml`,
and set extra configuration for any extra tool that you use
for the `extra_lines` key.

```toml
[pyproject]
extra_lines = """
_your own configuration lines_
"""
```

Extend [`codespell`](https://pypi.org/project/codespell) configuration
by setting the values for the `codespell_ignores` and `codespell_skip` keys.

```toml
[pyproject]
codespell_ignores = "foo,bar"
codespell_skip = "*.po,*.map,package-lock.json"
```

Extend [`z3c.dependencychecker`](https://pypi.org/project/z3c.dependencychecker) configuration
by setting the values for the `dependencies_ignores` and `dependencies_mappings` keys.

```toml
[pyproject]
dependencies_ignores = "['zestreleaser.towncrier']"
dependencies_mappings = [
  "gitpython = ['git']",
  "pygithub = ['github']",
]
```

Extend [`check-manifest`](https://pypi.org/project/check-manifest) configuration
by setting the values for the `check_manifest_ignores` key.

```toml
[pyproject]
check_manifest_ignores = """
    "*.map.js",
    "*.pyc",
"""
```

Configure [`towncrier`](https://pypi.org/project/towncrier) [`issue_format`](https://towncrier.readthedocs.io/en/stable/configuration.html) by setting the new format in the `towncrier_issue_format` key.

```toml
[pyproject]
towncrier_issue_format = "[#{issue}](https://github.com/plonegovbr/plonegovbr.portal/issues/{issue})"
```

Extend [`towncrier`](https://pypi.org/project/towncrier) configuration
by setting the values for the `towncrier_extra_lines` key.

```toml
[pyproject]
towncrier_extra_lines = """
_custom configuration_
"""
```

Extend [`black`](https://pypi.org/project/black) configuration
by setting the values for the `black_extra_lines` key.

```toml
[pyproject]
black_extra_lines = """
_custom configuration_
"""
```

Extend [`isort`](https://pypi.org/project/isort) configuration
by setting the values for the `isort_extra_lines` key.

```toml
[pyproject]
isort_extra_lines = """
_custom configuration_
"""
```

### `tox.ini`

Depending on the test runner that you want to use,
`plone/meta` will adapt `tox.ini` to it.

In the `[tox]` TOML table in `.meta.toml`, set the value for the key `test_runner` to `pytest` if you want to use [`pytest`](https://pypi.org/project/pytest).
By default, it falls back to use [`zope.testrunner`]((https://pypi.org/project/zope.testrunner)).

Likewise, the root path where the tests are to be found can be specified
under the key `test_path`. By default, it is set to nothing,
that is, the repository's top level is already importable
and thus the tests can be found directly.

If either a `tests` or `src` folder exists, then they are used as a safe fallbacks.

Add the `[tox]` TOML table in `.meta.toml`,
and set the extra configuration for `tox` under the `extra_lines` key.

```toml
[tox]
extra_lines = """
_your own configuration lines_
"""
```

Extend the list of default `tox` environments by using the `envlist_lines` key.

Add extra top level configuration for `tox` by using the `config_lines` key.

```toml
[tox]
envlist_lines = """
    my_other_environment
"""
config_lines = """
my_extra_top_level_tox_configuration_lines
"""
```

Extend the list of `extras` that need to be installed to run the test suite
and generate the coverage report by setting them on the `test_extras` key.

```toml
[tox]
test_extras = """
    tests
    widgets
"""
```

If your package uses [`mxdev`](https://pypi.org/project/mxdev/) to handle source checkouts for dependencies, you can set the `use_mxdev` key to ensure `tox` will first run mxdev.

You also will need to manually set the installation of additional packages being pulled by `mxdev` in the `test_deps_additional` key.

```toml
[tox]
use_mxdev = true
test_deps_additional = """
    -esources/plonegovbr.portal_base[test]
"""
```

When using `plone/meta` outside of plone core packages
there might be extra version pins, or overrides over the official versions.
To specify a custom constraints file, use the `constraints_file` key.

Generating a custom constraints.txt is out of scope for `plone/meta` itself,
there are plenty of tools that can do that though.

```toml
[tox]
constraints_file = "https://my-server.com/constraints.txt"
```

Extend the list of custom environment variables
that the test and coverage environments can get by using the `test_environment_variables` key.

```toml
[tox]
test_environment_variables = """
    PIP_EXTRA_INDEX_URL=https://my-pypi.my-server.com/
"""
```

## Detailed script usage

As said above, the `config-package.py` script is the tool to apply the configuration.

See its `--help` for the up-to-date possible options.

### CLI arguments

The following arguments are supported.

`--commit-msg=MSG`: use `MSG` as commit message instead of the default one

`--no-commit`: don't automatically commit changes after the configuration run

`--push`: push changes at the end of the configuration run.
By default, the changes are __not__ pushed

`--branch`: define a specific git branch name to be created for the changes.
By default, the script creates one which includes the name of the configuration type.
__Tip:__ Use `current` to update the current branch.

`--tox`: whether to run `tox` on the repository. By default it is not run.

`--no-track`: whether the package being configured should _not_ be added on `defaults/packages.txt`. By default, packages' names are added to it.

The following options are only needed one time
as their values are stored in `.meta.toml.`.

`--type`: define the configuration type. At this time, `default` is the only option.

## Other scripts

### Calling a script on multiple repositories

The `config-package.py` script only runs on a single repository.
To update multiple repositories at once, you can use `multi-call.py`.
It runs a given script on all repositories listed in a `packages.txt` file.

#### Usage

To run a script on all packages listed in a `packages.txt` file, call
`multi-call.py` as follows.

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

Running this script stashes any uncommitted changes in the repositories.
Run `git stash pop` to recover them.

### Re-enabling GitHub Actions

After a certain period of time (currently 60 days) without commits, GitHub
automatically disables Actions. They can be re-enabled manually per repository.
There is a script to do this for all repositories. It does no harm if Actions
is already enabled for a repository.

#### Preparation

- Install GitHub's CLI application, see https://github.com/cli/cli.
- Authorize using the application:
  - `gh auth login`
  - It is probably enough to do it once.

#### Usage

To run the script just call it:

```shell
bin/python re-enable-actions.py
```

### Dropping support for legacy Python versions

To drop support for Python 2.7 up to 3.6, several steps have to be done as
documented at https://zope.dev/developer/python2.html#how-to-drop-support.
There is a script to ease this process.

#### Preparation

- The package from which to remove legacy Python support has to have a `.meta.toml`
  file, in other words, it must be under control of the `config-package.py` script.

#### Usage

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
