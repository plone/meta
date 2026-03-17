from unittest.mock import patch

import argparse
import pytest
import tomlkit


@pytest.fixture
def mock_git_repo(tmp_path):
    """Create a minimal fake git repo directory structure."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    return tmp_path


@pytest.fixture
def meta_toml_factory(mock_git_repo):
    """Factory fixture to create .meta.toml files with custom content."""

    def _create(config_dict=None):
        if config_dict is None:
            config_dict = {"meta": {"template": "default", "commit-id": "test1234"}}
        meta_toml = mock_git_repo / ".meta.toml"
        with open(meta_toml, "w") as f:
            tomlkit.dump(config_dict, f)
        return mock_git_repo

    return _create


@pytest.fixture
def mock_args(mock_git_repo):
    """Create a mock args namespace for PackageConfiguration."""
    return argparse.Namespace(
        path=mock_git_repo,
        commit_msg=None,
        commit=False,
        push=False,
        type="default",
        run_tox=False,
        branch_name=None,
        track_package=False,
    )


@pytest.fixture
def pyproject_toml(mock_git_repo):
    """Create an empty pyproject.toml"""

    def _create():
        toml_path = mock_git_repo / "pyproject.toml"
        toml_path.touch()

    return _create


@pytest.fixture
def package_config(pyproject_toml, meta_toml_factory, mock_args):
    """Create a PackageConfiguration with mocked subprocess calls."""
    from plone.meta.config_package import PackageConfiguration

    meta_toml_factory()  # creates default .meta.toml
    pyproject_toml()  # creates an empty pyproject.toml
    with (
        patch(
            "plone.meta.config_package.git_server_url",
            return_value="https://github.com/plone/test-package",
        ),
        patch(
            "plone.meta.config_package.version",
            return_value="2.4.0",
        ),
    ):
        config = PackageConfiguration(mock_args)
    return config
