from .utils import Config, make_params


@make_params(
    "test_device.py",
    Config(
        "*testcase-*test-*device",
        new_cmds=(),
        legacy_cmds=(),
        passed=3,
        skipped=2,
        failed=3,
    ),
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
)
def test_collection(testdir, file, cmds, outcomes):
    testdir.copy_example(file)
    result = testdir.runpytest(*cmds)
    result.assert_outcomes(**outcomes)
