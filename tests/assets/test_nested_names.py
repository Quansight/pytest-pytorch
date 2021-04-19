from torch.testing._internal.common_device_type import (
    instantiate_device_type_tests,
    onlyOn,
)
from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    # fails for meta, passes for cpu
    def test_baz(self, device):
        assert device != "meta"


instantiate_device_type_tests(TestFoo, globals())


class TestFooBar(TestCase):
    # passes for meta, skips for cpu
    @onlyOn("meta")
    def test_baz(self, device):
        assert True


instantiate_device_type_tests(TestFooBar, globals())
