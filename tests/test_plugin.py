import pytest


class Config:
    def __init__(
        self,
        id,
        *,
        new_cmds,
        legacy_cmds=None,
        passed=0,
        skipped=0,
        failed=0,
        errors=0,
        xpassed=0,
        xfailed=0,
    ):
        self._id = id
        self._new_cmds = self._parse_cmds(new_cmds)
        self._legacy_cmds = self._parse_cmds(legacy_cmds or self._new_cmds)
        self._outcomes = dict(
            passed=passed,
            skipped=skipped,
            failed=failed,
            errors=errors,
            xpassed=xpassed,
            xfailed=xfailed,
        )

    @staticmethod
    def _parse_cmds(cmds):
        return (cmds,) if isinstance(cmds, str) else cmds

    @staticmethod
    def _amend_cmds(cmds, file):
        if not cmds or not cmds[0].startswith(":"):
            return (file, *cmds)
        else:
            return (file + cmds[0], *cmds[1:])

    def make_params(self, file):
        return (
            pytest.param(
                file,
                self._amend_cmds(self._new_cmds, file),
                self._outcomes,
                id=f"{self._id}-new",
            ),
            pytest.param(
                file,
                self._amend_cmds(self._legacy_cmds, file),
                self._outcomes,
                id=f"{self._id}-legacy",
            ),
        )


FILE = "test_device.py"
CONFIGS = [
    Config("*testcase-*test-*device", new_cmds=(), passed=3, skipped=2, failed=3),
    Config(
        "1testcase1-*test-*device",
        new_cmds="::TestFoo",
        legacy_cmds=("-k", "TestFoo"),
        passed=2,
        skipped=1,
        failed=1,
    ),
    Config(
        "1testcase2-*test-*device",
        new_cmds="::TestSpam",
        legacy_cmds=("-k", "TestSpam"),
        passed=1,
        skipped=1,
        failed=2,
    ),
    Config(
        "*testcase-*test-1device1",
        new_cmds=("-k", "meta"),
        legacy_cmds=("-k", "META"),
        passed=2,
        skipped=1,
        failed=1,
    ),
    Config(
        "*testcase-*test-1device2",
        new_cmds=("-k", "cpu"),
        legacy_cmds=("-k", "CPU"),
        passed=1,
        skipped=1,
        failed=2,
    ),
    Config(
        "1testcase-*test-1device1",
        new_cmds=("::TestFoo", "-k", "meta"),
        legacy_cmds="::TestFooMETA",
        passed=1,
        failed=1,
    ),
    Config(
        "1testcase-*test-1device2",
        new_cmds=("::TestFoo", "-k", "cpu"),
        legacy_cmds="::TestFooCPU",
        passed=1,
        skipped=1,
    ),
    Config(
        "1testcase-1test1-*device",
        new_cmds="::TestFoo::test_bar",
        legacy_cmds=("-k", "TestFoo and test_bar"),
        passed=1,
        failed=1,
    ),
    Config(
        "1testcase-1test2-*device",
        new_cmds="::TestFoo::test_baz",
        legacy_cmds=("-k", "TestFoo and test_baz"),
        passed=1,
        skipped=1,
    ),
    Config(
        "1testcase-1test-1device1",
        new_cmds=("::TestFoo::test_bar", "-k", "meta"),
        legacy_cmds="::TestFooMETA::test_bar_meta",
        failed=1,
    ),
    Config(
        "1testcase-1test-1device2",
        new_cmds=("::TestFoo::test_bar", "-k", "cpu"),
        legacy_cmds="::TestFooCPU::test_bar_cpu",
        passed=1,
    ),
]


def make_params(file, configs):
    return pytest.mark.parametrize(
        ("file", "cmds", "outcomes"),
        [param for config in configs for param in config.make_params(file)],
    )


@make_params(FILE, CONFIGS)
def test_collection(testdir, file, cmds, outcomes):
    testdir.copy_example(file)
    result = testdir.runpytest(*cmds)
    result.assert_outcomes(**outcomes)
