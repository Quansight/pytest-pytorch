import torch
from torch.testing._core import _dispatch_dtypes
from torch.testing._internal.common_device_type import (
    instantiate_device_type_tests,
    ops,
)
from torch.testing._internal.common_methods_invocations import OpInfo
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

dtypes = _dispatch_dtypes((torch.float32,))


class TestFoo(TestCase):
    @ops(
        [
            OpInfo("add", dtypes=dtypes),
            OpInfo("sub", dtypes=dtypes),
        ]
    )
    def test_bar(self, device, dtype, op):
        pass


instantiate_device_type_tests(TestFoo, globals(), only_for="cpu")
