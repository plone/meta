# Upgrade guide

This file describes the breaking changes between major versions.

## From `main` to `2.x`


### Test matrix

You can now define the combinations of Plone versions and Python versions to be tested.

`plone.meta` provides a default combination (the same as used by Plone itself), but can be overridden in the file `.meta.toml`.

```toml
[tox]
test_matrix = {"6.2" = ["3.14", "3.11"], "6.1" = ["3.13", "3.12", "3.11", "3.10", "3.9"]}
```

This will be used to generate the necessary `tox` environments and the GitHub Actions that will be run on each pull request.

> [!TIP]
> 🍀 `plone.meta` tries to be a bit more environmentally friendly.
> On GitHub, only the first and last Python versions will be added for testing.


### Constraints

The `constraints_file` option in `.meta.toml`'s `[tox]` table was renamed to `constraints_files`, and the type of its value was changed from a string to a dictionary.

This option continues to be optional.

The dictionary keys must be Plone versions, and each key's value must be the constraints file for that Plone version.

```toml
[tox]
# OLD
constraints_file = "https://example.org/my-custom-constraints.txt"
# NEW
constraints_files = {"6.2" = "https://example.org/constraints.6.2.txt", "6.1" = "https://example.org/constraints.6.1.txt"}
```


### GitHub Actions

The `py_versions` option in `.meta.toml`'s `[github]` table is deprecated.
We use the new `test_matrix` option from `[tox]` table, as we now can run multiple Python versions from within `tox` itself.

### GitHub variables

The GitHub variables `TEST_OS_VERSIONS` and `TEST_PYTHON_VERSIONS` are deprecated and no longer used.


### GitLab images

The `custom_image` option in `.meta.toml`'s `[gitlab]` table was renamed to `custom_images`, and the type of its value was changed from a string to a dictionary.

This option continues to be optional.

The dictionary keys must be Python versions, and the values a Docker image for that Python version.

```toml
[tox]
# OLD
custom_images = "python:3.11-bullseye"
# NEW
custom_images = {"3.13" = "python:3.13-bookworm", "3.12" = "python:3.12-bookworm"}
```
