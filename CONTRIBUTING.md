# Contributing

## Publishing to PyPI

### Prerequisites

```bash
pip install --upgrade pip
pip install --upgrade build
pip install --upgrade twine
```

### Building and Publishing to PyPI

```bash
python -m build
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
```

## Docker Container

Example: `docker-fastqc` (https://github.com/hisplan/docker-fastqc)

TBD

## WDL Pipeline

Example: `sharp (♯)` (https://github.com/hisplan/sharp)

TBD

## Boilerplate

https://github.com/hisplan/wdl-boilerplate
