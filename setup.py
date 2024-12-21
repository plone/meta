"""Setup for plone.meta package
"""

from pathlib import Path
from setuptools import find_packages
from setuptools import setup


setup(
    name="plone.meta",
    version="1.0.dev0",
    author="Plone Foundation",
    author_email="releaseteam@plone.org",
    description="Helper functions for package management",
    long_description=f"{Path('README.md').read_text()}\n\n{Path('CHANGES.md').read_text()}",
    long_description_content_type="text/markdown",
    keywords="plone packaging",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    license="GPL version 2",
    url="https://github.com/plone/meta",
    project_urls={
        "Issue Tracker": "https://github.com/plone/meta/issues",
        "Sources": "https://github.com/plone/meta",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["plone"],
    install_requires=[
        "setuptools",
        "Jinja2",
        "editorconfig",
        "pyyaml",
        "tomlkit",
        "tox",
        "validate-pyproject[all]",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "config-package=plone.meta.config_package:main",
            "multi-call=plone.meta.multi_call:main",
            "re-enable-actions=plone.meta.re_enable_actions:main",
        ],
    },
)
