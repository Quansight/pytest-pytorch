from torch.testing._internal.common_device_type import instantiate_device_type_tests
from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    def test_bar(self, device):
        pass


instantiate_device_type_tests(TestFoo, globals(), only_for="cpu")


class TestSpam(TestCase):
    def test_ham(self):
        pass
