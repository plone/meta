# meta

This repository's aim is to define and standarize a common set
of configuration files across Plone related repositories.

By using these files, you can have the same developer experience (DX)
across all Plone related packages.

The idea is to make it mandatory for repositories under the [GitHub Plone organization](https://github.com/plone),
while encouraging its adoption for the repositories under the [collective Plone organization](https://github.com/collective)
and even your own private packages for your customers.

With this configuration in place,
any developer has the answer to the following questions at their fingertips:

- Do the tests of this package pass?
- What's the coverage of the test suite?
- Is the package ready to be released?
- Are all dependencies clearly defined?
- What does the dependency graph look like?
- Are there any circular dependency problems?
- Is the code formatted to some agreed upon standards?
- Do all agreed upon code quality checks pass?

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

## Tox

As seen above, [`tox`](https://pypi.org/project/tox) provides the answers.

Tooling is like fashion, it keeps evolving and changing.

The great power behind `plone/meta` is that when we implement a better solution or tool,
we can swiftly move all packages to the new approach, making it as painless as possible!

## Configure a package

To get the above answers to any package, use the `config-package.py` script found in this repository's `config` folder.

See the [README](config/README.md) documentation for the details.
