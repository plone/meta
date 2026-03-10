# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "plone.meta"
copyright = "2023-2026, Plone Foundation"  # noqa: A001
author = "Plone Foundation"
release = "2.5.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
]

myst_enable_extensions = [
    "deflist",
    "colon_fence",
    "fieldlist",
]

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "plone_sphinx_theme"

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/plone/meta",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/plone.meta/",
            "icon": "fa-brands fa-python",
        },
    ],
    "use_edit_page_button": True,
    "navigation_with_keys": True,
}

html_context = {
    "github_user": "plone",
    "github_repo": "meta",
    "github_version": "2.x",
    "doc_path": "docs/sources",
}

html_extra_path = ["llms.txt"]
