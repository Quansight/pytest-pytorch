import pytest


@pytest.mark.parametrize("option", ["--disable-pytest-pytorch"])
def test_disable_pytest_pytorch(testdir, option):
    result = testdir.runpytest("--help")
    assert option in "\n".join(result.outlines)
