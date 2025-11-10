#!/usr/bin/env python3
##############################################################################
#
# Copyright (c) 2025 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from .shared.call import call
from .shared.git import git_branch
from .shared.path import change_dir

import argparse
import pathlib
import shutil


def main():
    parser = argparse.ArgumentParser(
        description="Update a repository to PEP 420 native namespace."
    )
    parser.add_argument(
        "path", type=pathlib.Path, help="path to the repository to be updated"
    )
    parser.add_argument(
        "--branch",
        dest="branch_name",
        default=None,
        help="Define a git branch name to be used for the changes. If not"
        " given it is constructed automatically and includes the configuration"
        " type",
    )
    parser.add_argument(
        "--no-breaking",
        dest="breaking",
        action="store_false",
        default=True,
        help="Don't bump for breaking change. Use this if release is already alpha.",
    )
    parser.add_argument(
        "--no-commit",
        dest="commit",
        action="store_false",
        default=True,
        help='Don\'t "git commit" changes made by this script.',
    )
    parser.add_argument(
        "--push",
        dest="push",
        action="store_true",
        default=False,
        help="Push changes directly.",
    )
    parser.add_argument(
        "--interactive",
        dest="interactive",
        action="store_true",
        default=False,
        help="Run interactively: Scripts will prompt for input. Implies "
        "--no-commit, changes will not be committed and pushed automatically.",
    )
    parser.add_argument(
        "--no-tests",
        dest="run_tests",
        action="store_false",
        default=True,
        help="Skip running unit tests.",
    )

    args = parser.parse_args()
    path = args.path.absolute()

    if not (path / ".git").exists():
        raise ValueError("`path` does not point to a git clone of a repository!")
    if not (path / ".meta.toml").exists():
        raise ValueError("The repository `path` points to has no .meta.toml!")

    with change_dir(path) as cwd_str:
        cwd = pathlib.Path(cwd_str)
        branch_name = args.branch_name or "pep-420-native-namespace"
        updating = git_branch(branch_name)

        non_interactive_params = []
        if not args.interactive and args.commit:
            non_interactive_params = ["--no-input"]
        else:
            args.commit = False

        if args.breaking:
            call("bumpversion", "--breaking", *non_interactive_params)
        (path / "news" / "3928.breaking").write_text(
            "Replace ``pkg_resources`` namespace with PEP 420 native namespace.\n"
            "Support only Plone 6.2 and Python 3.10+.\n"
        )

        setup_py = []
        setup_text = (path / "setup.py").read_text()
        has_62_classifier = "Framework :: Plone :: 6.2" in setup_text
        for line in setup_text.splitlines():
            if "from setuptools import find_packages" in line:
                continue
            elif '"setuptools",' in line:
                continue
            elif "namespace_packages" in line:
                continue
            elif "packages=" in line:
                continue
            elif "package_dir=" in line:
                continue
            elif "zope.testrunner" in line:
                setup_py.append(
                    line.replace("zope.testrunner", "zope.testrunner >= 6.4")
                )
            elif "Framework :: Plone :: 6.0" in line:
                continue
            elif "Framework :: Plone :: 6.1" in line:
                continue
            elif "Programming Language :: Python :: 3.8" in line:
                continue
            elif "Programming Language :: Python :: 3.9" in line:
                continue
            elif 'python_requires=">=3.8"' in line:
                setup_py.append(
                    line.replace('python_requires=">=3.8"', 'python_requires=">=3.10"')
                )
            elif 'python_requires=">=3.9"' in line:
                setup_py.append(
                    line.replace('python_requires=">=3.9"', 'python_requires=">=3.10"')
                )
            else:
                setup_py.append(line)
                # One extra check after the line has been added.
                if (
                    not has_62_classifier
                    and "Framework :: Plone" in line
                    and "Framework :: Plone ::" not in line
                ):
                    setup_py.append(
                        line.replace("Framework :: Plone", "Framework :: Plone :: 6.2")
                    )

        (path / "setup.py").write_text("\n".join(setup_py) + "\n")

        for src_dir_cont in (path / "src").iterdir():
            if not src_dir_cont.is_dir():
                continue
            pkg_init = src_dir_cont / "__init__.py"
            if pkg_init.exists():
                pkg_init.unlink()
            for pkg_dir_cont in src_dir_cont.iterdir():
                if not pkg_dir_cont.is_dir():
                    continue
                sub_pkg_init = pkg_dir_cont / "__init__.py"
                if sub_pkg_init.exists():
                    if "pkg_resources" in sub_pkg_init.read_text():
                        sub_pkg_init.unlink()

        if args.commit:
            print("Adding all changes ...")
            call("git", "add", ".")

        if args.run_tests:
            tox_path = shutil.which("tox") or (cwd / "venv" / "bin" / "tox")
            call(tox_path, "-p", "auto")

        if args.commit:
            print("Committing all changes ...")
            call("git", "commit", "-m", "Switch to PEP 420 native namespace.")
            if not args.push:
                print("All changes committed. Please check and push manually.")
                return
            call("git", "push", "--set-upstream", "origin", branch_name)
            if updating:
                print("Updated the previously created PR.")
            else:
                print(
                    "Are you logged in via `gh auth login` to create a PR? (y/N)?",
                    end=" ",
                )
                if input().lower() == "y":
                    call(
                        "gh",
                        "pr",
                        "create",
                        "--fill",
                        "--title",
                        "Switch to PEP 420 native namespace.",
                    )
                else:
                    print("If everything went fine up to here:")
                    print("Create a PR, using the URL shown above.")
        else:
            print("Applied all changes. Please check and commit manually.")
