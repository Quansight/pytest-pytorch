from typing import Collection, Set, Tuple

from torch.testing._internal.common_utils import TestCase as PyTorchTestCase


class TestCase:
    def __init__(
        self,
        template_test_case: PyTorchTestCase,
        instantiated_test_cases: Collection[PyTorchTestCase],
    ):
        self.template_test_case_name = template_test_case.__name__

        functions = []
        for template_function_name in dir(template_test_case):
            if not template_function_name.startswith("test_"):
                continue

            instantiated_test_cases_with_functions_names = [
                (test_case.__name__, function_name)
                for test_case in instantiated_test_cases
                for function_name in dir(test_case)
                if function_name.startswith(template_function_name)
            ]

            functions.append(
                TestCaseFunction(
                    template_test_case_name=self.template_test_case_name,
                    template_function_name=template_function_name,
                    instantiated_test_cases_with_functions_names=instantiated_test_cases_with_functions_names,
                )
            )
        self.functions = functions

    @property
    def new_cmds(self) -> str:
        return f"::{self.template_test_case_name}"

    @property
    def legacy_cmds(self) -> Tuple[str, ...]:
        return ("-k", f"{self.template_test_case_name}")

    def collect(self) -> Set[str]:
        collection = set()
        for function in self.functions:
            collection.update(function.collect())
        return collection


class TestCaseFunction:
    def __init__(
        self,
        *,
        template_test_case_name: str,
        template_function_name: str,
        instantiated_test_cases_with_functions_names: Collection[Tuple[str, str]],
    ) -> None:
        self._template_test_case_name = template_test_case_name
        self._template_function_name = template_function_name
        self._instantiated_test_cases_with_functions_names = (
            instantiated_test_cases_with_functions_names
        )

    @property
    def new_cmds(self) -> str:
        return f"::{self._template_test_case_name}::{self._template_function_name}"

    @property
    def legacy_cmds(self) -> Tuple[str, ...]:
        return (
            "-k",
            f"{self._template_test_case_name} and {self._template_function_name}",
        )

    def collect(self) -> Set[str]:
        return {
            f"::{test_case_name}::{function_name}"
            for test_case_name, function_name in self._instantiated_test_cases_with_functions_names
        }


class Spy:
    def __init__(self):
        self.test_cases = []

    def __call__(self, instantiate_device_type_tests):
        def wrapper(template_test_case, globals, *args, **kwargs):
            before = set(globals.keys())
            instantiate_device_type_tests(template_test_case, globals, *args, **kwargs)
            after = set(globals.keys())
            instantiated_test_cases = [globals[name] for name in (after - before)]

            self.test_cases.append(
                TestCase(template_test_case, instantiated_test_cases)
            )

        return wrapper
