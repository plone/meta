from plone.meta.config_package import META_HINT

import pathlib


class TestTestCfg:
    def test_defaults_to_empty_test_runner(self, package_config):
        # _get_options_for returns "" for unset options; the .get fallback
        # only applies when the key is missing, not when it's ""
        result = package_config._test_cfg()
        assert result["test_runner"] == ""

    def test_explicit_test_runner(self, package_config):
        package_config.meta_cfg["tox"]["test_runner"] = "zope.testrunner"
        result = package_config._test_cfg()
        assert result["test_runner"] == "zope.testrunner"

    def test_detects_tests_dir(self, package_config):
        (package_config.path / "tests").mkdir()
        result = package_config._test_cfg()
        assert result["test_path"] == "/tests"

    def test_detects_src_dir(self, package_config):
        (package_config.path / "src").mkdir()
        result = package_config._test_cfg()
        assert result["test_path"] == "/src"

    def test_empty_path_fallback(self, package_config):
        result = package_config._test_cfg()
        assert result["test_path"] == ""


class TestDetectRobotframework:
    def test_found_in_setup_py(self, package_config):
        setup_py = package_config.path / "setup.py"
        setup_py.write_text("install_requires=['plone.app.robotframework']")
        assert package_config._detect_robotframework() is True

    def test_not_found(self, package_config):
        assert package_config._detect_robotframework() is False

    def test_found_in_pyproject_toml(self, package_config):
        pyproject = package_config.path / "pyproject.toml"
        pyproject.write_text('dependencies = ["plone.app.robotframework"]')
        assert package_config._detect_robotframework() is True


class TestCopyWithMeta:
    def test_prepends_meta_hint(self, package_config):
        dest = package_config.path / ".editorconfig"
        package_config.copy_with_meta(
            "editorconfig.j2", destination=dest, extra_lines=""
        )
        content = dest.read_text()
        expected_hint = META_HINT.format(config_type="default")
        assert content.startswith(expected_hint)

    def test_default_destination_removes_j2(self, package_config):
        # "editorconfig.j2"[:-3] = "editorconfig" (no leading dot)
        result = package_config.copy_with_meta("editorconfig.j2", extra_lines="")
        assert result == pathlib.Path("editorconfig")
        assert (package_config.path / "editorconfig").exists()

    def test_custom_destination(self, package_config):
        dest = package_config.path / "custom.conf"
        package_config.copy_with_meta(
            "editorconfig.j2", destination=dest, extra_lines=""
        )
        assert dest.exists()

    def test_strips_trailing_whitespace_lines(self, package_config):
        dest = package_config.path / ".editorconfig"
        package_config.copy_with_meta(
            "editorconfig.j2", destination=dest, extra_lines=""
        )
        content = dest.read_text()
        for line in content.split("\n"):
            if line:
                assert not line.endswith(" "), f"Trailing space on line: {line!r}"


class TestNewsEntry:
    def test_creates_file_with_markdown(self, package_config):
        (package_config.path / "news").mkdir()
        (package_config.path / "CHANGES.md").write_text("# Changes")
        result = package_config.news_entry()
        assert result == pathlib.Path("news/+meta.internal")
        content = (package_config.path / "news" / "+meta.internal").read_text()
        assert content == "Update configuration files @plone\n"

    def test_creates_file_with_rst(self, package_config):
        (package_config.path / "news").mkdir()
        (package_config.path / "CHANGES.rst").write_text("Changes\n=======")
        package_config.news_entry()
        content = (package_config.path / "news" / "+meta.internal").read_text()
        assert "Update configuration files." in content
        assert "[plone devs]" in content

    def test_no_news_dir(self, package_config):
        result = package_config.news_entry()
        assert result is None

    def test_current_branch_skips(self, package_config):
        (package_config.path / "news").mkdir()
        package_config.args.branch_name = "current"
        result = package_config.news_entry()
        assert result is None


class TestValidateFiles:
    def test_validate_toml(self, package_config):
        toml_file = package_config.path / "test.toml"
        toml_file.write_text('[section]\nkey = "value"\n')
        # Should not raise
        package_config.validate_files([toml_file])

    def test_validate_yaml(self, package_config):
        yaml_file = package_config.path / "test.yml"
        yaml_file.write_text("key: value\n")
        package_config.validate_files([yaml_file])

    def test_validate_ini(self, package_config):
        ini_file = package_config.path / "test.ini"
        ini_file.write_text("[section]\nkey = value\n")
        package_config.validate_files([ini_file])
