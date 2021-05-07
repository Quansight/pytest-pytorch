import importlib
import pathlib
import sys

import pytest

from .utils import Config, make_parametrization, make_params


def make_standard_collection_parametrization():
    def make_file_config(test_cases):
        selection = set()
        for test_case in test_cases:
            selection.update(test_case.collect())
        return Config(
            selection=selection,
        )

    def make_test_case_configs(test_cases):
        return [
            Config(
                new_cmds=test_case.new_cmds,
                legacy_cmds=test_case.legacy_cmds,
                selection=test_case.collect(),
            )
            for test_case in test_cases
        ]

    def make_test_case_functions_configs(test_cases):
        return [
            Config(
                new_cmds=test_case_function.new_cmds,
                legacy_cmds=test_case_function.legacy_cmds,
                selection=test_case_function.collect(),
            )
            for test_case in test_cases
            for test_case_function in test_case.functions
        ]

    params = []
    assets = pathlib.Path(__file__).parent / "assets"
    sys.path.insert(0, str(assets))
    modules = sys.modules.copy()
    try:
        for test_file in assets.iterdir():
            module = test_file.stem
            if not test_file.name.startswith("test"):
                continue

            try:
                test_module = importlib.import_module(module)
                spy = test_module.__spy__
            except Exception:
                continue

            params.extend(
                make_params(
                    make_file_config(spy.test_cases),
                    *make_test_case_configs(spy.test_cases),
                    *make_test_case_functions_configs(spy.test_cases),
                    file=test_file.name,
                )
            )
    finally:
        sys.path.remove(str(assets))
        sys.modules = modules

    return pytest.mark.parametrize(Config.PARAM_NAMES, params)


@make_standard_collection_parametrization()
def test_standard_collection(collect_tests, file, cmds, selection):
    collection = collect_tests(file, cmds)
    assert collection == selection


@make_parametrization(
    Config(
        new_cmds=("-k", "cpu"),
        legacy_cmds=("-k", "cpu"),
        selection=(
            "::TestFooCPU::test_bar_cpu",
            "::TestFooCPU::test_baz_cpu",
            "::TestSpamCPU::test_ham_cpu",
            "::TestSpamCPU::test_eggs_cpu",
            "::TestQuxCPU::test_quux_cpu",
        ),
    ),
    Config(
        new_cmds=("-k", "meta"),
        legacy_cmds=("-k", "meta"),
        selection=(
            "::TestFooMETA::test_bar_meta",
            "::TestFooMETA::test_baz_meta",
            "::TestSpamMETA::test_ham_meta",
            "::TestSpamMETA::test_eggs_meta",
        ),
    ),
    file="test_device.py",
)
def test_devices(collect_tests, file, cmds, selection):
    collection = collect_tests(file, cmds)
    assert collection == selection


@make_parametrization(
    Config(
        new_cmds=("-k", "float16"),
        legacy_cmds=("-k", "float16"),
        selection=(
            "::TestFooCPU::test_bar_cpu_float16",
            "::TestFooCPU::test_bar_cpu_float16",
        ),
    ),
    Config(
        new_cmds=("-k", "int32"),
        legacy_cmds=("-k", "int32"),
        selection=(
            "::TestFooCPU::test_bar_cpu_int32",
            "::TestFooCPU::test_bar_cpu_int32",
        ),
    ),
    file="test_dtype.py",
)
def test_dtypes(collect_tests, file, cmds, selection):
    collection = collect_tests(file, cmds)
    assert collection == selection


@make_parametrization(
    Config(
        new_cmds=("-k", "add"),
        legacy_cmds=("-k", "add"),
        selection=(
            "::TestFooCPU::test_bar_add_cpu_float32",
            "::TestFooCPU::test_bar_add_with_alpha_cpu_float32",
        ),
    ),
    Config(
        new_cmds=("-k", "sub"),
        legacy_cmds=("-k", "sub"),
        selection=(
            "::TestFooCPU::test_bar_sub_cpu_float32",
            "::TestFooCPU::test_bar_sub_with_alpha_cpu_float32",
        ),
    ),
    file="test_op_infos.py",
)
def test_op_infos(collect_tests, file, cmds, selection):
    collection = collect_tests(file, cmds)
    assert collection == selection


@make_parametrization(
    Config(
        selection=(
            "::TestFoo::test_baz",
            "::TestFooBar::test_baz",
            "::TestSpam::test_ham",
            "::TestSpam::test_ham_eggs",
        ),
    ),
    Config(
        new_cmds="::TestFoo",
        legacy_cmds=("-k", "TestFoo and not TestFooBar"),
        selection=("::TestFoo::test_baz",),
    ),
    Config(
        new_cmds="::TestFooBar",
        legacy_cmds=("-k", "TestFooBar"),
        selection=("::TestFooBar::test_baz",),
    ),
    Config(
        new_cmds="::TestSpam::test_ham",
        legacy_cmds=("-k", "TestSpam and test_ham and not test_ham_eggs"),
        selection=("::TestSpam::test_ham",),
    ),
    Config(
        new_cmds="::TestSpam::test_ham_eggs",
        legacy_cmds=("-k", "TestSpam and test_ham_eggs"),
        selection=("::TestSpam::test_ham_eggs",),
    ),
    file="test_nested_names.py",
)
def test_nested_names(collect_tests, file, cmds, selection):
    collection = collect_tests(file, cmds)
    assert collection == selection
