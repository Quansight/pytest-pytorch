# Contributing

First and foremost: Thank you for your interest in `pytest-pytorch`'s development! We appreciate all contributions be it code or something else.

If you are contributing bug-fixes or documentation improvements, you can open a [pull request (PR)](https://github.com/Quansight/pytest-pytorch/pulls) without further discussion. If on the other hand you are planning to contribute new features, please open an [issue](https://github.com/Quansight/pytest-pytorch/issues) and discuss the feature with us first.

Every PR is subjected to multiple automatic checks (continuous integration, CI) as well as a manual code review that it has to pass before it can be merged. The automatic checks are performed by [tox](https://tox.readthedocs.io/en/latest/). You can find details and instructions how to run the checks locally below.

## Guide lines

`pytest-pytorch` uses the [GitHub workflow](https://guides.github.com/introduction/flow/). Below is small guide how to make your first contribution.

The following guide assumes that [git](https://git-scm.com/), [python](https://www.python.org/), and [pip](https://pypi.org/project/pip/), are available on your system. If that is not the case, follow the official installation instructions.

`pytest-pytorch` officially supports Python `3.6` to `3.9`. To ensure backward compatibility, the development should happen on the minimum Python version, i. e. `3.6`.

1. Fork `pytest-pytorch` on GitHub

    Navigate to [Quansight/pytest-pytorch](https://github.com/Quansight/pytest-pytorch) on GitHub and click the **Fork** button in the top right corner.

2. Clone your fork to your local file system

    Use `git clone` to get a local copy of `pytest-pytorch`'s repository that you can work on:
  
    ```
    $ PYTEST_PYTORCH_ROOT="pytest-pytorch"
    $ git clone "https://github.com/Quansight/pytest-pytorch.git" $PYTEST_PYTORCH_ROOT
    ```

3. Setup your development environment

    ```
    $ cd $PYTEST_PYTORCH_ROOT
    $ virtualenv .venv --prompt="(pytest-pytorch) "
    $ source .venv/bin/activate
    $ pip install -r requirements-dev.txt
    $ pre-commit install
    ```
  
    While `pytest-pytorch`'s development requirements are fairly lightweight, it is still recommended installing them in a virtual environment rather than system wide. If you do not have `virtualenv` installed, you can do so by running `pip install --user virtualenv`.

4. Create a branch for local development

    Use `git checkout` to create local branch with a descriptive name:
  
    ```
    $ PYTEST_PYTORCH_BRANCH="my-awesome-feature-or-bug-fix"
    $ git checkout -b $PYTEST_PYTORCH_BRANCH
    ```
  
    Now make your changes. Happy Coding!

5. Use `tox` to run various checks

    ```
    $ tox
    ```
  
    This is equivalent to running
  
    ```
    $ tox -e lint
    $ tox -e tests
    ```
  
    You can find details what the individual commands do below of this guide.

6. Commit and push your changes

    If all checks are passing you can commit your changes an push them to your fork:
  
    ```
    $ git add .
    $ git commit -m "Descriptive message of the changes made"
    $ git push -u origin $PYTEST_PYTORCH_BRANCH
    ```
  
    For larger changes, it is good practice to split them in multiple small commits rather than one large one. If you do that, make sure to run the test suite before every commit. Furthermore, use `git push` without any parameters for consecutive pushes.

7. Open a Pull request (PR)

    1. Navigate to [Quansight/pytest-pytorch/pulls](https://github.com/Quansight/pytest-pytorch/pulls) on GitHub and click on the green button "New pull request".
    2. Click on "compare across forks" below the "Compare changes" headline.
    3. Select your fork for "head repository" and your branch for "compare" in the drop-down menus.
    4. Click the the green button "Create pull request".
  
    If the time between the branch being pushed and the PR being opened is not too long, GitHub will offer you a yellow box after step 1. If you click the button, you can skip steps 2. and 3.

Steps 1. to 3. only have to performed once. If you want to continue contributing, make sure to branch from the current `master` branch. You can use `git pull`

```
$ git checkout master
$ git pull origin
$ git checkout -b "my-second-awesome-feature-or-bug-fix"
```

If you forgot to do that or if since the creation of your branch many commits have been made to the `master` branch, simply rebase your branch on top of it.

```
$ git checkout master
$ git pull origin
$ git checkout "my-second-awesome-feature-or-bug-fix"
$ git rebase master
```

## Code format and linting

`pytest-pytorch` uses [`isort`](https://github.com/PyCQA/isort) to sort the imports, [black](https://black.readthedocs.io/en/stable/) to format the code, and [flake8](https://flake8.pycqa.org/en/latest/) to enforce [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance. To format and check the code style, run

```
$ cd $PYTEST_PYTORCH_ROOT
$ source .venv/bin/activate
$ tox -e lint
```

Instead of running the checks manually, you can install them as pre-commit hooks:

```
$ cd $PYTEST_PYTORCH_ROOT
$ source .venv/bin/activate
$ pre-commit install
```

Now, amongst others, the above checks are run automatically every time you add a commit.

## Testing

`pytest-pytorch` uses [`pytest`](https://docs.pytest.org/en/stable/) to run the test suite. You can run it locally with

```
cd $PYTEST_PYTORCH_ROOT
source .venv/bin/activate
tox -e test
```
