from torch.testing._internal.common_device_type import (
    instantiate_device_type_tests,
    onlyCPU,
    onlyOn,
)
from torch.testing._internal.common_utils import TestCase

# ======================================================================================
# This block is necessary to autogenerate the parametrization for
# tests/test_plugin.py::test_standard_collection.
# It needs to be placed **after** the import of 'instantiate_device_type_tests' and
# **before** its first usage.
# ======================================================================================
try:
    from _spy import Spy

    __spy__ = Spy()
    del Spy
    instantiate_device_type_tests = __spy__(instantiate_device_type_tests)
except ModuleNotFoundError:
    pass
# ======================================================================================


class TestFoo(TestCase):
    def test_bar(self, device):
        pass

    def test_baz(self, device):
        pass


instantiate_device_type_tests(TestFoo, globals(), only_for=["cpu", "meta"])


class TestSpam(TestCase):
    @onlyOn("meta")
    def test_ham(self, device):
        pass

    @onlyCPU
    def test_eggs(self, device):
        pass


instantiate_device_type_tests(TestSpam, globals(), only_for=["cpu", "meta"])


class TestQux(TestCase):
    def test_quux(self, device):
        pass


instantiate_device_type_tests(TestQux, globals(), only_for=["cpu"])
