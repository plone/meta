---
myst:
  html_meta:
    "description": "Write custom Jinja2 templates for plone.meta"
    "property=og:description": "Write custom Jinja2 templates for plone.meta"
    "property=og:title": "Write Custom Templates"
    "keywords": "plone.meta, custom templates, Jinja2"
---

# Write Custom Templates

<!-- diataxis: how-to -->

If the `default` configuration type does not meet your needs and
`extra_lines` is not sufficient, you can create a custom template set.

:::{note}
Custom templates require modifying the plone.meta source. This is an
advanced topic. For most use cases, {doc}`customizing via .meta.toml
<customize-meta-toml>` is the recommended approach.
:::

## How the template system works

plone.meta uses a Jinja2 `FileSystemLoader` with two search paths, in order:

1. `src/plone/meta/<config_type>/` -- the active configuration type
2. `src/plone/meta/default/` -- the fallback

When a template is requested (e.g. `tox.ini.j2`), Jinja2 looks in the
config type directory first. If it finds the file there, it uses that
version. Otherwise, it falls back to `default/`.

This means you can override *individual* templates while inheriting the
rest from `default/`.

## Create a custom configuration type

1. In your fork or local clone of plone.meta, create a new directory
   alongside `default/`:

   ```shell
   mkdir -p src/plone/meta/mytype
   ```

2. Copy only the templates you want to change:

   ```shell
   cp src/plone/meta/default/tox.ini.j2 src/plone/meta/mytype/
   ```

3. Edit the copied template. Templates use a custom Jinja2 syntax with
   `%(variable)s` for variable substitution instead of the standard
   `{{ variable }}`:

   ```
   %(extra_lines)s
   %(test_runner)s
   %(constraints_file)s
   ```

   See {doc}`../reference/generated-files` for the full list of templates
   and their variables.

4. Register the new type by adding it to the `choices` list in
   `config_package.py`:

   ```python
   parser.add_argument(
       "-t",
       "--type",
       choices=[
           "default",
           "mytype",
       ],
       ...
   )
   ```

5. Create a `packages.txt` file in your new directory (can be empty):

   ```shell
   touch src/plone/meta/mytype/packages.txt
   ```

6. Reinstall plone.meta:

   ```shell
   venv/bin/pip install -e .
   ```

## Use the custom type

Apply the custom configuration to a repository:

```shell
venv/bin/config-package --type mytype /path/to/package
```

The type is stored in `.meta.toml` under `[meta] template`, so subsequent
runs do not need the `--type` flag.

## Template variables

All templates receive their variables from `.meta.toml` via the
`_get_options_for()` method. The variable names correspond to the keys
in each `.meta.toml` section.

Additionally, some variables are computed:

`config_type`
: The active configuration type name (e.g. `"default"`, `"mytype"`).

`news_folder_exists`
: `True` if a `news/` directory exists in the target repository.

`changes_extension`
: `"md"` or `"rst"` depending on whether `CHANGES.md` exists.

`prime_robotframework`
: `True` if `plone.app.robotframework` is detected as a dependency.

`package_name`
: The repository directory name (or overridden via `.meta.toml`).

## Considerations

- Keep your custom templates in a fork or branch. Upstream plone.meta
  only ships the `default` type.
- When upstream templates change, you will need to merge those changes
  into your overridden files.
- If your customization is generally useful, consider
  [requesting it upstream](https://github.com/plone/meta/issues/new)
  as a new `extra_lines` option instead.
