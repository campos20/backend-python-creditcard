# backend-python-creditcard

Sample backend in python for credit cards

## Requirements

- Python 3.11 (you can use pyenv to select correct version).

- [virtualenv](https://pypi.org/project/virtualenv/)

## Get started

This assumes you already closed the repo and navigated to it.

- Install dependencies.

We will be using poetry on top of virtualenv. You need to activate the virtualenv then start using poetry.

```bash
python3 -m virtualenv venv
source venv/bin/activate
pip3 install poetry
poetry install
```

## Local run

With the virtualenv activated, you can use

```bash
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs).

## Activate the virtualenv without installing

You only need to run `poetry install` on your first run (or if any package was added to the project).

To activate the virtualenv without installing, you just need to run

```bash
source venv/bin/activate
uvicorn main:app --reload
```
