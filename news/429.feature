Add a weekly `auto-update.yml` workflow that runs `config-package` from the latest plone.meta release and opens a pull request with the changes.
With it, Dependabot only opens security updates and pre-commit.ci updates quarterly.
Disable it with `auto_update = false` in the `[github]` section of `.meta.toml`.
@jladage
