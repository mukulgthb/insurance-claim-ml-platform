# Local development setup

Environment: Windows with Git Bash
Python command: python

## Create and activate the virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## Install dependencies

```bash
python -m pip install --only-binary=:all: -r requirements.txt
```

## Verify the environment

```bash
python --version
python -m pip --version
python -m pip check
```

## Record installed versions

```bash
python -m pip freeze > requirements-lock.txt
```
