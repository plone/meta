Made `pytest-plone` test dependency in `tox.ini` optional. Specify `use_pytest_plone =
false` if you don't want to use it.
Also added `check_manifest_extra_lines` for `pyproject.toml`, you can use it for
specifying corner cases like `ignore-bad-ideas`.
[reinout]
