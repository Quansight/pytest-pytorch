import inspect
import re
import unittest.mock
import warnings

from _pytest.unittest import TestCaseFunction, UnitTestCase

try:
    from torch.testing._internal.common_utils import TestCase as TestCaseTemplate

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

    warnings.warn(
        "Disabling the `pytest-pytorch` plugin, because 'torch' could not be imported."
    )


class TemplatedName(str):
    def __new__(cls, name, template_name):
        self = super().__new__(cls, name)
        self._template_name = template_name
        return self

    def __eq__(self, other):
        exact_match = str.__eq__(self, other)
        if exact_match:
            return True

        if not self._template_name:
            return False

        return str.__eq__(self._template_name, other)

    def __hash__(self):
        return super().__hash__()


class TemplatedTestCaseFunction(TestCaseFunction):
    _TEMPLATE_NAME_PATTERN = re.compile(r"def (?P<template_name>test_\w+)\(")

    @classmethod
    def _extract_template_name(cls, callobj):
        if not callobj:
            return None

        match = cls._TEMPLATE_NAME_PATTERN.search(inspect.getsource(callobj))
        if not match:
            return None

        return match.group("template_name")

    @classmethod
    def from_parent(cls, parent, *, name, callobj, **kw):
        return super().from_parent(
            parent, name=TemplatedName(name, cls._extract_template_name(callobj)), **kw
        )


class TemplatedTestCase(UnitTestCase):
    @classmethod
    def _extract_template_name(cls, name, obj):
        if not obj:
            return None

        if not hasattr(obj, "device_type"):
            return None

        return name[: -len(obj.device_type)]

    @classmethod
    def from_parent(cls, parent, *, name, obj=None):
        return super().from_parent(
            parent,
            name=TemplatedName(name, cls._extract_template_name(name, obj)),
            obj=obj,
        )

    def collect(self):
        # Yes, this is a bad practice. Unfortunately, there is no other option to
        # inject our custom 'TestCaseFunction' without duplicating everything in
        # 'UnitTestCase.collect()'
        with unittest.mock.patch(
            "_pytest.unittest.TestCaseFunction", new=TemplatedTestCaseFunction
        ):
            yield from super().collect()


def pytest_addoption(parser, pluginmanager):
    parser.addoption(
        "--disable-pytest-pytorch",
        action="store_true",
        help="Disable the `pytest-pytorch` plugin",
    )
    return None


def pytest_pycollect_makeitem(collector, name, obj):
    if not TORCH_AVAILABLE:
        return None

    if collector.config.getoption("disable_pytest_pytorch"):
        return None

    try:
        if not issubclass(obj, TestCaseTemplate) or obj is TestCaseTemplate:
            return None
    except Exception:
        return None

    return TemplatedTestCase.from_parent(collector, name=name, obj=obj)
