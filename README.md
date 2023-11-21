# backend-python-creditcard

Sample backend in python for credit cards

## Requirements

- Python 3.11 (you can use pyenv to select correct version).

  And one of the following

- [poetry](https://python-poetry.org/)
- [virtualenv](https://pypi.org/project/virtualenv/)

## Get started

- Install dependencies.

  - Using poetry

    Poetry can automagically manage virtual environments for you. If you have it installed in your system, you can just use `poetry install`.

  - Using virtualenv

    With the virtual env option, we also use poetry, but it will be contained withing the virtual environment.

    ```bash
    python3 -m virtualenv venv
    source venv/bin/activate
    pip3 install poetry
    poetry install
    ```
