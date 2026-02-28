# Use a Custom Branch Name

<!-- diataxis: how-to -->

By default, `config-package` creates a branch named
`config-with-default-template-<commit-hash>`. You can override this.

## Use a specific branch name

```shell
venv/bin/config-package --branch my-feature-branch /path/to/package
```

If the branch already exists, `config-package` checks it out and updates it.
If it does not exist, it creates a new branch.

## Update the current branch

To apply changes without creating a new branch:

```shell
venv/bin/config-package --branch current /path/to/package
```

This is useful when you have already created a branch manually and want to
update it with the latest configuration.
