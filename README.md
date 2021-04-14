# `pytest-pytorch`

[![license](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![repo status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![tests status](https://github.com/Quansight/pytest-pytorch/workflows/tests/badge.svg?branch=master)](https://github.com/Quansight/pytest-pytorch/actions?query=workflow%3Atests+branch%3Amaster)

## What is it?

`pytest-pytorch` is a lightweight [`pytest`](https://docs.pytest.org/en/stable/)-plugin that enhances the developer experience when working with the PyTorch test suite if you come from a `pytest` background.

## Why do I need it?

Some testcases in the PyTorch test suite are automatically generated when a module is loaded in order to parametrize them. Trying to collect them with their names as written, e.g. `pytest test_foo.py::TestFoo` or `pytest test_foo.py::TestFoo::test_bar`, is unfortunately not possible. If you are used to this syntax or your IDE relies on it ([PyCharm](https://www.jetbrains.com/help/pycharm/pytest.html#run-pytest-test), [VSCode](https://code.visualstudio.com/docs/python/testing#_run-tests)), you can install `pytest-pytorch` to make it work.

## How do I install it?

Installing `pytest-pytorch` is as easy as 

```
$ pip install pytest-pytorch
```

## How do I use it?

With `pytest-pytorch` installed you can select test cases and tests as if the instantiation for different devices was performed by [`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/example/parametrize.html#different-options-for-test-ids):

| Use case                            | Command                                              |
|-------------------------------------|------------------------------------------------------|
| Run a test case against all devices | `pytest test_foo.py::TestBar`                        |
| Run a test case against one device  | `pytest test_foo.py::TestBar -k "$DEVICE"`           |
| Run a test against all devices      | `pytest test_foo.py::TestBar::test_baz`              |
| Run a test against one device       | `pytest test_foo.py::TestBar::test_baz -k "$DEVICE"` |

## Can I have a little more background?

PyTorch uses its own method for generating tests that is for the most part compatible with [`unittest`](https://docs.python.org/3/library/unittest.html) and pytest. Its custom test generation allows test templates to be written and instantiated for different device types, data types, and operators. Consider the following module `test_foo.py`:

```python
from torch.testing._internal.common_utils import TestCase
from torch.testing._internal.common_device_type import instantiate_device_type_tests

class TestFoo(TestCase):
    def test_bar(self, device):
        pass
    
    def test_baz(self, device):
        pass

instantiate_device_type_tests(TestFoo, globals())
```

Assuming we `"cpu"` and `"cuda"` are available as devices, we can collect four tests:

1. `test_foo.py::TestFooCPU::test_bar_cpu`,
2. `test_foo.py::TestFooCPU::test_baz_cpu`,
3. `test_foo.py::TestFooCUDA::test_bar_cuda`, and
4. `test_foo.py::TestFooCUDA::test_baz_cuda`.

From a `pytest` perspective this is similar to decorating `TestFoo` with `@pytest.mark.parametrize("device", ("cpu", "cuda")))` which would result in

1. `test_foo.py::TestFoo:test_bar[cpu]`,
2. `test_foo.py::TestFoo:test_bar[cuda]`,
3. `test_foo.py::TestFoo:test_baz[cpu]`, and
4. `test_foo.py::TestFoo:test_baz[cuda]`.

Since the PyTorch test framework renames testcases and tests, naively running `pytest test_foo.py::TestFoo` or `pytest test_foo.py::TestFoo::test_bar` fails, because it can't find anything matching these names. Of course you can get around it by using the regular expression matching ([`-k` command line flag](https://docs.pytest.org/en/stable/reference.html#command-line-flags)) that `pytest` offers. 

`pytest-pytorch` performs this matching so you can keep your familiar workflow and your IDE is happy out of the box.

## How do I contribute?

First and foremost: Thank you for your interest in development of `pytest-pytorch`'s! We appreciate all contributions be it code or something else. Check out our [contribution guide lines](CONTRIBUTING.md) for details.
