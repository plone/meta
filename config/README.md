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
