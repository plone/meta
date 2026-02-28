from plone.meta.re_enable_actions import run_workflow
from unittest.mock import MagicMock
from unittest.mock import patch


class TestRunWorkflow:
    @patch("plone.meta.re_enable_actions.call")
    def test_success(self, mock_call):
        mock_call.return_value = MagicMock(returncode=0)
        result = run_workflow("https://github.com/plone", "plone", "test-repo")
        assert result is True

    @patch("plone.meta.re_enable_actions.call")
    def test_failure(self, mock_call):
        mock_call.return_value = MagicMock(returncode=1)
        result = run_workflow("https://github.com/plone", "plone", "test-repo")
        assert result is False


class TestReEnableActionsMain:
    @patch("plone.meta.re_enable_actions.call")
    @patch("plone.meta.re_enable_actions.list_packages")
    def test_enables_disabled_workflow(self, mock_list, mock_call):
        mock_list.return_value = ["test-repo"]
        # First call: workflow list; second: enable; third: run
        mock_call.side_effect = [
            MagicMock(stdout="Meta\tactive\tdisabled_inactivity\t12345"),
            MagicMock(returncode=0),  # enable
            MagicMock(returncode=0),  # run
        ]
        with patch("sys.argv", ["re-enable-actions"]):
            from plone.meta.re_enable_actions import main

            main()
        # Should have called enable
        calls_str = [str(c) for c in mock_call.call_args_list]
        enable_calls = [c for c in calls_str if "enable" in c]
        assert len(enable_calls) > 0

    @patch("plone.meta.re_enable_actions.call")
    @patch("plone.meta.re_enable_actions.list_packages")
    def test_skips_already_enabled(self, mock_list, mock_call):
        mock_list.return_value = ["test-repo"]
        mock_call.return_value = MagicMock(stdout="Meta\tactive\t\t12345")
        with patch("sys.argv", ["re-enable-actions"]):
            from plone.meta.re_enable_actions import main

            main()
        # Only one call (the list), no enable
        assert mock_call.call_count == 1
