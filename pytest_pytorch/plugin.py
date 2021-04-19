import re
import unittest.mock
import warnings
from typing import Pattern

from _pytest.unittest import TestCaseFunction, UnitTestCase

try:
    from torch.testing._internal.common_device_type import get_device_type_test_bases
    from torch.testing._internal.common_utils import TestCase as PyTorchTestCaseTemplate

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

    warnings.warn(
        "Disabling the plugin 'pytest-pytorch', because 'torch' could not be imported."
    )

    def get_device_type_test_bases():
        return []

    class PyTorchTestCaseTemplate:
        pass


class PytestPyTorchInternalError(Exception):
    def __init__(self, msg):
        super().__init__(
            f"{msg}\n"
            f"This is an internal error of the pytest plugin 'pytest-pytorch'."
            f"If you encounter this during normal operation, please file an issue "
            f"https://github.com/Quansight/pytest-pytorch/issues."
        )


TEST_BASE_DEVICE_PATTERN = re.compile(r"(?P<device>\w*?)TestBase$")


def _get_devices():
    devices = []
    for test_base in get_device_type_test_bases():
        match = TEST_BASE_DEVICE_PATTERN.match(test_base.__name__)
        if not match:
            raise PytestPyTorchInternalError(
                f"Unable to extract device name from {test_base.__name__}"
            )

        devices.append(match.group("device"))

    return devices


DEVICES = _get_devices()


class TemplateName(str):
    _TEMPLATE_NAME_PATTERN: Pattern

    def __init__(self, _):
        super().__init__()
        match = self._TEMPLATE_NAME_PATTERN.match(self)
        if not match:
            raise PytestPyTorchInternalError(
                f"Unable to extract template name from {self}"
            )
        self._template_name = match.group("template_name")

    def __eq__(self, other):
        return str.__eq__(self, other) or str.__eq__(self._template_name, other)

    def __hash__(self) -> int:
        return super().__hash__()


class TestCaseFunctionTemplateName(TemplateName):
    _TEMPLATE_NAME_PATTERN = re.compile(
        fr"(?P<template_name>\w*?)_({'|'.join([device.lower() for device in DEVICES])})"
    )


class PyTorchTestCaseFunction(TestCaseFunction):
    @classmethod
    def from_parent(cls, parent, *, name, **kw):
        return super().from_parent(
            parent, name=TestCaseFunctionTemplateName(name), **kw
        )


class TestCaseTemplateName(TemplateName):
    _TEMPLATE_NAME_PATTERN = re.compile(
        fr"(?P<template_name>\w*?)({'|'.join([device.upper() for device in DEVICES])})"
    )


class PyTorchTestCase(UnitTestCase):
    @classmethod
    def from_parent(cls, parent, *, name, obj=None):
        return super().from_parent(parent, name=TestCaseTemplateName(name), obj=obj)

    def collect(self):
        # Yes, this is a bad practice. Unfortunately, there is no other option to
        # inject our custom 'TestCaseFunction' without duplicating everything in
        # 'UnitTestCase.collect()'
        with unittest.mock.patch(
            "_pytest.unittest.TestCaseFunction", new=PyTorchTestCaseFunction
        ):
            yield from super().collect()


def pytest_pycollect_makeitem(collector, name, obj):
    if not TORCH_AVAILABLE:
        return None

    try:
        if (
            not issubclass(obj, PyTorchTestCaseTemplate)
            or obj is PyTorchTestCaseTemplate
        ):
            return None
    except Exception:
        return None

    return PyTorchTestCase.from_parent(collector, name=name, obj=obj)
