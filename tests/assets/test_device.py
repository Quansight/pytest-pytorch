from torch.testing._internal.common_device_type import (
    instantiate_device_type_tests,
    onlyCPU,
    onlyOn,
)
from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    # fails for meta, passes for cpu
    def test_bar(self, device):
        assert device != "meta"

    # passes for meta, skips for cpu
    @onlyOn("meta")
    def test_baz(self, device):
        assert True


instantiate_device_type_tests(TestFoo, globals())


class TestSpam(TestCase):
    # passes for meta, fails for cpu
    def test_ham(self, device):
        assert device == "meta"

    # skips for meta, fails for cpu
    @onlyCPU
    def test_eggs(self, device):
        assert False


instantiate_device_type_tests(TestSpam, globals())
