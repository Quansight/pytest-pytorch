# `pytest-pytorch`

[![license](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![repo status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![tests status](https://github.com/Quansight/pytest-pytorch/workflows/tests/badge.svg?branch=master)](https://github.com/Quansight/pytest-pytorch/actions?query=workflow%3Atests+branch%3Amaster)

## What is it?

`pytest-pytorch` is a lightweight [`pytest`]-plugin that enhances the developer experience when working with the [PyTorch] test suite if you come from a [`pytest`] background.

## Why do I need it?

Some testcases in the PyTorch test suite are only used as templates and will be instantiated at runtime. Unfortunately, [PyTorch]'s naming scheme for parametrizations differs from [`pytest`]'s. As a consequence, these tests cannot be selected by their names as written and one has to remember [PyTorch]'s naming scheme. This can be especially disrupting to your workflow if your IDE ([PyCharm](https://www.jetbrains.com/help/pycharm/pytest.html#run-pytest-test), [VSCode](https://code.visualstudio.com/docs/python/testing#_run-tests)) relies on [`pytest`]'s default selection syntax.

If this has ever been a source of frustration for you, worry no longer. `pytest-pytorch` was made for you.

## How do I install it?

You can install `pytest-pytorch` with `pip`

```shell
$ pip install pytest-pytorch
```

or with `conda`:

```shell
$ conda install -c conda-forge pytest-pytorch
```

## How do I use it?

With `pytest-pytorch` installed you can select test cases and tests by their names as written:

| Use case                            | Command                                 |
|-------------------------------------|-----------------------------------------|
| Run a test case against all devices | `pytest test_foo.py::TestBar`           |
| Run a test against all devices      | `pytest test_foo.py::TestBar::test_baz` |

Similar to a parametrization by [`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/example/parametrize.html#different-options-for-test-ids) you can use the [`-k` flag](https://docs.pytest.org/en/stable/reference.html#command-line-flags) to select a specific set of parameters:

| Use case                           | Command                                              |
|------------------------------------|------------------------------------------------------|
| Run a test case against one device | `pytest test_foo.py::TestBar -k "$DEVICE"`           |
| Run a test against one device      | `pytest test_foo.py::TestBar::test_baz -k "$DEVICE"` |

## Can I have a little more background?

Sure, we have written a [blog post about `pytest-pytorch`](https://deploy-preview-211--quansight-labs.netlify.app/blog/2021/06/pytest-pytorch/) that goes into details.

## How do I contribute?

First and foremost: Thank you for your interest in development of `pytest-pytorch`'s! We appreciate all contributions be it code or something else. Check out our [contribution guide lines](CONTRIBUTING.md) for details.

[PyTorch]: https://pytorch.org
[`pytest`]: https://docs.pytest.org/en/stable/
