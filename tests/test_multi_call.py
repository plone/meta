from unittest.mock import patch


class TestMultiCallMain:
    @patch("plone.meta.multi_call.call")
    def test_clones_missing_repo(self, mock_call_fn, tmp_path):
        script = tmp_path / "my_script.py"
        script.write_text("print('hello')")
        packages_txt = tmp_path / "packages.txt"
        packages_txt.write_text("test-package\n")
        clones = tmp_path / "clones"
        clones.mkdir()

        with patch(
            "sys.argv",
            ["multi-call", str(script), str(packages_txt), str(clones)],
        ):
            from plone.meta.multi_call import main

            main()

        # Should clone then run script
        calls = mock_call_fn.call_args_list
        clone_call = [c for c in calls if "clone" in str(c)]
        assert len(clone_call) > 0

    @patch("plone.meta.multi_call.call")
    def test_updates_existing_repo(self, mock_call_fn, tmp_path):
        script = tmp_path / "my_script.py"
        script.write_text("print('hello')")
        packages_txt = tmp_path / "packages.txt"
        packages_txt.write_text("test-package\n")
        clones = tmp_path / "clones"
        clones.mkdir()
        (clones / "test-package").mkdir()

        with patch(
            "sys.argv",
            ["multi-call", str(script), str(packages_txt), str(clones)],
        ):
            from plone.meta.multi_call import main

            main()

        # Should stash, checkout master, pull
        calls = [str(c) for c in mock_call_fn.call_args_list]
        stash_calls = [c for c in calls if "stash" in c]
        assert len(stash_calls) > 0
