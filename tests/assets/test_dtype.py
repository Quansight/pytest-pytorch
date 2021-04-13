import unittest

import torch
from torch.testing._internal.common_device_type import (
    dtypes,
    instantiate_device_type_tests,
    onlyCPU,
)
from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    @onlyCPU
    @dtypes(torch.float16, torch.int32)
    # fails for float16, passes for int32
    def test_bar(self, device, dtype):
        assert dtype == torch.int32

    # passes for float16, skips for int32
    @onlyCPU
    @dtypes(torch.float16, torch.int32)
    def test_baz(self, device, dtype):
        if dtype == torch.int32:
            raise unittest.SkipTest

        assert True


instantiate_device_type_tests(TestFoo, globals())


class TestSpam(TestCase):
    @onlyCPU
    def test_ham(self, device):
        assert True

    @onlyCPU
    @dtypes(torch.float16)
    def test_eggs(self, device, dtype):
        assert False


instantiate_device_type_tests(TestSpam, globals())
