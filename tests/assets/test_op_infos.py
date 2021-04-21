import torch
from torch.testing._internal.common_device_type import (
    dtypes,
    instantiate_device_type_tests,
    ops,
)
from torch.testing._internal.common_methods_invocations import OpInfo
from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    @dtypes(torch.float16, torch.int32)
    @ops([OpInfo("add"), OpInfo("sub")])
    def test_bar(self, device, dtype, op):
        assert True


instantiate_device_type_tests(TestFoo, globals())
