from plone.meta.config_package import get_test_matrix
from plone.meta.config_package import TOX_TEST_MATRIX

import pytest


@pytest.mark.parametrize(
    "input_matrix,expected",
    [
        pytest.param(None, TOX_TEST_MATRIX, id="none-returns-default"),
        pytest.param({}, TOX_TEST_MATRIX, id="empty-dict-returns-default"),
        pytest.param(
            {"6.2": ["*"]},
            {"6.2": TOX_TEST_MATRIX["6.2"]},
            id="wildcard-expands",
        ),
        pytest.param(
            {"6.2": ["3.13", "3.12"]},
            {"6.2": ["3.13", "3.12"]},
            id="explicit-versions-preserved",
        ),
    ],
)
def test_get_test_matrix(input_matrix, expected):
    assert get_test_matrix(input_matrix) == expected


def test_get_test_matrix_mixed_wildcard_and_explicit():
    result = get_test_matrix({"6.2": ["*"], "6.1": ["3.11"]})
    assert result["6.2"] == TOX_TEST_MATRIX["6.2"]
    assert result["6.1"] == ["3.11"]
