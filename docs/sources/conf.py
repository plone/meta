# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = "plone.meta"
copyright = "2023-2026, Plone Foundation"  # noqa: A001
author = "Gil Forcada Codinachs, Jens Klein, and contributors"
release = "2.0"

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

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = "shibuya"

html_theme_options = {
    "logo_target": "/plone.meta/",
    "accent_color": "blue",
    "color_mode": "dark",
    "dark_code": True,
    "nav_links": [
        {
            "title": "GitHub",
            "url": "https://github.com/plone/meta",
        },
        {
            "title": "PyPI",
            "url": "https://pypi.org/project/plone.meta/",
        },
        {
            "title": "Plone Docs",
            "url": "https://6.docs.plone.org/",
        },
    ],
}

html_extra_path = ["llms.txt"]
html_static_path = ["_static"]
