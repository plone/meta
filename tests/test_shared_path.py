from plone.meta.shared.path import change_dir
from plone.meta.shared.path import path_factory

import argparse
import os
import pathlib
import pytest


class TestChangeDir:
    def test_changes_to_target(self, tmp_path):
        with change_dir(tmp_path):
            assert os.getcwd() == str(tmp_path)

    def test_restores_original_dir(self, tmp_path):
        original = os.getcwd()
        with change_dir(tmp_path):
            pass
        assert os.getcwd() == original

    def test_yields_original_cwd(self, tmp_path):
        original = os.getcwd()
        with change_dir(tmp_path) as old_cwd:
            assert old_cwd == original

    def test_restores_on_exception(self, tmp_path):
        original = os.getcwd()
        with pytest.raises(RuntimeError):
            with change_dir(tmp_path):
                raise RuntimeError("test error")
        assert os.getcwd() == original


class TestPathFactory:
    def test_returns_path_for_existing_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("content")
        factory = path_factory("test")
        result = factory(str(f))
        assert isinstance(result, pathlib.Path)
        assert result == f

    def test_raises_for_nonexistent_path(self):
        factory = path_factory("test")
        with pytest.raises(argparse.ArgumentTypeError, match="does not exist"):
            factory("/nonexistent/path")

    def test_validates_extension(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("content")
        py_file = tmp_path / "test.py"
        py_file.write_text("content")

        factory = path_factory("test", has_extension=".txt")
        assert factory(str(txt_file)) == txt_file
        with pytest.raises(argparse.ArgumentTypeError, match="extension"):
            factory(str(py_file))

    def test_validates_is_dir(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("content")

        factory = path_factory("test", is_dir=True)
        assert factory(str(tmp_path)) == tmp_path
        with pytest.raises(argparse.ArgumentTypeError, match="directory"):
            factory(str(f))
