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

    def test_creates_files(self, package_config):
        package_config.is_gitlab = True
        result = package_config.gitlab_ci()
        assert result
        assert (package_config.path / ".gitlab-ci.yml").exists()


class TestMinimalConfigFiles:
    def test_editorconfig(self, package_config):
        result = package_config.editorconfig()
        assert result
        assert (package_config.path / ".editorconfig").exists()

    def test_gitignore(self, package_config):
        result = package_config.gitignore()
        assert result
        assert (package_config.path / ".gitignore").exists()

    def test_precommit(self, package_config):
        result = package_config.pre_commit_config()
        assert result
        assert (package_config.path / ".pre-commit-config.yaml").exists()

    def test_tox(self, package_config):
        result = package_config.tox()
        assert result
        assert (package_config.path / "tox.ini").exists()

    def test_flake8(self, package_config):
        result = package_config.flake8()
        assert result
        assert (package_config.path / ".flake8").exists()


class TestPyproject:
    def test_minimal_files(self, package_config):
        result = package_config.pyproject_toml()
        assert len(result) == 1
        assert (package_config.path / "pyproject.toml").exists()

    def test_if_news_folder_exists(self, package_config):
        (package_config.path / "news").mkdir(parents=True, exist_ok=True)
        result = package_config.pyproject_toml()
        assert len(result) == 1
        assert (package_config.path / "news" / ".gitkeep").exists()

    def test_if_changes_md_exists(self, package_config):
        (package_config.path / "news").mkdir(parents=True, exist_ok=True)
        (package_config.path / "CHANGES.md").touch()
        result = package_config.pyproject_toml()
        assert len(result) == 2
        assert (package_config.path / "news" / ".changelog_template.jinja").exists()


class TestSetuptoolsUpperBound:
    @pytest.mark.parametrize(["is_native", "expected"], [[True, "82"], [False, "83"]])
    def test_native_namespace(self, package_config, is_native, expected):
        if is_native:
            folder = package_config.path / "src" / "plone"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "__init__.py").write_text("\ndeclare_namespace(__name__)\n")
        result = package_config._setuptools_upper_bound()
        assert result == expected


class TestMinimalPythonVersion:
    @pytest.mark.parametrize(
        ["matrix", "output"],
        [
            [None, "3.10"],
            [{"6.1": ["*"]}, "3.10"],
            [{"6.2": ["*"]}, "3.10"],
            [{"6.2": ["3.13"]}, "3.13"],
            [{"6.2": ["3.13"], "6.1": ["3.9"]}, "3.9"],
            [{"6.2": ["3.13", "3.10"], "5.2": ["3.8"]}, "3.8"],
            [{"6.2": ["pypy3.10", "3.11"]}, "3.11"],
        ],
    )
    def test_python_version(self, package_config, matrix, output):
        if matrix:
            package_config.meta_cfg["tox"]["test_matrix"] = matrix

        result = package_config._minimal_python_version()
        assert result == output


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
