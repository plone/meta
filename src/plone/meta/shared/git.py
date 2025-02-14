from .call import call
from importlib.metadata import version


def get_commit_id():
    """Return the first 8 digits of the commit id of this repository."""
    return call(
        "git", "rev-parse", "--short=8", "HEAD", capture_output=True
    ).stdout.strip()


def get_branch_name(override, config_type):
    """Get the default branch name but prefer override if not empty.

    The commit ID is based on the meta repository.
    """
    if override == "current":
        # Note: can be empty if not on a branch.
        override = call(
            "git", "branch", "--show-current", capture_output=True
        ).stdout.splitlines()[0]

    meta_version = version("plone.meta")
    return override or f"config-with-{config_type}-template-{meta_version}"


def git_branch(branch_name) -> bool:
    """Switch to existing or create new branch.

    Return `True` if updating.
    """
    branches = call(
        "git", "branch", "--format", "%(refname:short)", capture_output=True
    ).stdout.splitlines()
    if branch_name in branches:
        call("git", "checkout", branch_name)
        updating = True
    else:
        call("git", "checkout", "-b", branch_name)
        updating = False
    return updating


def git_server_url():
    """Return the repository URL"""
    output = call("git", "remote", "get-url", "origin", capture_output=True)
    url = output.stdout.splitlines()[0]
    return url
