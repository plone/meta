from plone.meta.config_package import PackageConfiguration
from unittest.mock import patch

import argparse
import pytest


class TestPackageConfigurationInit:
    def test_raises_without_git_dir(self, tmp_path):
        args = argparse.Namespace(
            path=tmp_path,
            commit_msg=None,
            commit=False,
            push=False,
            type="default",
            run_tox=False,
            branch_name=None,
            track_package=False,
        )
        with pytest.raises(ValueError, match="does not point to a git clone"):
            PackageConfiguration(args)

    def test_reads_meta_toml(self, meta_toml_factory, mock_args):
        meta_toml_factory({"meta": {"template": "default", "commit-id": "abc"}})
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://github.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        assert config.meta_cfg["meta"]["template"] == "default"

    def test_creates_empty_meta_cfg_without_meta_toml(self, mock_git_repo, mock_args):
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://github.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        # meta_cfg should still have meta section (set by __init__)
        assert config.meta_cfg["meta"]["template"] == "default"

    def test_detects_github(self, meta_toml_factory, mock_args):
        meta_toml_factory()
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://github.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        assert config.is_github is True
        assert config.is_gitlab is False

    def test_detects_gitlab(self, meta_toml_factory, mock_args):
        meta_toml_factory()
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://gitlab.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        assert config.is_github is False
        assert config.is_gitlab is True

    def test_neither_github_nor_gitlab(self, meta_toml_factory, mock_args):
        meta_toml_factory()
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://bitbucket.org/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        assert config.is_github is False
        assert config.is_gitlab is False


class TestConfigType:
    def test_from_meta_toml(self, package_config):
        assert package_config.config_type == "default"

    def test_from_args_when_meta_toml_empty(self, mock_git_repo, mock_args):
        mock_args.type = "default"
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://github.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            config = PackageConfiguration(mock_args)
        assert config.config_type == "default"

    def test_raises_when_neither(self, mock_git_repo):
        args = argparse.Namespace(
            path=mock_git_repo,
            commit_msg=None,
            commit=False,
            push=False,
            type=None,
            run_tox=False,
            branch_name=None,
            track_package=False,
        )
        with (
            patch(
                "plone.meta.config_package.git_server_url",
                return_value="https://github.com/plone/test",
            ),
            patch("plone.meta.config_package.version", return_value="2.4.0"),
        ):
            with pytest.raises(ValueError, match="Configuration type not set"):
                PackageConfiguration(args)
