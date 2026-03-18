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

from .config_package import META_HINT
from .shared.call import call
from .shared.git import get_branch_name
from .shared.git import git_branch
from .shared.path import change_dir
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import argparse
import ast
import contextlib
import os
import pathlib
import sys
import tomlkit

PROJECT_SIMPLE_KEYS = (
    "name",
    "version",
    "description",
)
IGNORE_KEYS = (
    "zip_safe",
    "long_description_content_type",
    "package_dir",
    "packages",
    "include_package_data",
    "test_suite",
    "tests_require",
)
UNCONVERTIBLE_KEYS = (
    "cmdclass",
    "ext_modules",
    "headers",
    "cffi_modules",
)

LICENSE_CLASSIFIER_TO_SPDX = {
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)": "GPL-2.0-only",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)": "GPL-2.0-or-later",
    "License :: OSI Approved :: Zope Public License": "ZPL-2.1",
    "License :: OSI Approved :: BSD License": "BSD-3-Clause",
}

LICENSE_TO_SPDX = {
    "bsd": "BSD-3-Clause",
    "gpl": "GPL-2.0-only",
    "gplv2": "GPL-2.0-only",
    "gplversion2": "GPL-2.0-only",
    "gplv2orlater": "GPL-2.0-or-later",
    "gplversion2orlater": "GPL-2.0-or-later",
    "lgpl": "LGPL-2.1-only",
    "zpl21": "ZPL-2.1",
}


def get_pyproject_toml(path, comment=""):
    """Parse ``pyproject.toml`` and return its content as ``TOMLDocument``.

    Args:
        path (str, pathlib.Path): Filesystem path to a pyproject.toml file.

    Kwargs:
        comment (str): Optional comment added to the top of the file.

    Returns:
        A TOMLDocument instance from the pyproject.toml file.
    """
    toml_contents = ""
    if path.exists():
        toml_contents = path.read_text()

    if comment and not (
        toml_contents.startswith(comment) or toml_contents.startswith(f"# \n{comment}")
    ):
        toml_contents = f"{comment}\n{toml_contents}"

    return tomlkit.loads(toml_contents)


def parse_setup_function(ast_node, assigned_names=None):
    """Parse values out of the setup call ast definition"""
    setup_kwargs = {}
    assigned_names = assigned_names or {}

    for kw_arg in ast_node.keywords:
        if isinstance(kw_arg.value, (ast.Constant, ast.List, ast.Tuple)):
            setup_kwargs[kw_arg.arg] = ast.literal_eval(kw_arg.value)
        elif isinstance(kw_arg.value, ast.Dict):
            # This could hide variables
            try:
                setup_kwargs[kw_arg.arg] = ast.literal_eval(kw_arg.value)
            except ValueError:
                # Need to crawl the dictionary
                gathered = {}
                for key, value in zip(kw_arg.value.keys, kw_arg.value.values):
                    if isinstance(value, ast.Name):
                        gathered[key.value] = assigned_names.get(value.id, "")
                    elif isinstance(value, ast.BinOp):
                        if isinstance(value.left, ast.List):
                            # e. g. "['Sphinx'] + BROWSER_REQUIRES"
                            print("XXX Cannot convert list addition XXX")
                            print("XXX Please fix setup.py manually first XXX")
                            print("XXX list addition: " f"{ast.unparse(value)} XXX")
                            sys.exit(1)
                        # Interpolated string 'x%sy' % foo
                        unformatted = value.left.value
                        variable = assigned_names.get(value.right.id, "")
                        formatted = unformatted.replace("%s", variable)
                        gathered[key.value] = formatted
                    elif isinstance(value, (ast.List, ast.Tuple)):
                        try:
                            gathered[key.value] = ast.literal_eval(value)
                        except ValueError:
                            # Probably a variable in the list
                            lst = []
                            for member in value.elts:
                                if isinstance(
                                    member, (ast.Constant, ast.List, ast.Tuple)
                                ):
                                    lst.append(ast.literal_eval(member.value))
                                elif isinstance(member, ast.BinOp):
                                    unformatted = member.left.value
                                    variable = assigned_names.get(member.right.id, "")
                                    formatted = unformatted.replace("%s", variable)
                                    lst.append(formatted)
                                else:
                                    lst.append(ast.literal_eval(member.value))
                            gathered[key.value] = lst
                    else:
                        try:
                            gathered[key.value] = ast.literal_eval(value)
                        except ValueError:
                            print("XXX Cannot convert dictionary value XXX")
                            print("XXX Please fix setup.py manually first XXX")
                            print(f"XXX Dictionary key: {key.value} XXX")
                            print(ast.dump(value, indent=2))
                            sys.exit(1)
                setup_kwargs[kw_arg.arg] = gathered
        elif isinstance(kw_arg.value, ast.Name):
            if kw_arg.value.id in assigned_names:
                value = assigned_names.get(kw_arg.value.id)
            else:
                value = kw_arg.value.id
            setup_kwargs[kw_arg.arg] = value

    return setup_kwargs


