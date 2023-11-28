# backend-python-creditcard

## Requirements

- Python 3.11 (you can use pyenv to select correct version).

- [virtualenv](https://pypi.org/project/virtualenv/)

## Get started

This assumes you already cloned the repo and navigated to it. Also, that you started containers following the root README.md instructions.

- Navigate to the app folder

```bash
cd app
```

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

## Using the authorization

When you visit [http://localhost:8000/docs](http://localhost:8000/docs), you will notice a gree `Authorize` button. This allows you to use the authorization headers for all the endpoints that requires it.

## Activate the virtualenv without installing

You only need to run `poetry install` on your first run (or if any package was added to the project).

To activate the virtualenv without installing, you just need to run

```bash
source venv/bin/activate
uvicorn main:app --reload
```

## Testing

You will need to be in the `app` folder, virtualenv should be activated.

```bash
python -m pytest -o log_cli=true
```

## Decisions

Here are some reasonings behind some decisions you will find on this project:

- FastAPI: It is a modern web framework that is quickly becoming one of the most common options for creating backends with Python. It is fast and easy to use.
- Databases on docker: this is to make this project as plug-n-play and also disposable.
- We only secured 1 endpoint (a POST to create a credit card) as creating resources are critical. This project also uses it's own signed jwt. Secret key were generated with `openssl rand -hex 32`.
