======
Config
======

Purpose
-------

Bring the configuration of the Plone packages into a common state and keep it there.

Contents
--------

The `default` directory contains the following files:

* editorconfig

  - This file is copied to `.editorconfig` and allows developers to have a
    common editor configuration experience in all repos.

* lint-requirements.txt.j2

  - list of packages needed to run the GitHub actions.

* linting.yml.j2

  - Configuration for GitHub actions.

* packages.txt

  - This file lists the packages which use the configuration in the directory.

* pyproject.toml.j2

  - configuration for various python related tools.

* setup.cfg.j2

  - common `setup.cfg`, which should be copied to the repository of the package

* tox.ini.j2

  - tox configuration, which should be copied to the repository of the package

Usage
-----

Preparation
+++++++++++

The script needs a ``venv`` with some packages installed::

    $ python3.11 -m venv .
    $ bin/pip install -r requirements.txt

To use the configuration provided here in a package call the following script::

    $ bin/python config-package.py <path-to-package> [<additional-options>]

See ``--help`` for details.

The script does the following steps:

1. Add the package name to ``packages.txt``
2. Copies various files to the repository
3. Remove a possibly existing ``.travis.yml`` and ``bootstrap.py``
4. Run all ``tox`` _targets_. The ``tox`` script may be either on the current
   ``$PATH`` or in the ``bin`` subfolder of the current working directory.
5. Create a branch and a few commits with all the changes

After running the script you should manually do the following steps:

1. Double check the changes and adapt the code to them
2. Add a news entry
2. Check in possible changes in the plone/meta repository itself

CLI arguments
+++++++++++++

The following arguments are supported.

--commit-msg=MSG
  Use MSG as commit message instead of an artificial one.

--no-commit
  Don't automatically commit changes after the configuration run.

--no-push
  Avoid pushing at the end of the configuration run.

--branch
  Define a specific git branch name to be created for the changes. By default
  the script creates one which includes the name of the configuration type.

The following options are only needed one time as their values are stored in
``.meta.toml.``.

--type
  Define the configuration type, by now `default` is the only option

Options
+++++++

There is almost no options to configure so far,
but that does not mean it has to be this way!

See ``zopefoundation/meta`` for plenty of examples
of options that can be added to the configuration files
if the need arises.

``.meta.toml`` file is added inside the package repository.
This file stores the template name and commit id
of the *meta* repository at the time of the run.
This file is generated during the configuration run,
if it does not exist or at least gets updated.
Example:

.. code-block:: ini

    [meta]
    template = "default"
    commit-id = "< commit-hash >"

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

Meta Options
````````````

template
  Name of the configuration type, to be used as the template for the
  repository. Currently read-only.

commit-id
  Commit of the meta repository, which was used for the last configuration run.
  Currently read-only.

Dependencies
````````````

Options to configure `z3c.dependencychecker`.

ignores
  Text line of a list of packages that should be ignored.

mappings
  List of text lines with mappings of imports and packages providing them.
  i.e. `Zope` provides `Products.Five` and other importable packages.

Check-manifest
``````````````

Options to configure `check-manifest`.

additional-ignores
  List of text lines to be added on check-manifest configuration for files to be ignored.

Codespell
`````````

Options to configure `codespell`.

additional-ignores
  List of words that should be ignored by `codespell`.

Hints
-----

* Calling ``config-package.py`` again updates a previously created pull request
  if there are changes made in the files ``config-package.py`` touches.

* Call ``bin/check-python-versions <path-to-package> -h`` to see how to fix
  version mismatches in the *lint* tox environment.

Calling a script on multiple repositories
-----------------------------------------

The ``config-package.py`` script only runs on a single repository.
To update multiple repositories at once you can use ``multi-call.py``.
It runs a given script on all repositories listed in a ``packages.txt`` file.

Usage
+++++

To run a script on all packages listed in a ``packages.txt`` file call
``multi-call.py`` the following way::

    $ bin/python multi-call.py <name-of-the-script.py> <path-to-packages.txt> <path-to-clones> <arguments-for-script>

See ``--help`` for details.

The script does the following steps:

1. It does the following steps for each line in the given ``packages.txt``
   which does not start with ``#``.
2. Check if there is a repository in ``<path-to-clones>`` with the name of the
   repository. If it does not exist: clone it. If it exists: clean the clone
   from changes, switch to ``master`` branch and pull from origin.
3. Call the given script with the package name and arguments for the script.

.. caution::

  Running this script stashes any uncommitted changes in the repositories,
  run ``git stash pop`` to recover them.

Re-enabling GitHub Actions
--------------------------

After a certain period of time (currently 60 days) without commits GitHub
automatically disables Actions. They can be re-enabled manually per repository.
There is a script to do this for all repositories. It does no harm if Actions
is already enabled for a repository.

Preparation
+++++++++++

* Install GitHub's CLI application, see https://github.com/cli/cli.

* Authorize using the application:

  - ``gh auth login``
  - It is probably enough to do it once.

Usage
+++++

To run the script just call it::

    $ bin/python re-enable-actions.py

Dropping support for legacy Python versions
-------------------------------------------

To drop support for Python 2.7 up to 3.6 several steps have to be done as
documented at https://zope.dev/developer/python2.html#how-to-drop-support.
There is a script to ease this process.

Preparation
+++++++++++

* The package to remove legacy python support from has to have a ``.meta.toml``
  file aka it must be under control of the ``config-package.py`` script.

Usage
+++++

To run the script call::

    $ bin/python drop-legacy-python.py <path-to-package>

Additional optional parameters, see above at ``config-package.py`` for a
descriptions of them:

* ``--branch``

You can call the script interactively by passing the argument
``--interactive``, this will let the various scripts prompt for information and
prevent automatic commits and pushes. That way all changes can be viewed before
committing them.
