from plone.meta.shared.call import abort
from plone.meta.shared.call import call
from unittest.mock import patch

import pytest
import subprocess


class TestCall:
    @patch("plone.meta.shared.call.subprocess.run")
    def test_success_returns_result(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "hello"], returncode=0, stdout="hello\n", stderr=""
        )
        result = call("echo", "hello")
        assert result.returncode == 0
        assert result.stdout == "hello\n"

    @patch("plone.meta.shared.call.subprocess.run")
    def test_passes_args_to_subprocess(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "status"], returncode=0
        )
        call("git", "status")
        mock_run.assert_called_once_with(
            ("git", "status"), capture_output=False, text=True, cwd=None
        )

    @patch("plone.meta.shared.call.subprocess.run")
    def test_capture_output(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["cmd"], returncode=0, stdout="out"
        )
        call("cmd", capture_output=True)
        mock_run.assert_called_once_with(
            ("cmd",), capture_output=True, text=True, cwd=None
        )

    @patch("plone.meta.shared.call.subprocess.run")
    def test_cwd_kwarg(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(args=["cmd"], returncode=0)
        call("cmd", cwd="/tmp")
        mock_run.assert_called_once_with(
            ("cmd",), capture_output=False, text=True, cwd="/tmp"
        )

    @patch("plone.meta.shared.call.abort")
    @patch("plone.meta.shared.call.subprocess.run")
    def test_failure_calls_abort(self, mock_run, mock_abort):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["cmd"], returncode=1, stdout="", stderr="error"
        )
        call("cmd")
        mock_abort.assert_called_once_with(1)

    @patch("plone.meta.shared.call.abort")
    @patch("plone.meta.shared.call.subprocess.run")
    def test_allowed_return_codes(self, mock_run, mock_abort):
        mock_run.return_value = subprocess.CompletedProcess(args=["cmd"], returncode=1)
        call("cmd", allowed_return_codes=(0, 1))
        mock_abort.assert_not_called()

    @patch("plone.meta.shared.call.abort")
    @patch("plone.meta.shared.call.subprocess.run")
    def test_default_only_zero_allowed(self, mock_run, mock_abort):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["cmd"], returncode=2, stdout="", stderr=""
        )
        call("cmd")
        mock_abort.assert_called_once_with(2)


class TestAbort:
    @patch("builtins.input", return_value="n")
    def test_exits_on_no(self, mock_input):
        with pytest.raises(SystemExit) as exc_info:
            abort(42)
        assert exc_info.value.code == 42

    @patch("builtins.input", return_value="y")
    def test_continues_on_yes(self, mock_input):
        abort(42)  # should not raise
