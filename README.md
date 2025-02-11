> [!TIP]
> Since February 11th 2025 `plone.meta` is not using `main` branch for development anymore,
> have a look at the current default branch on GitHub UI.

# plone/meta

`plone/meta` defines and standardizes a common set of configuration files across Plone related Python repositories.
It does not cover the following.

-   Volto or any other JavaScript-based project, which has its own ecosystem.
-   Monorepo projects with backend and frontend code bases, such as those created by [Cookieplone](https://github.com/plone/cookieplone).
    Repositories must have a single Python package at the top level.
-   Projects that support multiple versions of Plone in the same branch.


## Setup

Clone `plone/meta` to any machine, then change your current working directory into `meta/config`, create a Python virtual environment, and install `plone/meta`'s requirements.

```shell
git clone https://github.com/plone/meta.git
cd meta
python3 -m venv venv
venv/bin/pip install -e .
```


## `config-package` usage

The command `config-package` from `plone/meta` creates or overwrites configuration files for your project.
See a current list of [configuration files](#configuration-files) that it will create or overwrite.

This command has several [command line options](#cli-arguments) that you can use to override the default options.

When you run this command, it automatically goes through the following steps.

1.  It creates a new git branch from the current branch in your project.
1.  If the file {file}`.meta.toml` is not present in the project, then it creates this and the other new configuration files from `plone/meta`'s Jinja2 templates.
    Otherwise, it reads the file {file}`.meta.toml` for regenerating the configuration files.
1.  It writes the configuration files.
1.  It creates a change log entry.
1.  By default, it commits changes.
1.  It optionally adds packages, pushes commits, or runs tox from the configuration files. 

> [!TIP]
> If you prefer to name the new git branch instead of letting the command name it using its default naming scheme, then either create a new branch `my-new-branch`, switch to it, and use the `--branch current` option, or do all that in one step with the `--branch my-new-branch` option.

> [!TIP]
> If you prefer to review changes before committing them, then use the `--no-commit` option.

For help for `config-package`, use the following command.

```shell
venv/bin/config-package --help
```

You can request more extension points if `plone/meta` does not fulfill your needs in the [issue tracker](https://github.com/plone/meta/issues/new).


### Generate configuration files

Now you can run the command `config-package` to generate configuration files from Jinja2 template files to manage your project.

```shell
venv/bin/config-package [OPTIONS] PATH/TO/PACKAGE
```


### Manage configuration files

For each of the configuration files, you should edit its [corresponding stanza](#applying-a-customized-configuration) in the file `.meta.toml`.

> [!WARNING]
> Do not directly edit the configuration files that `plone/meta` manages.
Anytime someone runs the command `config-package`, any changes made in these files will get clobbered.

Commit your changes, then run the command `config-package` to regenerate configuration files from your project's `.meta.toml`.

```shell
venv/bin/config-package [OPTIONS] PATH/TO/PACKAGE
```


### `config-package` command line options

`config-package` supports the following command line options.

-   `--branch BRANCH_NAME`: Define a specific git branch name to create for the changes.
    By default, the script creates one, which includes the name of the configuration type.
    > [!TIP]
    > Use `current` to update the current branch.
-   `--commit-msg MSG`: Use `MSG` as the commit message instead of the default one.
-   `--no-commit`: Don't automatically commit changes after the configuration run.
-   `-h, --help`: Display help.
-   `--push`: Push changes at the end of the configuration run.
    By default, the changes are _not_ pushed.
-   `--tox`: Whether to run `tox` on the repository.
    By default, it does not run.
-   `--track`: Whether the package being configured should be added to `defaults/packages.txt`.
    By default, they are _not_ added.
-   `-t, --type`: define the configuration type.
    At this time, `default` is the only option.
    This option is only needed one time as their values are stored in `.meta.toml`.


### `config-package` configuration files

`plone.meta` generates configuration files in your local repository.
Currently, the files that `plone.meta` manages are the following.

-   `.meta.toml`: `plone.meta`'s configuration file
-   `.editorconfig`: configuration meant to be read by code editors
-   `.flake8`: [`flake8`](https://pypi.org/project/flake8) configuration
-   `.gitignore`: list of file/folders patterns that `git` should ignore
-   `.github/workflows/meta.yml`: GitHub workflows to run the testing and code quality and analysis tools on GitHub, provided the repository is hosted at github.com
-   `.gitlab-ci.yml`: GitLab CI configuration, provided the repository is hosted at gitlab.com
-   `.pre-commit-config.yaml`: [`pre-commit`](https://pypi.org/project/pre-commit) configuration
-   `pyproject.toml`: configuration options for a wide variety of Python tooling
-   `tox.ini`: [`tox`](https://pypi.org/project/tox) configuration, _the most important file_

You can find the _template_ files for each of these files in the `config/default` folder of this `plone.meta` repository.

You will notice that they have a `.jinja` extension.
That's because the files are not merely copied over to the target repository, but rather they are enhanced and adapted on the way to their destination.

The following sections describe how to configure each of the configuration files.


#### `.editorconfig`

Add the `[editorconfig]` TOML table in `.meta.toml`, and set extra configuration for `editorconfig` under the `extra_lines` key.

```toml
[editorconfig]
extra_lines = """
_your own configuration lines_
"""
```

If you want to set the indentation to four spaces for frontend related files, add the following to your `.meta.toml`.

```toml
[editorconfig]
extra_lines = """
[*.{json,jsonl,js,jsx,ts,tsx,css,less,scss}]
indent_size = 4
"""
```


#### `.flake8`

Add the `[flake8]` TOML table in `.meta.toml`, and set the extra configuration for `flake8` under the `extra_lines` key.

```toml
[flake8]
extra_lines = """
_your own configuration lines_
"""
```


#### `.gitignore`

Add the `[gitignore]` TOML table in `.meta.toml`, and set the extra configuration for `git` under the `extra_lines` key.

```toml
[gitignore]
extra_lines = """
_your own configuration lines_
"""
```


#### `.github/workflows/meta.yml`

> [!NOTE]
> The variables `TEST_OS_VERSIONS` and `TEST_PYTHON_VERSIONS` variables need to exist, either at the GitHub organization level, or at the repository level.

See the [GitHub documentation about variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables).

These variables are expected to be lists.

-   `TEST_OS_VERSIONS`: `["ubuntu-latest",]`
    -   a list of valid operating system names according [to GitHub Actions](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources)
-   `TEST_PYTHON_VERSIONS`: `["3.13", "3.12", "3.11", "3.10", ]`
    -   a list of valid Python versions according to [python-versions action](https://github.com/actions/python-versions/)

Add the `[github]` TOML table in `.meta.toml`, and set the enabled jobs with the `jobs` key.

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

It is possible to configure from which branch or tag of `plone/meta` to get the workflow files by setting the value of the `ref` key.
In the following example, all GitHub workflows would come from the `v3` tag, instead of the default `main` branch.

```toml
[github]
ref = "v3"
```

To set environment variables for all jobs, specify the `env` key as follows.

```toml
[github]
env = """
  debug: 1
  image-name: 'org/image'
  image-tag: 'latest'
"""
```

To install specific operating system level dependencies, which must be Ubuntu package names, specify the following key.

```toml
[github]
os_dependencies = "git libxml2"
```

To run tests against specific Python versions, specify the `py_versions` key as follows.

> [!NOTE]
> The GitHub Action expects a string to be parsed as a JSON array.
> Unfortunately, quotes need to be escaped.

```toml
[github]
py_versions = "[\"3.11\", \"3.10\"]"
```

Extend GitHub workflow configuration with additional jobs by setting the values for the `extra_lines` key.

```toml
[github]
extra_lines = """
  another:
    uses: org/repo/.github/workflows/file.yml@main
"""
```


#### `.gitlab-ci.yml`

Add the `[gitlab]` TOML table in `.meta.toml`, and set the extra configuration for GitLab CI under the `extra_lines` key.

```toml
[gitlab]
extra_lines = """
_your own configuration lines_
"""
```

Specify a custom Docker image, if the default does not fit your needs, in the `custom_image` key.

```toml
[gitlab]
custom_image = "python:3.11-bullseye"
```

To install specific test and coverage dependencies, add the `os_dependencies` key as follows.

```toml
[gitlab]
os_dependencies = """
    - apt-get install libxslt libxml2
"""
```

You can customize the enabled GitLab jobs with the `jobs` key.

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


#### `.pre-commit-config.yaml`

Add the `[pre_commit]` TOML table in `.meta.toml`, and set the extra configuration for `pre-commit` under the `extra_lines` key.

```toml
[pre_commit]
extra_lines = """
_your own configuration lines_
"""
```

Extend [`zpretty`](https://pypi.org/project/zpretty) configuration by setting the values for the `zpretty_extra_lines` key.

```toml
[pre_commit]
zpretty_extra_lines = """
_your own configuration lines_
"""
```

Extend [codespell](https://pypi.org/project/codespell) configuration by setting the values for the `codespell_extra_lines` key.

```toml
[pre_commit]
codespell_extra_lines = """
_your own configuration lines_
"""
```

Extend [Flake8](https://pypi.org/project/flake8) configuration by setting the values for the `flake8_extra_lines` key.
For example, to add extra Flake8 plugins, you would specify `additional_dependencies` as shown.

```toml
[pre_commit]
flake8_extra_lines = """
        additional_dependencies:
          - flake8-debugger
          - flake8-deprecated
"""
```

Extend [i18ndude](https://pypi.org/project/i18ndude) configuration by setting the values for the `i18ndude_extra_lines` key.
For example, to add extra i18ndude plugins, you would specify `additional_dependencies` as shown.

```toml
[pre_commit]
i18ndude_extra_lines = """
        additional_dependencies:
          - toml
"""
```

If you want to disable the i18ndude check, add the following pre-commit configuration option to your `.meta.toml` file.

```toml
[pre_commit]
i18ndude_extra_lines = """
        pass_filenames: false
"""
```


#### `pyproject.toml`

Add the `[pyproject]` TOML table in `.meta.toml`, and set configuration for any extra tool that you use for the `extra_lines` key.

```toml
[pyproject]
extra_lines = """
_your own configuration lines_
"""
```

Extend [codespell](https://pypi.org/project/codespell) configuration by setting the values for the `codespell_ignores` and `codespell_skip` keys.

```toml
[pyproject]
codespell_ignores = "foo,bar"
codespell_skip = "*.po,*.map,package-lock.json"
```

Extend [z3c.dependencychecker](https://pypi.org/project/z3c.dependencychecker) configuration by setting the values for the `dependencies_ignores` and `dependencies_mappings` keys.

```toml
[pyproject]
dependencies_ignores = "['zestreleaser.towncrier']"
dependencies_mappings = [
  "gitpython = ['git']",
  "pygithub = ['github']",
]
```

Extend [check-manifest](https://pypi.org/project/check-manifest) configuration by setting the values for the `check_manifest_ignores` key.

```toml
[pyproject]
check_manifest_ignores = """
    "*.map.js",
    "*.pyc",
"""
```

Extend [Black](https://pypi.org/project/black) configuration by setting the values for the `black_extra_lines` key.

```toml
[pyproject]
black_extra_lines = """
_custom configuration_
"""
```

Extend [isort](https://pypi.org/project/isort) configuration by setting the values for the `isort_extra_lines` key.

```toml
[pyproject]
isort_extra_lines = """
_custom configuration_
"""
```


##### `towncrier` configuration

If your project contains a `news/` folder, `plone.meta` will add the configuration for `towncrier`.

If your `CHANGES` file has the extension `.md`, a `changelog_template.jinja` template will be generated inside the `news/` folder.

Configure [`towncrier`](https://pypi.org/project/towncrier) [`issue_format`](https://towncrier.readthedocs.io/en/stable/configuration.html) by setting the new format in the `towncrier_issue_format` key.

```toml
[pyproject]
towncrier_issue_format = "[#{issue}](https://github.com/plonegovbr/plonegovbr.portal/issues/{issue})"
```

Extend [`towncrier`](https://pypi.org/project/towncrier) configuration by setting the values for the `towncrier_extra_lines` key.

```toml
[pyproject]
towncrier_extra_lines = """
_custom configuration_
"""
```


#### `tox.ini`

Depending on the test runner that you want to use, `plone.meta` will adapt `tox.ini` to it.

In the `[tox]` TOML table in `.meta.toml`, set the value for the key `test_runner` to `pytest` if you want to use [`pytest`](https://pypi.org/project/pytest).
By default, it falls back to use [zope.testrunner](https://pypi.org/project/zope.testrunner).

Likewise, the root path where the tests are to be found can be specified under the key `test_path`.
By default, it is set to nothing, that is, the repository's top level is already importable and thus the tests can be found directly.

If either a `tests` or `src` folder exists, then they are used as safe fallbacks.

Add the `[tox]` TOML table in `.meta.toml`, and set the extra configuration for `tox` under the `extra_lines` key.

```toml
[tox]
extra_lines = """
_your own configuration lines_
"""
```

Extend the list of default `tox` environments in the `envlist_lines` key.
Add extra top level configuration for `tox` in the `config_lines` key.

```toml
[tox]
envlist_lines = """
    my_other_environment
"""
config_lines = """
my_extra_top_level_tox_configuration_lines
"""
```

Customize the default values for all `tox` environments in the `testenv_options` key.

```toml
[tox]
testenv_options = """
basepython = /usr/bin/python3.8
"""
```

Extend the list of `extras` that need to be installed for running the test suite and generate the coverage report by setting them on the `test_extras` key.

```toml
[tox]
test_extras = """
    tests
    widgets
"""
```

If your package uses [mxdev](https://pypi.org/project/mxdev/) to handle source checkouts for dependencies, you can set the `use_mxdev` key to ensure `tox` will first run mxdev.
You also need to manually set the installation of additional packages that `mxdev` pulls in with the `test_deps_additional` key.

```toml
[tox]
use_mxdev = true
test_deps_additional = """
    -esources/plonegovbr.portal_base[test]
"""
```

When using `plone.meta` outside of plone core packages, there might be extra version pins, or overrides over the official versions.
To specify a custom constraints file, use the `constraints_file` key.

Generating a custom `constraints.txt` is out of scope for `plone.meta` itself.
There are plenty of tools that can do that though.

```toml
[tox]
constraints_file = "https://my-server.com/constraints.txt"
```

Extend the list of custom environment variables that the test and coverage environments can get in the `test_environment_variables` key.

```toml
[tox]
test_environment_variables = """
    PIP_EXTRA_INDEX_URL=https://my-pypi.my-server.com/
"""
```

For packages that have `plone.app.robotframework` based tests, it automatically detects it and primes [Playwright](https://playwright.dev/) to install the needed browsers.



### Manage multiple repositories with `multi-call`

The `config-package` command runs only on a single repository.
To update multiple repositories at once, you can use the command `multi-call`.
It runs on all repositories listed in a `packages.txt` file.

To run `multi-call` on all packages listed in a `packages.txt` file use the following command with positional arguments as shown.

-   The file path the Python script to be called.
-   The file path to `packages.txt`, which lists repositories of packages on which the Python script will be called.
-   The file path to the directory where the clones of the repositories are stored.
-   Arguments to pass into the Python script.

```shell
bin/multi-call <name-of-the-script.py> <path-to-packages.txt> <path-to-clones> <arguments-for-script>
```

The script performs the following steps for each line in the given `packages.txt` that does not start with a hash mark (`#`).

1.  Check if there is a repository in `<path-to-clones>` with the name of the repository.
    If it does not exist, then clone it.
    If it exists, then clean the clone from changes, switch to the `master` branch, and pull from the origin.
2.  Call the given script with the package name and arguments for the script.

> [!CAUTION]
> Running this script stashes any uncommitted changes in the repositories.
> Run `git stash pop` to recover them.



### Re-enable GitHub Actions with `re-enable-actions`

After a certain period of time without commits to a repository, GitHub automatically disables Actions.
You can re-enable them manually per repository.
`re-enable-actions` can do this for all repositories.
It does no harm if Actions are already enabled for a repository.


#### Setup GitHub CLI

-   Install [GitHub's CLI application](https://github.com/cli/cli).
-   Authorize using the application:
    -   `gh auth login`
    - It is probably enough to do it once.


#### `re-enable-actions` usage

Use the following command.

```shell
venv/bin/re-enable-actions
```


## Explanation

This section provides explanation of design decisions and capabilities of `plone/meta`.


### Project management

By using `plone/meta`, you can have the same developer experience (DX)
across all Plone related packages.

The idea is to make it mandatory for repositories under the [GitHub Plone organization](https://github.com/plone),
while encouraging its adoption for the repositories under the [collective Plone organization](https://github.com/collective)
and even your own private packages for your customers.

With this configuration in place,
any developer has the answer to the following questions at their fingertips:

-   Do the tests of this package pass?
-   What's the coverage of the test suite?
-   Is the package ready to be released?
-   Are all dependencies clearly defined?
-   What does the dependency graph look like?
-   Are there any circular dependency problems?
-   Is the code formatted to some agreed upon standards?
-   Do all agreed upon code quality checks pass?

To find the answers to these questions, you can run the following commands.

```shell
# run the test suite
tox -e test
# get a coverage report
tox -e coverage
# check if the package is ready to be released
tox -e release-check
# check if the dependencies are all specified
tox -e dependencies
# generate a dependency graph
tox -e dependencies-graph
# check if there are circular dependencies
tox -e circular
# format the code
tox -e format
# run all sorts of QA tools (code smells, typo finder...)
tox -e lint
```

As seen above, [`tox`](https://pypi.org/project/tox) provides the answers.

Tooling is like fashion, it keeps evolving and changing.

The great power behind `plone.meta` is that when we implement a better solution or tool,
we can swiftly move all packages to the new approach, making it as painless as possible!


### Configuration philosophy

It is one thing to standardize, yet another to be flexible enough to adapt to each repository's particular needs.

Fortunately `plone.meta` tries its best to accomplish both:

- it provides sane defaults
- it allows extension of the defaults with custom configuration

The configuration files have comments all over them
with instructions on how to extend, modify, and influence
what `plone.meta` ends up adding on those files.

Those options are to be stored,
as it is mentioned on the comments themselves,
in `.meta.toml`.

This way, when the configuration files get regenerated,
`plone.meta` reads the configuration in `.meta.toml`
and reapplies the specific configuration on the other files.

See the specific configuration files sections below on how to extend and modify each configuration file.

The idea behind the configuration system
in `plone.meta` controlled configuration files is to make it as simple as possible.

Rather than adding plenty of configuration options,
almost all configuration files have an `extra_lines` section
that allows you to paste as much configuration as you want there.

In this way, it provides a simple, yet powerful, extension mechanism.

There are a few, and growing, other configuration options in a few files,
where the simple approach described above is not enough.

