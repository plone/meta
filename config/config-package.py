#!/usr/bin/env python3
from functools import cached_property
from shared.call import call
from shared.git import get_branch_name
from shared.git import get_commit_id
from shared.git import git_branch
from shared.git import git_server_url
from shared.path import change_dir
from shared.toml_encoder import TomlArraySeparatorEncoderWithNewline

import argparse
import collections
import jinja2
import pathlib
import shutil
import toml


META_HINT = """\
# Generated from:
# https://github.com/plone/meta/tree/master/config/{config_type}
# See the inline comments on how to expand/tweak this configuration file"""
META_HINT_MARKDOWN = """\
<!--
Generated from:
https://github.com/plone/meta/tree/master/config/{config_type}
See the inline comments on how to expand/tweak this configuration file
--> """
DEFAULT = object()

PLONE_CONSTRAINTS_FILE = 'https://dist.plone.org/release/6.0-dev/constraints.txt'

DOCKER_IMAGE = 'python:3.11-bullseye'

GHA_DEFAULT_BRANCH = "master"
GHA_DEFAULT_JOBS = [
    "qa",
    "test",
    "coverage",
    "dependencies",
    "release-ready",
    "circular"
]


def handle_command_line_arguments():
    """Parse command line options"""
    parser = argparse.ArgumentParser(
        description='Use configuration for a package.')
    parser.add_argument(
        'path', type=pathlib.Path,
        help='path to the repository to be configured')
    parser.add_argument(
        '--commit-msg',
        dest='commit_msg',
        metavar='MSG',
        help='Use MSG as commit message instead of an artificial one.')
    parser.add_argument(
        '--no-commit',
        dest='commit',
        action='store_false',
        default=True,
        help='Prevent automatic committing of changes.')
    parser.add_argument(
        '--push',
        dest='push',
        action='store_true',
        default=False,
        help='Push changes directly.')
    parser.add_argument(
        '-t', '--type',
        choices=[
            'default',
        ],
        default='default',
        dest='type',
        help='type of the configuration to be used, see README.rst. '
        'Only required when running on a repository for the first time.')
    parser.add_argument(
        '--tox',
        dest='run_tox',
        action='store_true',
        default=False,
        help='Whether to run tox after configuring the repository.')
    parser.add_argument(
        '--branch',
        dest='branch_name',
        default=None,
        help='Define a git branch name to be used for the changes. '
        'If not given it is constructed automatically and includes '
        'the configuration type. Use "current" to update the current branch.')

    args = parser.parse_args()
    return args


