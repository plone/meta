from unittest.mock import patch

import pytest


class TestCommitAndPush:
    @patch("plone.meta.config_package.call")
    def test_no_commit_when_commit_false(self, mock_call_fn, package_config):
        package_config.args.commit = False
        package_config.commit_and_push(["file1.txt"])
        mock_call_fn.assert_not_called()

    @patch("plone.meta.config_package.call")
    def test_commits_files(self, mock_call_fn, package_config):
        package_config.args.commit = True
        package_config.args.push = False
        package_config.commit_and_push(["file1.txt", "file2.txt"])
        assert mock_call_fn.call_count == 2  # git add + git commit

    @patch("plone.meta.config_package.call")
    def test_commits_and_pushes(self, mock_call_fn, package_config):
        package_config.args.commit = True
        package_config.args.push = True
        package_config.commit_and_push(["file1.txt"])
        assert mock_call_fn.call_count == 3  # git add + git commit + git push


class TestGhaWorkflows:
    def test_returns_empty_for_non_github(self, package_config):
        package_config.is_github = False
        assert package_config.gha_workflows() == []

    def test_creates_workflow_files(self, package_config):
        result = package_config.gha_workflows()
        assert len(result) >= 2  # at least meta.yml and dependabot.yml
        workflows_dir = package_config.path / ".github" / "workflows"
        assert (workflows_dir / "meta.yml").exists()
        assert (package_config.path / ".github" / "dependabot.yml").exists()


class TestGitlabCi:
    def test_returns_empty_for_non_gitlab(self, package_config):
        package_config.is_gitlab = False
        assert package_config.gitlab_ci() == []


class TestHandleGhActions:
    def test_returns_empty_when_disabled(self, package_config):
        package_config.meta_cfg["tox"]["use_test_matrix"] = False
        result = package_config.handle_gh_actions()
        assert result == []

    def test_default_matrix_generates_combinations(self, package_config):
        result = package_config.handle_gh_actions()
        assert "plone62" in result
        assert "plone61" in result


class TestGitlabTestingMatrix:
    def test_default_matrix(self, package_config):
        result = package_config._gitlab_testing_matrix("")
        assert "testing_matrix" in result
        assert len(result["testing_matrix"]) > 0

    def test_missing_image_raises(self, package_config):
        package_config.meta_cfg["tox"]["test_matrix"] = {"6.2": ["9.99"]}
        with pytest.raises(ValueError, match="no Docker image"):
            package_config._gitlab_testing_matrix({"9.99": None})
