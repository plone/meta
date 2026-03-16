from plone.meta.shared.git import get_branch_name
from plone.meta.shared.git import get_commit_id
from plone.meta.shared.git import git_branch
from plone.meta.shared.git import git_server_url
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


class TestGetCommitId:
    @patch("plone.meta.shared.git.call")
    def test_returns_stripped_stdout(self, mock_call_fn):
        mock_call_fn.return_value = MagicMock(stdout="abc12345\n")
        result = get_commit_id()
        assert result == "abc12345"

    @patch("plone.meta.shared.git.call")
    def test_calls_git_rev_parse(self, mock_call_fn):
        mock_call_fn.return_value = MagicMock(stdout="abc12345\n")
        get_commit_id()
        mock_call_fn.assert_called_once_with(
            "git", "rev-parse", "--short=8", "HEAD", capture_output=True
        )


class TestGetBranchName:
    @pytest.mark.parametrize(
        ("override", "expected"),
        [
            ("my-branch", "my-branch"),
            ("", "config-with-default-template-2.4.0"),
            (None, "config-with-default-template-2.4.0"),
        ],
    )
    @patch("plone.meta.shared.git.version", return_value="2.4.0")
    @patch("plone.meta.shared.git.call")
    def test_override_variants(self, mock_call_fn, mock_version, override, expected):
        result = get_branch_name(override, "default")
        assert result == expected
        mock_call_fn.assert_not_called()

    @pytest.mark.parametrize(
        ("stdout", "expected"),
        [
            ("feature-branch\n", "feature-branch"),
            ("\n", "config-with-default-template-2.4.0"),
        ],
    )
    @patch("plone.meta.shared.git.version", return_value="2.4.0")
    @patch("plone.meta.shared.git.call")
    def test_current_override_variants(
        self, mock_call_fn, mock_version, stdout, expected
    ):
        mock_call_fn.return_value = MagicMock(stdout=stdout)
        result = get_branch_name("current", "default")
        assert result == expected
        mock_call_fn.assert_called_once_with(
            "git", "branch", "--show-current", capture_output=True
        )


class TestGitBranch:
    @patch("plone.meta.shared.git.call")
    def test_existing_branch_checks_out(self, mock_call_fn):
        mock_call_fn.return_value = MagicMock(stdout="main\nmy-branch\nother\n")
        result = git_branch("my-branch")
        assert result is True
        assert mock_call_fn.call_count == 2
        mock_call_fn.assert_any_call(
            "git", "branch", "--format", "%(refname:short)", capture_output=True
        )
        mock_call_fn.assert_any_call("git", "checkout", "my-branch")

    @patch("plone.meta.shared.git.call")
    def test_new_branch_creates(self, mock_call_fn):
        mock_call_fn.return_value = MagicMock(stdout="main\nother\n")
        result = git_branch("new-branch")
        assert result is False
        mock_call_fn.assert_any_call("git", "checkout", "-b", "new-branch")


class TestGitServerUrl:
    @patch("plone.meta.shared.git.call")
    def test_returns_first_line(self, mock_call_fn):
        mock_call_fn.return_value = MagicMock(
            stdout="https://github.com/plone/test.git\n"
        )
        result = git_server_url()
        assert result == "https://github.com/plone/test.git"
