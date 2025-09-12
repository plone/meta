from .shared.call import call
from .shared.git import get_branch_name
from .shared.git import git_branch
from .shared.git import git_server_url
from .shared.path import change_dir
from functools import cached_property
from importlib.metadata import version

import argparse
import collections
import configparser
import editorconfig
import jinja2
import pathlib
import re
import shutil
import tomlkit
import validate_pyproject
import yaml


META_HINT = """\
# Generated from:
# https://github.com/plone/meta/tree/main/src/plone/meta/{config_type}
# See the inline comments on how to expand/tweak this configuration file"""
META_HINT_MARKDOWN = """\
<!--
Generated from:
https://github.com/plone/meta/tree/main/src/plone/meta/{config_type}
See the inline comments on how to expand/tweak this configuration file
--> """
DEFAULT = object()

# List all python versions we want to test a given Plone version against
TOX_TEST_MATRIX = {
    "6.2": ["3.13", "3.12", "3.11", "3.10"],
    "6.1": ["3.13", "3.12", "3.11", "3.10"],
    "6.0": ["3.13", "3.12", "3.11", "3.10", "3.9"],
}

MXDEV_CONSTRAINTS = "constraints-mxdev.txt"

DOCKER_IMAGES = {
    "3.13": "python:3.13-bookworm",
    "3.12": "python:3.12-bookworm",
    "3.11": "python:3.11-bookworm",
    "3.10": "python:3.10-bookworm",
    "3.9": "python:3.9-bookworm",
}

# Rather than pointing configured repositories to `plone.meta`'s `main` branch
# to get their GHA workflows, point them to an ever evolving branch.
#
# This has a few benefits:
# - configured repositories do not point to outdated GHA workflows
# - `plone.meta` can do breaking changes on GHA workflows and roll them gradually
GHA_DEFAULT_REF = "2.x"

GHA_DEFAULT_JOBS = [
    "qa",
    "coverage",
    "dependencies",
    "release_ready",
    "circular",
]

GITLAB_DEFAULT_JOBS = [
    "lint",
    "release-ready",
    "dependencies",
    "circular-dependencies",
    "testing",
    "coverage",
]


def handle_command_line_arguments():
    """Parse command line options"""
    parser = argparse.ArgumentParser(description="Use configuration for a package.")
    parser.add_argument(
        "path", type=pathlib.Path, help="path to the repository to be configured"
    )
    parser.add_argument(
        "--commit-msg",
        dest="commit_msg",
        metavar="MSG",
        help="Use MSG as commit message instead of an artificial one.",
    )
    parser.add_argument(
        "--no-commit",
        dest="commit",
        action="store_false",
        default=True,
        help="Prevent automatic committing of changes.",
    )
    parser.add_argument(
        "--push",
        dest="push",
        action="store_true",
        default=False,
        help="Push changes directly.",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=[
            "default",
        ],
        default="default",
        dest="type",
        help="type of the configuration to be used, see README.md. "
        "Only required when running on a repository for the first time.",
    )
    parser.add_argument(
        "--tox",
        dest="run_tox",
        action="store_true",
        default=False,
        help="Whether to run tox after configuring the repository.",
    )
    parser.add_argument(
        "--branch",
        dest="branch_name",
        default=None,
        help="Define a git branch name to be used for the changes. "
        "If not given it is constructed automatically and includes "
        'the configuration type. Use "current" to update the current branch.',
    )
    parser.add_argument(
        "--track",
        dest="track_package",
        action="store_true",
        default=False,
        help="Whether to add the package being configured in packages.txt.",
    )

    args = parser.parse_args()
    return args


def get_test_matrix(test_matrix):
    """Get test matrix from options or use the default one.

    If no test matrix is given, use the default one.
    If a test matrix is given, we check if one of the Plone versions has '*'
    as Python versions, which means "all supported versions".
    We then replace the '*' with the default list of supported Python versions.

    Example input:

        {
            "6.2": ["*"],
            "6.1": ["3.11"],
        }

    Example output:

        {
            "6.2": ["3.13", "3.12", "3.11", "3.10"],
            "6.1": ["3.11"],
        }
    """
    if not test_matrix:
        return TOX_TEST_MATRIX
    result = {}
    for plone_version, python_versions in test_matrix.items():
        if python_versions == ["*"]:
            result[plone_version] = TOX_TEST_MATRIX[plone_version]
        else:
            result[plone_version] = python_versions
    return result