class PackageConfiguration:

    def __init__(self, args):
        self.args = args
        self.path = args.path.absolute()
        self.meta_cfg = {}

        if not (self.path / '.git').exists():
            raise ValueError(
                f'{self.path!r} does not point '
                'to a git clone of a repository!')

        self.meta_cfg = self._read_meta_configuration()
        self.meta_cfg['meta']['template'] = self.config_type
        self.meta_cfg['meta']['commit-id'] = get_commit_id()

        with change_dir(self.path):
            server_url = git_server_url()
        self.is_github = 'github' in server_url
        self.is_gitlab = 'gitlab' in server_url
        if not self.is_github and not self.is_gitlab:
            self.print_warning(
                'CI configuration',
                'The repository is not hosted in github nor in gitlab, no CI configuration will be done!'
            )

    def _read_meta_configuration(self):
        """Read and update meta configuration"""
        meta_toml_path = self.path / '.meta.toml'
        if meta_toml_path.exists():
            meta_cfg = toml.load(meta_toml_path)
            meta_cfg = collections.defaultdict(dict, **meta_cfg)
        else:
            meta_cfg = collections.defaultdict(dict)
        return meta_cfg

    @cached_property
    def config_type(self):
        value = self.meta_cfg['meta'].get('template') or self.args.type
        if value is None:
            raise ValueError(
                'Configuration type not set. '
                'Please use `--type` to select it.')
        return value

    @cached_property
    def config_type_path(self):
        return pathlib.Path(__file__).parent / self.config_type

    @cached_property
    def default_path(self):
        return pathlib.Path(__file__).parent / 'default'

    @cached_property
    def jinja_env(self):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                [self.config_type_path, self.default_path]),
            variable_start_string='%(',
            variable_end_string=')s',
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @cached_property
    def branch_name(self):
        return get_branch_name(self.args.branch_name, self.config_type)

    def _add_project_to_config_type_list(self):
        """Add the current project to packages.txt if it is not there"""
        with open(self.config_type_path / 'packages.txt') as f:
            known_packages = f.read().splitlines()

        if self.path.name in known_packages:
            print(f'{self.path.name} is already configured '
                  'for this config type, updating.')
            return
        print(f'{self.path.name} is not yet configured '
              'for this config type, adding.')
        with open(self.config_type_path / 'packages.txt', 'a') as f:
            f.write(f'{self.path.name}\n')

    def cfg_option(self, section, name=None, default=DEFAULT):
        """Read a value from `self.meta_cfg`, default to `[]` if not existing.
        """
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
            options[name] = self.cfg_option(section, name, '')
        return options

    def _test_cfg(self):
        """Setup testing configuration."""
        options = self._get_options_for(
            'tox',
            ('test_runner', 'test_path')
        )
        path = options.get("test_path")
        if not path:
            if (self.path / 'tests').exists():
                path = "/tests"
            elif (self.path / 'src').exists():
                path = "/src"
            else:
                path = ""
        options["test_path"] = path
        runner = options.get("test_runner", "zope.testrunner")
        options["test_runner"] = runner
        return options

    def warn_on_setup_cfg(self):
        """Warn if setup.cfg has sections that we define in other files"""
        setup_file = pathlib.Path( self.path / 'setup.cfg')
        if not setup_file.exists():
            return
        content = setup_file.read_text()
        sections_outside = ('check-manifest', 'flake8', 'bdist_wheel')
        prefix = 'setup.cfg cleanup'
        print()
        for section_name in sections_outside:
            if f'[{section_name}]' in content:
                self.print_warning(prefix, f'please remove [{section_name}] section')

    def print_warning(self, prefix, message):
        print(f'*** {prefix}" {message}\n')

    def editorconfig(self):
        options = self._get_options_for(
            'editorconfig',
            ('extra_lines', )
        )
        return self.copy_with_meta(
            'editorconfig.j2',
            self.path / '.editorconfig',
            **options
        )

    def gitignore(self):
        options = self._get_options_for(
            'gitignore',
            ('extra_lines', )
        )
        return self.copy_with_meta(
            'gitignore.j2',
            self.path / '.gitignore',
            **options
        )

    def pre_commit_config(self):
        options = self._get_options_for(
            'pre_commit',
            (
                'zpretty_extra_lines',
                'codespell_extra_lines',
                'flake8_extra_lines',
                'extra_lines',
            )
        )

        return self.copy_with_meta(
            'pre-commit-config.yaml.j2',
            self.path / '.pre-commit-config.yaml',
            **options
        )

    def pyproject_toml(self):
        files = []
        changes_extension = 'rst'
        if (self.path / 'CHANGES.md').exists():
            changes_extension = 'md'
            destination = self.path / 'news' / '.changelog_template.jinja'
            shutil.copy(
                self.config_type_path / 'changelog_template.jinja',
                destination
            )
            files.append(destination)

        options = self._get_options_for(
            'pyproject',
            (
                'codespell_ignores',
                'codespell_skip',
                'dependencies_ignores',
                'dependencies_mappings',
                'check_manifest_ignores',
                'towncrier_issue_format',
                'towncrier_extra_lines',
                'isort_extra_lines',
                'black_extra_lines',
                'extra_lines',
            )
        )

        filename = self.copy_with_meta(
            'pyproject.toml.j2',
            changes_extension=changes_extension,
            **options,
        )
        files.append(filename)
        return files

    def tox(self):
        options = self._get_options_for(
            'tox',
            (
                'constraints_file',
                'envlist_lines',
                'config_lines',
                'test_extras',
                'test_environment_variables',
                'extra_lines',
            )
        )
        options.update(self._test_cfg())
        options['package_name'] = self.path.name
        if not options['constraints_file']:
            options['constraints_file'] = PLONE_CONSTRAINTS_FILE
        return self.copy_with_meta(
            'tox.ini.j2',
            **options
        )

    def news_entry(self):
        if self.args.branch_name == 'current':
            print('Updating current branch, so I do not add a news entry.')
            return
        news = self.path / 'news'
        news.mkdir(parents=True, exist_ok=True)

        destination = self.path / 'news' / f'{get_commit_id()}.internal'
        with open(destination, 'w') as f_:
            f_.write('Update configuration files.\n')
            f_.write('[plone devs]\n')

        return destination.relative_to(self.path)

    def gha_workflows(self):
        if not self.is_github:
            return []
        folder = self.path / '.github' / 'workflows'
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / 'meta.yml'
        options = self._get_options_for(
            'github',
            (
                'branch',
                'jobs',
                'additional_jobs',
            )
        )
        options.update(self._test_cfg())
        if not options.get("branch"):
            options['branch'] = GHA_DEFAULT_BRANCH
        if not options.get("jobs"):
            options['jobs'] = GHA_DEFAULT_JOBS
        return self.copy_with_meta(
            'meta.yml.j2',
            destination=destination,
            **options
        )
        return self.copy_with_meta('meta.yml.j2', destination=destination)

    def gitlab_ci(self):
        if not self.is_gitlab:
            return []
        options = self._get_options_for('gitlab', ('custom_image', 'extra_lines', ))
        if not options['custom_image']:
            options['custom_image'] = DOCKER_IMAGE
        destination = self.path / '.gitlab-ci.yml'
        return self.copy_with_meta('gitlab-ci.yml.j2', destination=destination, **options)

    def flake8(self):
        options = self._get_options_for('flake8', ('extra_lines', ))
        destination = self.path / '.flake8'
        return self.copy_with_meta(
            'flake8.j2', destination=destination, **options
        )

    def copy_with_meta(
            self, template_name, destination=None,
            meta_hint=META_HINT, **kw):
        """Copy the source file to destination and a hint of origin.

        If kwargs are given they are used as template arguments.
        """
        template = self.jinja_env.get_template(template_name)
        rendered = template.render(config_type=self.config_type, **kw)
        meta_hint = meta_hint.format(config_type=self.config_type)
        if rendered.startswith('#!'):
            she_bang, _, body = rendered.partition('\n')
            content = '\n'.join([she_bang, meta_hint, body])
        else:
            content = '\n'.join([meta_hint, rendered])

        if destination is None:
            if template_name.endswith('.j2'):
                destination = self.path / template_name[:-3]  # remove `.j2`
            else:
                destination = self.path / template_name

        # Get rid of empty lines at the end.
        content = content.strip() + "\n"
        with open(destination, 'w') as f_:
            f_.write(content)

        return destination.relative_to(self.path)

    def remove_old_files(self):
        filenames = ('bootstrap.py', '.travis.yml')
        with change_dir(self.path):
            for filename in filenames:
                if pathlib.Path(filename).exists():
                    call('git', 'rm', filename)

    def remove_toml_empty_sections(self):
        meta_cfg = {k: v for k, v in self.meta_cfg.items() if v}
        with change_dir(self.path):
            with open('.meta.toml', 'w') as meta_f:
                meta_f.write(META_HINT.format(config_type=self.config_type))
                meta_f.write('\n')
                toml.dump(
                    meta_cfg, meta_f,
                    TomlArraySeparatorEncoderWithNewline(
                        separator=',\n   ', indent_first_line=True))

    def run_tox(self):
        with change_dir(self.path) as cwd:
            tox_path = shutil.which('tox') or (pathlib.Path(cwd) / 'bin' / 'tox')
            call(tox_path, '-e', 'format,lint')

    @property
    def _commit_msg(self):
        return self.args.commit_msg or 'Configuring with plone/meta'

    def commit_and_push(self, filenames):
        if not self.args.commit:
            return

        with change_dir(self.path):
            call('git', 'add', *filenames)
            call('git', 'commit', '-m', self._commit_msg)
            if self.args.push:
                call('git', 'push', '--set-upstream', 'origin', self.branch_name)

    @staticmethod
    def final_help_tips(updating):
        print()
        print('If everything went fine up to here:')
        if updating:
            print('Updated the previously created PR.')
        else:
            print('Create a PR, using the URL shown above.')

    def configure(self):
        self._add_project_to_config_type_list()

        files_changed = [
            self.path / '.meta.toml',
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
        files_changed = filter(None, files_changed)

        self.remove_old_files()
        self.remove_toml_empty_sections()
        if self.args.run_tox:
            self.run_tox()

        with change_dir(self.path):
            updating = git_branch(self.branch_name)

        self.commit_and_push(files_changed)
        self.warn_on_setup_cfg()
        self.final_help_tips(updating)


def main():
    args = handle_command_line_arguments()

    package = PackageConfiguration(args)
    package.configure()


main()
