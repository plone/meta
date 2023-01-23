#!/usr/bin/env python3
from functools import cached_property
from shared.call import call
from shared.git import get_branch_name
from shared.git import get_commit_id
from shared.git import git_branch
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
# https://github.com/plone/meta/tree/master/config/{config_type}"""
META_HINT_MARKDOWN = """\
<!--
Generated from:
https://github.com/plone/meta/tree/master/config/{config_type}
--> """
FUTURE_PYTHON_VERSION = "3.12.0-alpha.2"
DEFAULT = object()


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
        '--branch',
        dest='branch_name',
        default=None,
        help='Define a git branch name to be used for the changes. '
        'If not given it is constructed automatically and includes '
        'the configuration type')

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
        else:
            print(f'{self.path.name} is not yet configured '
                  'for this config type, adding.')
            with open(self.config_type_path / 'packages.txt', 'a') as f:
                f.write(f'{self.path.name}\n')

    def setup_cfg(self):
        """Copy setup.cfg file to the package being configured."""
        extra_check_manifest_ignores = self.cfg_option(
            'check-manifest', 'additional-ignores')

        return self.copy_with_meta(
            'setup.cfg.j2',
            self.path / 'setup.cfg',
            self.config_type,
            additional_check_manifest_ignores=extra_check_manifest_ignores,
        )

    def cfg_option(self, section, name, default=DEFAULT):
        """Read a value from `self.meta_cfg`, default to `[]` if not existing.
        """
        if default == DEFAULT:
            default = []
        return self.meta_cfg[section].get(name, default)

    def linting_yml(self):
        workflows = self.path / '.github' / 'workflows'
        workflows.mkdir(parents=True, exist_ok=True)
        return self.copy_with_meta('linting.yml.j2', workflows / 'linting.yml')

    def editorconfig(self):
        return self.copy_with_meta('editorconfig', self.path / '.editorconfig')

    def lint_requirements(self):
        return self.copy_with_meta('lint-requirements.txt.j2')

    def pyproject_toml(self):
        return self.copy_with_meta('pyproject.toml.j2')

    def tox(self):
        return self.copy_with_meta('tox.ini.j2')

    def news_entry(self):
        news = self.path / 'news'
        news.mkdir(parents=True, exist_ok=True)

        destination = self.path / f'1.internal.{get_commit_id}'
        with open(destination, 'w') as f_:
            f_.write('Update configuration files\n')
            f_.write('[plone devs]')

        return destination.name

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

        with open(destination, 'w') as f_:
            f_.write(content)

        return destination.relative_to(self.path)

    def remove_old_files(self):
        filenames = ('bootstrap.py', '.travis.yml')
        with change_dir(self.path):
            for filename in filenames:
                if pathlib.Path(filename).exists():
                    call('git', 'rm', 'filename')

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
            self.editorconfig(),
            self.lint_requirements(),
            self.linting_yml(),
            self.pyproject_toml(),
            self.setup_cfg(),
            self.tox(),
            self.news_entry(),
        ]

        self.remove_old_files()
        self.remove_toml_empty_sections()
        self.run_tox()

        with change_dir(self.path):
            updating = git_branch(self.branch_name)

        self.commit_and_push(files_changed)
        self.final_help_tips(updating)


def main():
    args = handle_command_line_arguments()

    package = PackageConfiguration(args)
    package.configure()


main()
