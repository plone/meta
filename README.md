# meta

This repository's aim is to define common configuration files
across all/most repositories in the [GitHub plone organization](https://github.com/plone).

This allows Plone developers and contributors
to have the same expectations/workflow
when contributing to any of the Plone repositories.

The following areas are configured on repositories
where the configuration has been applied.

## Testing

A `tox.ini` configuration is added to each repository to allow contributors
to test their contributions, as well as running the tests on GitHub Actions.

To run the tests, run the following commands:

```shell
python3.11 -m venv venv
. venv/bin/activate
pip install tox
tox -e test
```

Note: the GitHub Actions workflow is __not__ installed on each repository,
but rather shared by all repositories.

The workflow definition can be found in this repository in `shared-workflows/tests.yml`.

To enable a repository, as an admin, go to the [Actions permissions](https://github.com/organizations/plone/settings/actions),
scroll all the way down, update the relevant workflow
and finally search the repository you just configured.

## Code analysis / formatting

On the `tox.ini` configuration there are two environments
to format and run quality check tools:

```shell
tox -e format
tox -e lint
```

Note: they are based on `pre-commit`.
Each repository needs to be enabled on [pre-commit.ci](https://pre-commit.ci/)
for the formatting/linting to run on each commit.

Note: although it is based on `pre-commit`
it does _not_ install its hooks by default.

## Dependencies

Another `tox` environment allows you to check
if the distribution defines all its dependencies on `setup.py`.

```shell
tox -e dependencies
```

Note: these `tox` environments are not run on GitHub Actions as of now.
