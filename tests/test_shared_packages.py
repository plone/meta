from plone.meta.shared.packages import list_packages


class TestListPackages:
    def test_returns_package_names(self, tmp_path):
        f = tmp_path / "packages.txt"
        f.write_text("pkg1\npkg2\npkg3\n")
        assert list_packages(f) == ["pkg1", "pkg2", "pkg3"]

    def test_filters_comments(self, tmp_path):
        f = tmp_path / "packages.txt"
        f.write_text("# comment\npkg1\n# another\npkg2\n")
        assert list_packages(f) == ["pkg1", "pkg2"]

    def test_filters_blank_lines(self, tmp_path):
        f = tmp_path / "packages.txt"
        f.write_text("pkg1\n\n\npkg2\n")
        assert list_packages(f) == ["pkg1", "pkg2"]

    def test_empty_file(self, tmp_path):
        f = tmp_path / "packages.txt"
        f.write_text("")
        assert list_packages(f) == []

    def test_comments_and_blanks_mixed(self, tmp_path):
        f = tmp_path / "packages.txt"
        f.write_text("# Header\n\npkg1\n# Note\npkg2\n\npkg3\n")
        assert list_packages(f) == ["pkg1", "pkg2", "pkg3"]
