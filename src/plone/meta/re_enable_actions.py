from .shared.call import call
from .shared.packages import list_packages
import argparse
import itertools
import pathlib


org = 'plone'
base_url = f'https://github.com/{org}'
base_path = pathlib.Path(__file__).parent
types = ['default']


def run_workflow(base_url, org, repo):
    """Manually start the tests.yml workflow of a repository."""
    result = call('gh', 'workflow', 'run', 'tests.yml', '-R', f'{org}/{repo}')
    if result.returncode != 0:
        print('To enable manually starting workflows clone the repository'
              ' and run config-package on it.')
        print('Command to clone:')
        print(f'git clone {base_url}/{repo}.git')
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Re-enable GitHub Actions for all repos in a packages.txt'
                    ' files.')
    parser.add_argument(
        '--force-run',
        help='Run workflow even it is already enabled.',
        action='store_true')

    args = parser.parse_args()

    repos = itertools.chain(
        *[list_packages(base_path / type / 'packages.txt')
          for type in types])


    for repo in repos:
        print(repo)
        wfs = call(
            'gh', 'workflow', 'list', '--all', '-R', f'{org}/{repo}',
            capture_output=True).stdout
        test_lines = [x for x in wfs.splitlines() if x.startswith('Meta')]
        if not test_lines:
            print('Meta is not in the workflows. Clone the repository'
                ' and run config-package on it.')
            print('Command to clone:')
            print(f'git clone {base_url}/{repo}.git')
            continue
        test_line = test_lines[0]
        if 'disabled_inactivity' not in test_line:
            print('    ☑️  already enabled')
            if args.force_run:
                run_workflow(base_url, org, repo)
            continue
        test_id = test_line.split()[-1]
        call('gh', 'workflow', 'enable', test_id, '-R', f'{org}/{repo}')
        if run_workflow(base_url, org, repo):
            print('    ✅ enabled')
