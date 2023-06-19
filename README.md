# meta

This repository's aim is to define and standarize a common set
of configuration files across Plone related repositories.

By using these files, you can have the same developer experience (DX)
across all Plone related packages.
which benefits seasoned contributors and newcomers alike.

The idea is to make it mandatory for repositories under the [GitHub Plone organization](https://github.com/plone),
while encouraging its adoption for the repositories under the [collective Plone organization](https://github.com/collective)
and even your own private packages for your customers.

With this configurations set in place,
any developer has the answer to the following questions at their fingertips:

- do the tests of this package pass?
- what's the coverage of the test suite?
- is the package ready to be released?
- are all dependencies clearly defined?
- how the dependencies graph looks like?
- are there any circular dependency problems?
- is the code formatted upon some agreed standards?
- are all agreed upon quality tools passing?

__How to find the answers?__ With the following commands:

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
# check if there are cyclic dependencies
tox -e circular
# format the code
tox -e format
# run all sorts of QA tools (code smells, typo finder...)
tox -e lint
```

## Tox

As seen above, [`tox`](https://pypi.org/project/tox) is the tool to find all these answers.

Tooling is like fashion, it keeps evolving and changing.

The great power behind `plone/meta` is that as soon as we find a better solution/tool,
we can swiftly move all packages to a new approach and making it as painless as possible!

## Configure a package

How to get the above answers to any package?
By using the `config-package.py` script found in this repositories' `config` folder.

See the [README](config/README.md) documentation for the details.
