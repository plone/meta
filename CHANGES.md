# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 2.0.0 (2025-02-11)


### New features

- Allow to configure extra options on `i18ndude`'s `pre-commit` configuration @Akshat2Jain [#133](https://github.com/plone/meta/issues/133)
- Install browsers (for playwright) on packages that run
  plone.app.robotframework tests @gforcada [#155](https://github.com/plone/meta/issues/155)
- Allow setting GHA environment variables @ericof [#164](https://github.com/plone/meta/issues/164)
- Implement conditional towncrier configuration depending on
  existing `news/` folder @petschki [#170](https://github.com/plone/meta/issues/170)
- Allow customizing enabled gitlab-ci jobs @petschki [#171](https://github.com/plone/meta/issues/171)
- In generated `pyproject.toml` files, add `build-system` requiring `setuptools` 68.2+.
  Also, build the package in isolation, so the build is free to use the required `setuptools` version.
  This combination fixes possible `ModuleNotFoundErrors` for `plone.app.*` packages @mauritsvanrees [#172](https://github.com/plone/meta/issues/172)
- Ignore `.*project` in git @wesleybl [#179](https://github.com/plone/meta/issues/179)
- `tox`: allow to configure what gets in `testenv` environment @gforcada [#185](https://github.com/plone/meta/issues/185)
- Configure `dependabot` to get GHA updates. @gforcada [#201](https://github.com/plone/meta/issues/201)
- GHA: Allow to run `tox -e test` with multiple python versions @gforcada [#210](https://github.com/plone/meta/issues/210)
- Made `pytest-plone` test dependency in `tox.ini` optional. Specify `use_pytest_plone =
  false` if you don't want to use it.
  Also added `check_manifest_extra_lines` for `pyproject.toml`, you can use it for
  specifying corner cases like `ignore-bad-ideas` @reinout [#212](https://github.com/plone/meta/issues/212)
- Use tomlkit for TOML read/write operations
  it allow custom regexes with backslahes in meta.toml
  it is a port of https://github.com/zopefoundation/meta/pull/215 [#229](https://github.com/plone/meta/issues/229)
- Turn this repository into a proper Python distribution. @gforcada [#239](https://github.com/plone/meta/issues/239)
- Make `plone.meta` an actual python distribution releasable in PyPI @gforcada [#248](https://github.com/plone/meta/issues/248)
- When creating a branch, use the git commit hash from meta repository @gforcada 


### Bug fixes

- Only run a GHA on Linux, while we wait for a counterpart for Windows @gforcada [#180](https://github.com/plone/meta/issues/180)
- Moved inline comments in .editorconfig to their own lines: the spec at
  https://spec.editorconfig.org/#no-inline-comments forbids it @reinout [#208](https://github.com/plone/meta/issues/208)
- Stop relying on GitHub repository/organization variables @gforcada [#210](https://github.com/plone/meta/issues/210)
- Preventing lines with only spaces in the generated tox.ini @reinout [#212](https://github.com/plone/meta/issues/212)
- On `.meta.toml` file installed by `plone.meta`, write `plone.meta`'s version on `commit-id` rather than a commit.
  We are no longer running `plone.meta` out of a checkout, but rather from a release version @gforcada [#248](https://github.com/plone/meta/issues/248)
- Fix `dependabot.yml` location @gforcada [#252](https://github.com/plone/meta/issues/252)
- Do not track packages on `packages.txt` by default @gforcada 
- Ensure that `prettier`'s default line length is respected @gforcada 
- Mark old `shared-workflows` GHA as deprecated @gforcada 


### Internal

- Add .gitignore @wesleybl [#178](https://github.com/plone/meta/issues/178)
- Editorconfig: Restructure the frontend config.

  - Add an xml type to the xml section.
  - Move the HTML type to the xml section.

  This allows more easily for frontend related files except HTML files to be
  reconfigured for an 4-space indentation. 4 spaces for JS/CSS related code is
  the default style in Patternslib/Mockup. style @thet [#197](https://github.com/plone/meta/issues/197)


### Documentation

- Add a note on how to disable i18ndude checks.
  Add a note on how to apply a customized configuration.
  @thet [#200](https://github.com/plone/meta/issues/200)

## 1.0.0 (2023-07-12)


### New features:

- Allow passing arguments to `tox -e test`.
  [@mauritsvanrees] #0
- Run robot tests as well (pass `--all` to `zope.testrunner`)
  [@mauritsvanrees] #0
- Generate XML coverage reports.
  [@gforcada] #0
- Handle repositories that do not have `towncrier` configured.
  [@petschki] #0
- Add `skip` option to `codespell`.
  [@petschki] #0
- Fix deletion of old files.
  [@mauritsvanrees] #0
- Use `pre-commit` to manage most of QA/linting tools.
  [@mauritsvanrees] #0
- Make `tox` fail if the environment is not defined.
  [@mauritsvanrees] #0
- Allow to install extra dependencies on tox environments.
  [@gforcada] #0
- Allow updating the current branch, rather than creating a new one.
  [@mauritsvanrees] #0
- Update `pre-commit` configuration.
  [@ale-rt] #0
- Allow repositories to not be recorded in `packages.txt`.
  [@gforcada] #0
- Report branch coverage.
  [@gforcada] #0
- Major update on the documentation.
  [@gforcada] #0
- Decide on standard towncrier snippets.
  [@gforcada] #2
- Do not push repository changes by default.
  [@gforcada] #3
- Do not run `tox` in parallel mode,
  when first configuring a repository.
  [@gforcada] #4
- New linting tool: check-manifest.
  [@gforcada] #6
- Use `git ls-files` to get the files that need to be linted.
  [@gforcada] #11
- Display project dependencies in a visual graph.
  [@gforcada] #14
- Run distributions' tests.
  [@gforcada] #15
- Add automatic (towncrier) news entry when configuring a repository.
  [@gforcada] #20
- Keep `setup.metadata` and `setup.options` in .meta.toml.
  [@mauritsvanrees] #24
- Add another linter: pyroma.
  [@gforcada] #28
- Analyze package dependencies with `z3c.dependencychecker`.
  [@gforcada] #34
- New formatter: zpretty.
  [@gforcada] #35
- New linter: `pipforester` (find circular dependencies).
  [@gforcada] #42
- New linter: check-python-versions
  [@gforcada] #44
- Generate coverage reports.
  [@gforcada] #45
- Support markdown for towncrier news snippets.
  [@gforcada] #49
- Add default dependency mappings for `z3c.dependencychecker`.
  [@gforcada] #52
- New linter: i18ndude.
  [@gforcada] #60
- Manage `.gitignore` as well.
  [@gforcada] #62
- Allow to configure OS dependencies to be installed (for CI jobs).
  [@gforcada] #65
- Allow to specify extra configuration options for `flake8`,
  like exclude files, plugins, etc..
  [@gforcada] #71
- Show coverage reports on GHA job summaries.
  [@gforcada] #72
- Improve documentation of all options, and ensure all options are documented.
  [@gforcada] #82
- Do not rely on a centralized workflow, but rather install shim GHA workflows.
  [@gforcada] #87
- New linter: `twine` to ensure repositories are always ready to be released.
  [@gforcada] #98
- Automatically detect if `pytest` or `zope.testrunner` is used.
  [@ericof] #120
- Add support for GitLab CI.
  [@gforcada] #131
- Allow to extend all sections of `pyproject.toml`.
  [@gforcada] #135
- Allow to specify a custom constraints.txt for `tox` environments to use.
  [@gforcada] #136
- Allow to specify environment variables on `tox.ini`.
  [@gforcada] #143
- Allow to specify towncrier issue format.
  [@ericof] #147
- Allow to customize GHA shim.
  [@ericof] #150
- Add `mxdev` support.
  [@ericof] #151


### Bug fixes:

- Do not ignore `setuptools` on `plone.base` mapping.
  [@mauritsvanrees] #0
- Use `constrain_package_deps = true` on `tox.ini`.
  [@mauritsvanrees] #0
- Fix changelog template to have a leading dot.
  [@mauritsvanrees] #0
- Add `ExtensionClass` namespaces on `Zope` mapping.
  [@jensens] #0
- Update `.gitignore` defaults.
  [@petschki] #0, #111
- Ignore `tox.ini` from check-manifest.
  [@gforcada] #5
- Adjust `flake8` configuration to be compatible with `black`.
  [@mauritsvanrees] #23
- Allow to configure `codespell` to ignore some words.
  [@gforcada] #29
- Specify, on `pyupgrade`, which python version to lint.
  [@mauritsvanrees] #41
- Add a missing `codespell` dependency.
  [@gforcada] #47
- Move `check-manifest` configuration over to `pyproject.toml`.
  [@gforcada] #56
- Improve codespell default configuration options by providing sane defaults.
  [@gforcada] #57
- Enforce `pipforester` to be run always.
  [@gforcada] #77
- Do not install dependencies on `z3c.dependencychecker` tox environment.
  [@gforcada] #84
- Ignore coverage errors when generating reports.
  [@mauritsvanrees] #110
- Update `.editorconfig` defaults.
  [@ericof] #116
- Update `.gitignore` defaults.
  [@ericof] #123
