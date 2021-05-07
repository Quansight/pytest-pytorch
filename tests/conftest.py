import pytest

pytest_plugins = ["pytester"]


@pytest.fixture
def collect_tests(testdir):
    def collect_tests_(file: str, cmds: str):
        testdir.copy_example(file)
        result = testdir.runpytest("--quiet", "--collect-only", *cmds)
        assert result.ret == pytest.ExitCode.OK

        collection = set()
        for line in result.outlines:
            if not line:
                break

            collection.add(line)

        return collection

    return collect_tests_