def handle_classifiers(classifiers):
    new_classifiers = []
    license_counter = 0
    license_classifiers = []

    for classifier in classifiers:
        if classifier.startswith("License"):
            if classifier not in LICENSE_CLASSIFIER_TO_SPDX.keys():
                print(f"License classifier {classifier} was not expected")
                print("either remove it and run the script again,")
                print("or double check if that was the intended classifier.")
                sys.exit()
            license_counter += 1
            license_classifiers.append(classifier)
            continue
        elif classifier in ("Framework :: Zope2", "Framework :: Zope :: 2"):
            continue
        elif classifier == "Framework :: Zope3":
            new_classifiers.append("Framework :: Zope :: 3")
        else:
            new_classifiers.append(classifier)

    if license_counter > 1:
        print("There are too many License :: classifiers, fix that first!")
        sys.exit()

    return new_classifiers, license_classifiers


def check_license(license, license_classifier):
    """Check license sanity check.

    Compare that the license key on setup.py and the license related classifier
    match, otherwise complain.

    If they match, return a SPDX license complain expression.
    """
    normalized_license = "".join(ch for ch in license.lower() if ch.isalnum())
    license_spdx = LICENSE_TO_SPDX.get(normalized_license)
    if len(license_classifier) == 0:
        if license_spdx:
            return license_spdx
        print(f'Unknown license "{license}", please fix it or remove it ')
        print("so that the script does not complain.")
        sys.exit(1)

    classifier_spdx = LICENSE_CLASSIFIER_TO_SPDX[license_classifier[0]]
    if license_spdx and license_spdx != classifier_spdx:
        print(
            f'License "{license}" does not match classifier "{license_classifier[0]}".'
        )
        sys.exit(1)

    return classifier_spdx


