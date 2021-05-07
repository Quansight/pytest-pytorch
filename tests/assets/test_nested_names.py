from torch.testing._internal.common_utils import TestCase


class TestFoo(TestCase):
    def test_baz(self):
        pass


class TestFooBar(TestCase):
    def test_baz(self):
        pass


class TestSpam(TestCase):
    def test_ham(self):
        pass

    def test_ham_eggs(self):
        pass
