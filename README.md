# babelize

A framework for managing Hugo translations

## Development

Create your venv and install requirements-dev.txt:

```
python -m venv venv
. ./venv/bin/activate
make dev
pre-commit install
```

## Use

```
babelize ls -l
babelize ls -l ES
babelize ls -l ES -d 3
babelize ls -l ES -l DE
```