def setup_args_to_toml_dict(setup_py_path, setup_kwargs):
    """Iterate over setup_kwargs and generate a dictionary of values suitable
    for pyproject.toml and a dictionary with unconverted arguments
    """
    toml_dict = {"project": {}}
    p_data = toml_dict["project"]

    for key in IGNORE_KEYS:
        setup_kwargs.pop(key, None)

    for key in UNCONVERTIBLE_KEYS:
        setup_kwargs.pop(key, None)

    for key in PROJECT_SIMPLE_KEYS:
        if key in setup_kwargs:
            p_data[key] = setup_kwargs.pop(key)

    original_classifiers = setup_kwargs.pop("classifiers", [])
    p_data["classifiers"], license_classifiers = handle_classifiers(
        original_classifiers
    )

    license = setup_kwargs.pop("license")
    p_data["license"] = check_license(license, license_classifiers)

    readme = None
    for readme_name in ("README.rst", "README.txt"):
        if (setup_py_path.parent / readme_name).exists():
            readme = readme_name
            break

    changelog = None
    for changelog_name in ("CHANGES.rst", "CHANGES.txt"):
        if (setup_py_path.parent / changelog_name).exists():
            changelog = changelog_name
            break

    if readme and not changelog:
        p_data["readme"] = readme
    elif readme and changelog:
        readme_spec = tomlkit.inline_table()
        readme_spec.update({"file": [readme, changelog]})
        toml_dict["tool"] = {"setuptools": {"dynamic": {"readme": readme_spec}}}
        dynamic_attributes = p_data.setdefault("dynamic", [])
        dynamic_attributes.append("readme")
    else:
        print("XXX WARNING XXX: This package has no README.rst or README.txt!")

    if "python_requires" in setup_kwargs:
        p_data["requires-python"] = setup_kwargs.pop("python_requires")

    if "author" in setup_kwargs:
        name = setup_kwargs.pop("author").replace("Zope Corporation", "Zope Foundation")
        # Fix bad capitalization found in some packages
        name = name.replace("Contributors", "contributors")
        author_dict = {"name": name}
        if "author_email" in setup_kwargs:
            email = setup_kwargs.pop("author_email").replace("zope.org", "zope.dev")
            author_dict["email"] = email
        p_data["authors"] = tomlkit.array()
        p_data["authors"].add_line(author_dict)

    maintainers_table = {
        "name": "Plone Foundation and contributors",
        "email": "zope-dev@zope.dev",
    }
    p_data["maintainers"] = tomlkit.array()
    p_data["maintainers"].add_line(maintainers_table)

    entry_points = {}
    scripts = {}
    ep_data = setup_kwargs.pop("entry_points", {})

    if isinstance(ep_data, str):
        ep_lines = [x.strip() for x in ep_data.split("\n") if x]
        ep_data = {}
        for line in ep_lines:
            key_buffer = ""
            if line.startswith("["):
                line = line.replace("[", "").replace("]", "").strip()
                key_buffer = line
            else:
                if line and key_buffer:
                    line = line.replace(" = ", "=").strip()
                    ep_data[key_buffer] = line
                    key_buffer = ""

    for ep_type, ep_list in ep_data.items():
        if ep_type == "console_scripts":
            for ep in ep_list:
                ep_name, ep_target = (x.strip() for x in ep.split("="))
                scripts[ep_name] = ep_target
        else:
            entrypoint_dict = entry_points.setdefault(ep_type, {})
            for ep in ep_list:
                ep_name, ep_target = (x.strip() for x in ep.split("="))
                entrypoint_dict[ep_name] = ep_target

    if scripts:
        p_data["scripts"] = scripts
    if entry_points:
        p_data["entry-points"] = entry_points

    extras = setup_kwargs.pop("extras_require", {})
    if isinstance(extras, str):
        print(" XXX Error converting setup.py XXX")
        print(" XXX Clean up setup.py manually first:")
        print(f" Change extras_require value to not use variable {extras}!")
        print(f" Instead, insert the actual value of variable {extras}.")
        sys.exit(1)
    opt_deps = {}
    for e_name, e_list in extras.items():
        opt_deps[e_name] = e_list
    if opt_deps:
        p_data["optional-dependencies"] = opt_deps

    install_reqs = setup_kwargs.pop("install_requires", [])
    if install_reqs:
        for dependency in install_reqs:
            if dependency.startswith("setuptools"):
                print('XXX Found "setuptools" as install time dependency.')
                print("XXX Please check if it is really needed!")
                break
        p_data["dependencies"] = install_reqs

    keywords = setup_kwargs.pop("keywords", "")
    if keywords and isinstance(keywords, str):
        p_data["keywords"] = keywords.split()
    elif isinstance(keywords, (list, tuple)):
        p_data["keywords"] = keywords

    project_urls = setup_kwargs.pop("project_urls", {})
    url = setup_kwargs.pop("url", "")
    if "github" in url and "Source" not in project_urls:
        project_urls["Source"] = url
    if "Sources" in project_urls:
        project_urls["Source"] = project_urls.pop("Sources")
    if "Issue Tracker" in project_urls:
        project_urls["Issues"] = project_urls.pop("Issue Tracker")
    if project_urls:
        p_data["urls"] = project_urls

    return (setup_kwargs, toml_dict)


