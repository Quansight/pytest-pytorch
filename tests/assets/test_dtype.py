import torch
from torch.testing._internal.common_device_type import (
    dtypes,
    instantiate_device_type_tests,
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
    @dtypes(torch.float16, torch.int32)
    def test_bar(self, device, dtype):
        pass


instantiate_device_type_tests(TestFoo, globals(), only_for="cpu")
