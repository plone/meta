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
        help='Prevent automatic committing of changes. Implies --no-push.')
    parser.add_argument(
        '--no-push',
        dest='push',
        action='store_false',
        default=True,
        help='Prevent direct push.')
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
    def distribution_path(self):
        paths = (
            (self.path / 'src'),
            (self.path / 'plone'),
        )
        for path in paths:
            if path.exists():
                return path.parts[-1]
        raise ValueError('The repository does not have a `src` or a `plone` folder!')

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
        extra_flake8_config = self.cfg_option(
            'flake8', 'additional-config')
        extra_check_manifest_ignores = self.cfg_option(
            'check-manifest', 'additional-ignores')
        check_manifest_ignore_bad_ideas = self.cfg_option(
            'check-manifest', 'ignore-bad-ideas')
        isort_known_third_party = self.cfg_option(
            'isort', 'known_third_party',
            default=' six, docutils, pkg_resources')
        isort_known_zope = self.cfg_option('isort', 'known_zope', default='')
        isort_known_first_party = self.cfg_option(
            'isort', 'known_first_party', default='')
        isort_known_local_folder = self.meta_cfg['isort'].get(
            'known_local_folder', '')
        for var in (
            'isort_known_third_party',
            'isort_known_zope',
            'isort_known_first_party',
        ):
            if locals()[var]:
                # Avoid whitespace at end of line if empty:
                locals()[var] = ' ' + locals()[var]

        zest_releaser_options = self.meta_cfg['zest-releaser'].get(
            'options', [])
        if self.config_type == 'c-code':
            zest_releaser_options.append('create-wheel = no')

        self.copy_with_meta(
            'setup.cfg.j2',
            self.path / 'setup.cfg',
            self.config_type,
            additional_flake8_config=extra_flake8_config,
            additional_check_manifest_ignores=extra_check_manifest_ignores,
            check_manifest_ignore_bad_ideas=check_manifest_ignore_bad_ideas,
            isort_known_third_party=isort_known_third_party,
            isort_known_zope=isort_known_zope,
            isort_known_first_party=isort_known_first_party,
            isort_known_local_folder=isort_known_local_folder,
            zest_releaser_options=zest_releaser_options,
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

        self.copy_with_meta(
            'linting.yml.j2',
            workflows / 'linting.yml',
            self.config_type,
        )

    def editorconfig(self):
        self.copy_with_meta(
            'editorconfig',
            self.path / '.editorconfig',
            self.config_type
        )

    def lint_requirements(self):
        self.copy_with_meta(
            'lint-requirements.txt.j2',
            self.path / 'lint-requirements.txt',
            self.config_type
        )

    def pyproject_toml(self):
        self.copy_with_meta(
            'pyproject.toml.j2',
            self.path / 'pyproject.toml',
            self.config_type
        )

    def tox(self):
        self.copy_with_meta(
            'tox.ini.j2',
            self.path / 'tox.ini',
            self.config_type,
            dist_path=self.distribution_path
        )

    def copy_with_meta(
            self, template_name, destination, config_type,
            meta_hint=META_HINT, **kw):
        """Copy the source file to destination and a hint of origin.

        If kwargs are given they are used as template arguments.
        """
        template = self.jinja_env.get_template(template_name)
        rendered = template.render(config_type=config_type, **kw)
        meta_hint = meta_hint.format(config_type=config_type)
        if rendered.startswith('#!'):
            she_bang, _, body = rendered.partition('\n')
            content = '\n'.join([she_bang, meta_hint, body])
        else:
            content = '\n'.join([meta_hint, rendered])

        with open(destination, 'w') as f_:
            f_.write(content)

    def configure(self):
        self._add_project_to_config_type_list()

        self.editorconfig()
        self.lint_requirements()
        self.linting_yml()
        self.pyproject_toml()
        self.setup_cfg()
        self.tox()

        with change_dir(self.path) as cwd:
            if pathlib.Path('bootstrap.py').exists():
                call('git', 'rm', 'bootstrap.py')
            if pathlib.Path('.travis.yml').exists():
                call('git', 'rm', '.travis.yml')
            # Remove empty sections:
            meta_cfg = {k: v for k, v in self.meta_cfg.items() if v}
            with open('.meta.toml', 'w') as meta_f:
                meta_f.write(META_HINT.format(config_type=self.config_type))
                meta_f.write('\n')
                toml.dump(
                    meta_cfg, meta_f,
                    TomlArraySeparatorEncoderWithNewline(
                        separator=',\n   ', indent_first_line=True))

            tox_path = shutil.which('tox') or (
                pathlib.Path(cwd) / 'bin' / 'tox')
            call(tox_path, '-p', 'auto')

            updating = git_branch(self.branch_name)

            if self.args.commit:
                files = [
                    '.editorconfig',
                    'lint-requirements.txt',
                    '.github/workflows/linting.yml',
                    'pyproject.toml',
                    'setup.cfg',
                    '.meta.toml',
                    'tox.ini',
                ]
                call('git', 'add', *files)
                if self.args.commit_msg:
                    commit_msg = self.args.commit_msg
                else:
                    commit_msg = f'Configuring for {self.config_type}'
                call('git', 'commit', '-m', commit_msg)
                if self.args.push:
                    call('git', 'push', '--set-upstream',
                         'origin', self.branch_name)
            print()
            print('If everything went fine up to here:')
            if updating:
                print('Updated the previously created PR.')
            else:
                print('Create a PR, using the URL shown above.')


def main():
    args = handle_command_line_arguments()

    package = PackageConfiguration(args)
    package.configure()


main()