def parse_setup_py(path):
    """Parse values out of setup.py"""
    setup_kwargs = {}
    assigned_names = {}

    # Nasty: Import the setup module file to get at the resolved variables
    import_spec = spec_from_file_location("setup", path)
    setup_module = module_from_spec(import_spec)
    try:
        with open(os.devnull, "w") as fp:
            with contextlib.redirect_stderr(fp):
                import_spec.loader.exec_module(setup_module)
    except (FileNotFoundError, SystemExit):
        pass

    for key in dir(setup_module):
        assigned_names[key] = getattr(setup_module, key)

    file_contents = pathlib.Path(path).read_text()

    # Create the ast tree for the setup module to find the setup call
    # definition in order to parse out the call arguments.
    ast_tree = ast.parse(file_contents)
    setup_node = None

    for ast_node in ast_tree.body:
        if (
            isinstance(ast_node, ast.Expr)
            and isinstance(ast_node.value, ast.Call)
            and ast_node.value.func.id == "setup"
        ):
            setup_node = ast_node.value
            break

    if setup_node is not None:
        setup_kwargs = parse_setup_function(setup_node, assigned_names)
    leftover_setup_kwargs, toml_dict = setup_args_to_toml_dict(path, setup_kwargs)

    return leftover_setup_kwargs, toml_dict


def rewrite_pyproject_toml(path, toml_dict):
    toml_file = path / "pyproject.toml"
    p_toml = get_pyproject_toml(toml_file)

    def recursive_merge(dict1, dict2):
        for key, value in dict2.items():
            if (
                key in dict1
                and isinstance(dict1[key], dict)
                and isinstance(value, dict)
            ):
                dict1[key] = recursive_merge(dict1[key], value)
            else:
                # We will not overwrite existing values!
                if key not in dict1:
                    dict1[key] = value
        return dict1

    p_toml = recursive_merge(p_toml, toml_dict)

    # Format long lists
    p_toml["project"]["classifiers"].multiline(True)
    p_toml["project"]["authors"].multiline(True)
    p_toml["project"]["maintainers"].multiline(True)
    if (
        "dependencies" in p_toml["project"]
        and len(p_toml["project"]["dependencies"]) > 1
    ):
        p_toml["project"]["dependencies"].multiline(True)
    if "keywords" in p_toml["project"] and len(p_toml["project"]["keywords"]) > 4:
        p_toml["project"]["keywords"].multiline(True)

    opt_deps = p_toml["project"].get("optional-dependencies", {})
    for key, value in opt_deps.items():
        if len(value) > 1:
            p_toml["project"]["optional-dependencies"][key].multiline(True)

    # Last sanity check to see if anything is missing
    if "requires-python" not in p_toml["project"]:
        p_toml["project"]["requires-python"] = ">=3.10"

    # Create a fresh TOMLDocument instance so I can control section sorting
    new_doc = tomlkit.loads(META_HINT.format(config_type="default"))

    changes_file = "CHANGES.rst"
    if (path / "CHANGES.md").exists():
        changes_file = "CHANGES.md"
    project_name = path.resolve().parts[-1]
    existing_branch = get_branch_name(override="current", config_type="default")
    issues_url = "https://github.com/plone/Products.CMFPlone/issues"
    project_url = f"https://github.com/plone/{project_name}"
    changelog = f"{project_url}/blob/{existing_branch}/{changes_file}"

    comment_header = (
        "START-MARKER-MANUAL-CONFIG",
        "Anything from here until END-MARKER-MANUAL-CONFIG",
        "will be kept by plone.meta",
    )

    for key in sorted(p_toml.keys()):
        if key == "project":
            for text in comment_header:
                new_doc.add(tomlkit.comment(text))
        new_doc[key] = p_toml.get(key)
        if key == "project":
            if "urls" not in new_doc[key]:
                urls_table = tomlkit.table()
                urls_table.append("Source", project_url)
                new_doc[key].append("urls", urls_table)
            new_doc[key]["urls"].append("Issues", issues_url)
            new_doc[key]["urls"].append("Changelog", changelog)
            new_doc.add(tomlkit.comment("END-MARKER-MANUAL-CONFIG"))

    return tomlkit.dumps(new_doc)


