import pytest


class TestCfgOption:
    def test_returns_section(self, package_config):
        package_config.meta_cfg["tox"]["test_runner"] = "pytest"
        result = package_config.cfg_option("tox")
        assert result["test_runner"] == "pytest"

    def test_returns_value(self, package_config):
        package_config.meta_cfg["tox"]["test_runner"] = "pytest"
        result = package_config.cfg_option("tox", "test_runner")
        assert result == "pytest"

    def test_returns_default(self, package_config):
        result = package_config.cfg_option("tox", "nonexistent")
        assert result == []

    def test_returns_custom_default(self, package_config):
        result = package_config.cfg_option("tox", "nonexistent", "custom")
        assert result == "custom"


class TestNormalizedPythonVersion:
    def test_plain(self, package_config):
        assert package_config._normalized_python_version("3.12") == "py3.12"

    def test_already_prefixed(self, package_config):
        assert package_config._normalized_python_version("py3.12") == "py3.12"

    def test_pypy(self, package_config):
        assert package_config._normalized_python_version("pypy3.10") == "pypy3.10"


class TestNoDotPythonVersion:
    def test_plain(self, package_config):
        assert package_config._no_dot_python_version("3.12") == "py312"

    def test_pypy(self, package_config):
        assert package_config._no_dot_python_version("pypy3.10") == "pypy310"


class TestMinimalPythonVersion:
    def test_mixed_versions_returns_semantic_minimum(self, package_config):
        """Versions like 3.10 should be correctly compared, not lexicographically."""
        package_config.meta_cfg["tox"]["test_matrix"] = {
            "6.2": ["3.13", "3.10"],
            "5.2": ["3.8"],
        }
        result = package_config._minimal_python_version()
        assert result == "3.8"

    def test_wildcard_matrix(self, package_config):
        """Wildcard should expand to default versions and find the minimum."""
        package_config.meta_cfg["tox"]["test_matrix"] = {"6.2": ["*"]}
        result = package_config._minimal_python_version()
        assert result == "3.10"

    def test_default_matrix(self, package_config):
        """Default matrix should return 3.10 as minimum."""
        result = package_config._minimal_python_version()
        assert result == "3.10"


class TestHandleTestingMatrix:
    def test_default_matrix(self, package_config):
        result = package_config._handle_testing_matrix(None)
        assert "py314-plone62" in result
        assert "py310-plone62" in result

    def test_custom_matrix(self, package_config):
        result = package_config._handle_testing_matrix({"6.2": ["3.13", "3.12"]})
        assert "py313-plone62" in result
        assert "py312-plone62" in result
        assert "py314" not in result


class TestHandleConstraintsFiles:
    def test_with_mxdev(self, package_config):
        options = {"use_mxdev": True, "use_test_matrix": True, "constraints_files": ""}
        result = package_config._handle_constraints_files(options)
        assert result["constraints_file"] == "-c constraints-mxdev.txt"
        assert result["single_constraints_file"] == "-c constraints-mxdev.txt"

    def test_without_test_matrix(self, package_config):
        options = {
            "use_mxdev": False,
            "use_test_matrix": False,
            "constraints_files": "",
        }
        result = package_config._handle_constraints_files(options)
        assert result["constraints_file"] == ""
        assert result["single_constraints_file"] == ""

    def test_default_urls(self, package_config):
        options = {
            "use_mxdev": False,
            "use_test_matrix": True,
            "constraints_files": "",
            "test_matrix": None,
        }
        result = package_config._handle_constraints_files(options)
        assert "dist.plone.org" in result["constraints_file"]
        assert "dist.plone.org" in result["single_constraints_file"]

    def test_mismatched_versions_raises(self, package_config):
        options = {
            "use_mxdev": False,
            "use_test_matrix": True,
            "constraints_files": {"6.2": "url1"},
            "test_matrix": {"6.2": ["3.13"], "6.1": ["3.12"]},
        }
        with pytest.raises(ValueError, match="same Plone versions"):
            package_config._handle_constraints_files(options)
