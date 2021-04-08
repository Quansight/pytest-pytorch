import unittest.mock

from _pytest.unittest import TestCaseFunction, UnitTestCase

from torch.testing._internal.common_utils import TestCase as PyTorchTestCaseTemplate


class TemplateName(str):
    def __eq__(self, other):
        return self.startswith(str(other))

    def __hash__(self) -> int:
        return super().__hash__()


class PyTorchTestCaseFunction(TestCaseFunction):
    @classmethod
    def from_parent(cls, parent, *, name, **kw):
        return super().from_parent(parent, name=TemplateName(name), **kw)


class PyTorchTestCase(UnitTestCase):
    @classmethod
    def from_parent(cls, parent, *, name, obj=None):
        return super().from_parent(parent, name=TemplateName(name), obj=obj)

    def collect(self):
        # Yes, this is a bad practice. Unfortunately, there is no other option to
        # inject our custom 'TestCaseFunction' without duplicating everyting in
        # 'UnitTestCase.collect()'
        with unittest.mock.patch(
            "_pytest.unittest.TestCaseFunction", new=PyTorchTestCaseFunction
        ):
            yield from super().collect()


def pytest_pycollect_makeitem(collector, name, obj):
    try:
        if (
            not issubclass(obj, PyTorchTestCaseTemplate)
            or obj is PyTorchTestCaseTemplate
        ):
            return None
    except Exception:
        return None

    return PyTorchTestCase.from_parent(collector, name=name, obj=obj)