def rewrite_setup_py(path, leftover_setup_kwargs):
    """Write new setup py with unconverted call arguments

    While it's possible to take the ``setup.py`` source, parse out an ast
    tree and manipulate that to generate new code it loses all comments,
    spacing and formatting when dumping it back out. So I am doing it with an
    axe. This code assumes that the call to ``setup`` is the last thing in the
    file.
    """
    new_setup_py = []
    with open(path) as fp:
        old_setup_py = fp.readlines()

    for line in old_setup_py:
        if line.startswith("setup("):
            break

        new_setup_py.append(line)

    new_setup_py.append("# See pyproject.toml for package metadata\n")
    if not leftover_setup_kwargs:
        new_setup_py.append("setup()\n")
    else:
        new_setup_py.append("setup(\n")
        for key, value in leftover_setup_kwargs.items():
            new_setup_py.append(f"    {key}={value},\n")
        new_setup_py.append(")\n")

    return "".join(new_setup_py)


def package_sanity_check(path):
    """Sanity checks for the provided path"""
    sane = True

    if not path.exists():
        print(f" - no such path {path}.")
        sane = False

    if not path.is_dir():
        print(f" - {path} is not a folder")
        sane = False

    if not (path / "setup.py").exists():
        print(" - no setup.py found, cannot convert package.")
        sane = False

    if not (path / ".meta.toml").exists():
        print(" - no .meta.toml found, cannot convert package.")
        sane = False

    return sane


def write_news_entry(path):
    news_folder = path / "news"
    if not news_folder.exists():
        print("WARNING: no news entry created as there is no 'news' folder")
        return

    filename = "+setup-to-pyproject.internal"
    news_entry = news_folder / filename
    if (path / "CHANGES.md").exists():
        changelog_text = (
            "Move package metadata from `setup.py` to `pyproject.toml` @plone\n"
        )
    else:
        changelog_text = "Move package metadata from ``setup.py`` to ``pyproject.toml``.\n[plone devs]\n"
    news_entry.write_text(changelog_text)

    with change_dir(path):
        call("git", "add", f"news/{filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Move package metadata from setup.py to pyproject.toml."
    )
    parser.add_argument(
        "path", type=pathlib.Path, help="path to the repository to be configured"
    )
    parser.add_argument(
        "--branch",
        dest="branch_name",
        default=None,
        help="Define a git branch name to be used for the changes. "
        "If not given it is constructed automatically and includes "
        'the configuration type. Use "current" to update the current branch.',
    )
    args = parser.parse_args()

    print(f"Converting package {args.path.name}")

    if not package_sanity_check(args.path):
        print("Conversion not possible, exiting.")
        sys.exit()

    leftover_setup_kwargs, toml_dict = parse_setup_py(args.path / "setup.py")

    # Sanity check - if project has been converted already, give up.
    if "name" not in toml_dict["project"] and "version" not in toml_dict["project"]:
        print("Package has been converted already, exiting.")
        sys.exit()

    toml_content = rewrite_pyproject_toml(args.path, toml_dict)
    setup_content = rewrite_setup_py(args.path / "setup.py", leftover_setup_kwargs)

    (args.path / "pyproject.toml").write_text(toml_content)
    (args.path / "setup.py").write_text(setup_content)

    print("Look through setup.py and pyproject.toml to see if it needs changes.")
    write_news_entry(args.path)

    with change_dir(args.path):
        branch_name = args.branch_name or "convert-setup-py-to-pyproject-toml"
        git_branch(branch_name)

        commit_msg = "feat: move metadata from setup.py to pyproject.toml."
        call("git", "add", "setup.py", "pyproject.toml")
        call("git", "commit", "-m", commit_msg)

    print(f"Finished converting {args.path.name}.")