class PackageConfiguration:

    def __init__(self, args):
        self.args = args
        self.path = args.path.absolute()
        self.meta_cfg = {}

        if not (self.path / ".git").exists():
            raise ValueError(
                f"{self.path!r} does not point to a git clone of a repository!"
            )

        self.meta_cfg = self._read_meta_configuration()
        self.meta_cfg["meta"]["template"] = self.config_type
        self.meta_cfg["meta"]["commit-id"] = self._get_version()

        with change_dir(self.path):
            server_url = git_server_url()
        self.is_github = "github" in server_url
        self.is_gitlab = "gitlab" in server_url
        if not self.is_github and not self.is_gitlab:
            self.print_warning(
                "CI configuration",
                "The repository is not hosted in github nor in gitlab, no CI configuration will be done!",
            )

    def _get_version(self):
        return version("plone.meta")

    def _read_meta_configuration(self):
        """Read and update meta configuration"""
        meta_toml_path = self.path / ".meta.toml"
        if meta_toml_path.exists():
            with open(meta_toml_path, "rb") as meta_f:
                meta_cfg = tomlkit.load(meta_f)
            meta_cfg = collections.defaultdict(dict, **meta_cfg)
        else:
            meta_cfg = collections.defaultdict(dict)
        return meta_cfg

    @cached_property
    def config_type(self):
        value = self.meta_cfg["meta"].get("template") or self.args.type
        if value is None:
            raise ValueError(
                "Configuration type not set. Please use `--type` to select it."
            )
        return value

    @cached_property
    def config_type_path(self):
        return pathlib.Path(__file__).parent / self.config_type

    @cached_property
    def default_path(self):
        return pathlib.Path(__file__).parent / "default"

    @cached_property
    def jinja_env(self):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader([self.config_type_path, self.default_path]),
            variable_start_string="%(",
            variable_end_string=")s",
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @cached_property
    def branch_name(self):
        return get_branch_name(self.args.branch_name, self.config_type)

    def _add_project_to_config_type_list(self):
        """Add the current project to packages.txt if it is not there"""
        with open(self.config_type_path / "packages.txt") as f:
            known_packages = f.read().splitlines()

        if self.path.name in known_packages:
            print(
                f"{self.path.name} is already configured "
                "for this config type, updating."
            )
            return
        print(f"{self.path.name} is not yet configured for this config type, adding.")
        with open(self.config_type_path / "packages.txt", "a") as f:
            f.write(f"{self.path.name}\n")

    def cfg_option(self, section, name=None, default=DEFAULT):
        """Read a value from `self.meta_cfg`, default to `[]` if not existing."""
        if default == DEFAULT:
            default = []
        if name is None:
            # Get the entire section.
            return self.meta_cfg[section]
        return self.meta_cfg[section].get(name, default)

    def _get_options_for(self, section, names):
        """Get all given named options from a given section"""
        options = {}
        for name in names:
            options[name] = self.cfg_option(section, name, "")
        return options

    def _test_cfg(self):
        """Setup testing configuration."""
        options = self._get_options_for("tox", ("test_runner", "test_path"))
        path = options.get("test_path")
        if not path:
            if (self.path / "tests").exists():
                path = "/tests"
            elif (self.path / "src").exists():
                path = "/src"
            else:
                path = ""
        options["test_path"] = path
        runner = options.get("test_runner", "zope.testrunner")
        options["test_runner"] = runner
        return options

    def warn_on_setup_cfg(self):
        """Warn if setup.cfg has sections that we define in other files"""
        setup_file = pathlib.Path(self.path / "setup.cfg")
        if not setup_file.exists():
            return
        content = setup_file.read_text()
        sections_outside = ("check-manifest", "flake8", "bdist_wheel")
        prefix = "setup.cfg cleanup"
        print()
        for section_name in sections_outside:
            if f"[{section_name}]" in content:
                self.print_warning(prefix, f"please remove [{section_name}] section")

    def print_warning(self, prefix, message):
        print(f"*** {prefix}: {message}\n")

    def editorconfig(self):
        options = self._get_options_for("editorconfig", ("extra_lines",))
        return self.copy_with_meta(
            "editorconfig.j2", self.path / ".editorconfig", **options
        )

    def gitignore(self):
        options = self._get_options_for("gitignore", ("extra_lines",))
        return self.copy_with_meta("gitignore.j2", self.path / ".gitignore", **options)

    def pre_commit_config(self):
        options = self._get_options_for(
            "pre_commit",
            (
                "zpretty_extra_lines",
                "codespell_extra_lines",
                "flake8_extra_lines",
                "extra_lines",
                "i18ndude_extra_lines",
            ),
        )

        return self.copy_with_meta(
            "pre-commit-config.yaml.j2",
            self.path / ".pre-commit-config.yaml",
            **options,
        )

    def pyproject_toml(self):
        files = []

        options = self._get_options_for(
            "pyproject",
            (
                "codespell_ignores",
                "codespell_skip",
                "dependencies_ignores",
                "dependencies_mappings",
                "check_manifest_ignores",
                "towncrier_issue_format",
                "towncrier_extra_lines",
                "isort_extra_lines",
                "black_extra_lines",
                "check_manifest_extra_lines",
                "extra_lines",
            ),
        )

        options["changes_extension"] = "rst"
        if (self.path / "CHANGES.md").exists():
            options["changes_extension"] = "md"

        options["news_folder_exists"] = False
        news = self.path / "news"
        if news.exists():
            options["news_folder_exists"] = True
            if options["changes_extension"] == "md":
                destination = news / ".changelog_template.jinja"
                shutil.copy(
                    self.config_type_path / "changelog_template.jinja", destination
                )
                files.append(destination)
            else:
                # only add the `.gitkeep` file if there is no jinja template
                gitkeep = news / ".gitkeep"
                gitkeep.touch(exist_ok=True)

        else:
            self.print_warning(
                "towncrier",
                "If you want to use Towncrier, you have to create a 'news/' folder manually.",
            )

        filename = self.copy_with_meta(
            "pyproject.toml.j2",
            **options,
        )
        files.append(filename)
        return files

    def tox(self):
        options = self._get_options_for(
            "tox",
            (
                "constrain_package_deps",
                "constraints_files",
                "envlist_lines",
                "testenv_options",
                "use_mxdev",
                "config_lines",
                "test_deps_additional",
                "test_extras",
                "test_environment_variables",
                "extra_lines",
                "use_pytest_plone",
                "package_name",
                "test_matrix",
            ),
        )
        use_mxdev = options.get("use_mxdev", False)
        options.update(self._test_cfg())
        options["package_name"] = options.get("package_name") or self.path.name
        options["news_folder_exists"] = (self.path / "news").exists()

        options["prime_robotframework"] = self._detect_robotframework()

        if not options["constrain_package_deps"]:
            options["constrain_package_deps"] = "false" if use_mxdev else "true"

        if options["use_pytest_plone"] is not False:
            # Default is '', so turn it into True
            options["use_pytest_plone"] = True

        options.update(self._handle_constraints_files(options))
        options["plone_envlist_lines"] = self._handle_testing_matrix(
            options["test_matrix"]
        )
        return self.copy_with_meta("tox.ini.j2", **options)

    def _handle_constraints_files(self, options):
        if options.get("use_mxdev", False):
            constraints = single_constraints = f"-c {MXDEV_CONSTRAINTS}"
        else:
            constraints = options["constraints_files"]
            test_matrix = get_test_matrix(options.get("test_matrix"))
            plone_versions = list(test_matrix.keys())

            single_constraints = f"-c https://dist.plone.org/release/{plone_versions[0]}-dev/constraints.txt"
            if constraints:
                first_plone_version = list(constraints.keys())[0]
                single_constraints = f"-c {constraints[first_plone_version]}"
                if len(test_matrix.keys()) != len(constraints.keys()):
                    raise ValueError(
                        "`constraints_files` and `test_matrix` need to provide the same Plone versions."
                        f"They provide {list(constraints.keys())} and {list(test_matrix.keys())} respectively."
                    )

            lines = []
            for plone_version in plone_versions:
                no_dot = plone_version.replace(".", "")
                url = f"https://dist.plone.org/release/{plone_version}-dev/constraints.txt"
                if constraints:
                    url = constraints[plone_version]
                lines.append(f"plone{no_dot}: -c {url}")
            constraints = "\n    ".join(lines)
        return {
            "constraints_file": constraints,
            "single_constraints_file": single_constraints,
        }

    def _normalized_python_version(self, python_version):
        """Return a normalized python version string.

        3.x -> py3.x
        `pypy3.x`  -> `pypy3.x`, so be careful that we don't get `pypypy3.x`.
        """
        if python_version.startswith("py"):
            return python_version
        return f"py{python_version}"

    def _no_dot_python_version(self, python_version):
        """Return a normalized python version string without dots.

        3.x -> py3x
        `pypy3.x`  -> `pypy3x`, so be careful that we don't get `pypypy3x`.
        """
        return self._normalized_python_version(python_version).replace(".", "")

    def _handle_testing_matrix(self, test_matrix):
        """Generate the tox environments matrix of Python and Plone versions to test

        Either `options` provides a dictionary like:
        {
          'PLONE_VERSION_1': [LIST_OF_PYTHON_VERSIONS],
          'PLONE_VERSION_2': [LIST_OF_PYTHON_VERSIONS],
        }

        Or the default `TOX_TEST_MATRIX` is used.
        """
        lines = []
        matrix = get_test_matrix(test_matrix)
        for plone_version, python_versions in matrix.items():
            no_dot_plone = plone_version.replace(".", "")
            for python_version in python_versions:
                no_dot_python = self._no_dot_python_version(python_version)
                lines.append(f"{no_dot_python}-plone{no_dot_plone}")
        return "\n    ".join(lines)

    def _detect_robotframework(self):
        """Dynamically find out if robotframework is used in the package.

        We look at the dependencies, as we expect the dependency checker
        to make it easy for us.
        """
        try_files = (
            self.path / "setup.py",
            self.path / "pyproject.toml",
        )
        for file_obj in try_files:
            if file_obj.exists():
                text = file_obj.read_text()
                if "plone.app.robotframework" in text:
                    return True
        return False

    def news_entry(self):
        news = self.path / "news"

        if not news.exists():
            return

        if self.args.branch_name == "current":
            print("Updating current branch, so I do not add a news entry.")
            return

        destination = self.path / "news" / "+meta.internal"
        with open(destination, "w") as f_:
            if (self.path / "CHANGES.md").exists():
                f_.write("Update configuration files @plone")
            else:
                f_.write("Update configuration files.\n")
                f_.write("[plone devs]\n")

        return destination.relative_to(self.path)

    def gha_workflows(self):
        if not self.is_github:
            return []
        github_folder = self.path / ".github"
        workflows_folder = github_folder / "workflows"
        workflows_folder.mkdir(parents=True, exist_ok=True)
        destination = workflows_folder / "meta.yml"
        options = self._get_options_for(
            "github",
            (
                "env",
                "ref",
                "jobs",
                "os_dependencies",
                "extra_lines",
                "extra_lines_after_os_dependencies",
            ),
        )
        if not options.get("ref"):
            options["ref"] = GHA_DEFAULT_REF
        if not options.get("jobs"):
            options["jobs"] = GHA_DEFAULT_JOBS
        meta_file = self.copy_with_meta(
            "meta.yml.j2", destination=destination, **options
        )
        dependabot = self.copy_with_meta(
            "dependabot.yml", destination=github_folder / "dependabot.yml"
        )

        if (self.path / "dependabot.yml").exists():
            self.print_warning(
                "CI configuration",
                "A `dependabot.yml` file at the top-level was found, please remove it",
            )

        options["gh_config_lines"] = self.handle_gh_actions()
        testing_file = self.copy_with_meta(
            "test-matrix.yml.j2",
            destination=workflows_folder / "test-matrix.yml",
            **options,
        )

        return [meta_file, dependabot, testing_file]

    def handle_gh_actions(self):
        options = self._get_options_for("tox", ("test_matrix",))
        test_matrix = get_test_matrix(options.get("test_matrix"))
        combinations = []
        for plone_version, python_versions in test_matrix.items():
            no_dot_plone = plone_version.replace(".", "")
            # Only test the lowest and highest Python version for a given Plone
            # version.  But always include any PyPy versions in the list.
            pypy_versions = [v for v in python_versions if v.startswith("pypy")]
            standard_versions = [v for v in python_versions if not v.startswith("pypy")]
            selected_versions = {standard_versions[0], standard_versions[-1]}
            if pypy_versions:
                selected_versions.update(pypy_versions)
            sorted_versions = sorted(selected_versions, reverse=True)
            for py_version in sorted_versions:
                normalized_python = self._normalized_python_version(py_version)
                no_dot_python = self._no_dot_python_version(normalized_python)
                combinations.append(
                    f'["{py_version}", "{plone_version} on {normalized_python}", "{no_dot_python}-plone{no_dot_plone}"]'
                )
        return "\n        - ".join(combinations)

    def gitlab_ci(self):
        if not self.is_gitlab:
            return []
        options = self._get_options_for(
            "gitlab",
            (
                "custom_images",
                "os_dependencies",
                "extra_lines",
                "jobs",
            ),
        )
        options.update(self._gitlab_testing_matrix(options["custom_images"]))
        options["destination"] = self.path / ".gitlab-ci.yml"
        if not options.get("jobs"):
            options["jobs"] = GITLAB_DEFAULT_JOBS
        return self.copy_with_meta("gitlab-ci.yml.j2", **options)

    def _gitlab_testing_matrix(self, custom_images):
        options = self._get_options_for("tox", ("test_matrix",))
        test_matrix = get_test_matrix(options.get("test_matrix"))
        combinations = []
        image = ""
        for plone_version, python_versions in test_matrix.items():
            no_dot_plone = plone_version.replace(".", "")
            top_bottom_versions = {python_versions[0], python_versions[-1]}
            sorted_versions = sorted(top_bottom_versions, reverse=True)
            for py_version in sorted_versions:
                no_dot_python = self._no_dot_python_version(py_version)
                image = DOCKER_IMAGES.get(py_version)
                if custom_images:
                    image = custom_images.get(py_version)
                if not image:
                    raise ValueError(
                        f"There is no Docker image defined for Python {py_version}. "
                        "Either provide it in the `custom_images` option or report an issue to `plone.meta`."
                    )

                combinations.append((image, f"{no_dot_python}-plone{no_dot_plone}"))
        return {
            "testing_matrix": combinations,
            "custom_image": image,
        }

    def flake8(self):
        options = self._get_options_for("flake8", ("extra_lines",))
        destination = self.path / ".flake8"
        return self.copy_with_meta("flake8.j2", destination=destination, **options)

    def copy_with_meta(
        self, template_name, destination=None, meta_hint=META_HINT, **kw
    ):
        """Copy the source file to destination and a hint of origin.

        If kwargs are given they are used as template arguments.
        """
        template = self.jinja_env.get_template(template_name)
        rendered = template.render(config_type=self.config_type, **kw)
        meta_hint = meta_hint.format(config_type=self.config_type)
        if rendered.startswith("#!"):
            she_bang, _, body = rendered.partition("\n")
            content = "\n".join([she_bang, meta_hint, body])
        else:
            content = "\n".join([meta_hint, rendered])

        if destination is None:
            if template_name.endswith(".j2"):
                destination = self.path / template_name[:-3]  # remove `.j2`
            else:
                destination = self.path / template_name

        # Get rid of spaces on lines with only spaces, like happens in the generated
        # tox.ini
        content = re.sub(r"\n\ +\n", r"\n\n", content)

        # Get rid of empty lines at the end.
        content = content.strip() + "\n"
        with open(destination, "w") as f_:
            f_.write(content)

        return destination.relative_to(self.path)

    def remove_old_files(self):
        filenames = ("bootstrap.py", ".travis.yml")
        with change_dir(self.path):
            for filename in filenames:
                if pathlib.Path(filename).exists():
                    call("git", "rm", filename)

    def remove_toml_empty_sections(self):
        meta_cfg = {k: v for k, v in self.meta_cfg.items() if v}
        with change_dir(self.path):
            with open(".meta.toml", "w") as meta_f:
                meta_f.write(META_HINT.format(config_type=self.config_type))
                meta_f.write("\n")
                tomlkit.dump(meta_cfg, meta_f)

    def run_tox(self):
        with change_dir(self.path) as cwd:
            tox_path = shutil.which("tox") or (pathlib.Path(cwd) / "bin" / "tox")
            call(tox_path, "-e", "format,lint")

    def validate_files(self, files_changed):
        """Ensure that files are not broken"""
        for file_obj in files_changed:
            if file_obj.suffix == ".toml":
                self._validate_toml(file_obj)
            elif file_obj.suffix in (".yaml", ".yml"):
                self._validate_yaml(file_obj)
            elif file_obj.suffix == ".ini" or file_obj.stem == ".flake8":
                self._validate_ini(file_obj)
            elif file_obj.stem == ".editorconfig":
                self._validate_editorconfig(file_obj)

    def _validate_toml(self, file_obj):
        """Validate files that are in TOML format"""
        with change_dir(self.path):

            with open(file_obj, "rb") as meta_f:
                data = tomlkit.load(meta_f)

            if self.path.stem == "pyproject":
                validator = validate_pyproject.api.Validator()
                validator(data)

    def _validate_yaml(self, file_obj):
        """Validate files that are in YAML format"""
        with change_dir(self.path):
            data = file_obj.read_text()
            _ = yaml.safe_load(data)

    def _validate_ini(self, file_obj):
        """Validate files that are in INI format"""
        config = configparser.ConfigParser()
        with change_dir(self.path):
            _ = config.read(file_obj)

    def _validate_editorconfig(self, file_obj):
        """Validate .editorconfig file"""
        with change_dir(self.path):
            editorconfig.get_properties(file_obj.resolve())

    @property
    def _commit_msg(self):
        return self.args.commit_msg or "Configuring with plone.meta"

    def commit_and_push(self, filenames):
        if not self.args.commit:
            return

        with change_dir(self.path):
            call("git", "add", *filenames)
            call("git", "commit", "-m", self._commit_msg)
            if self.args.push:
                call("git", "push", "--set-upstream", "origin", self.branch_name)

    @staticmethod
    def final_help_tips(updating):
        print()
        print("If everything went fine up to here:")
        if updating:
            print("Updated the previously created PR.")
        else:
            print("Create a PR, using the URL shown above.")

    def configure(self):
        if self.args.track_package:
            self._add_project_to_config_type_list()

        files_changed = [
            self.path / ".meta.toml",
        ]
        methods = (
            self.editorconfig,
            self.gitignore,
            self.pre_commit_config,
            self.pyproject_toml,
            self.tox,
            self.news_entry,
            self.flake8,
            self.gha_workflows,
            self.gitlab_ci,
        )
        for method in methods:
            files = method()
            if isinstance(files, list):
                files_changed.extend(files)
            else:
                files_changed.append(files)
        files_changed = [x for x in filter(None, files_changed)]

        self.remove_old_files()
        self.remove_toml_empty_sections()
        if self.args.run_tox:
            self.run_tox()

        with change_dir(self.path):
            updating = git_branch(self.branch_name)

        self.validate_files(files_changed)
        self.commit_and_push(files_changed)
        self.warn_on_setup_cfg()
        self.final_help_tips(updating)


def main():
    args = handle_command_line_arguments()

    package = PackageConfiguration(args)
    package.configure()
