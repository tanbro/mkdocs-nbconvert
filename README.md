# mkdocs-nbconvert

[![PyPI](https://img.shields.io/pypi/v/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)
[![GitHub tag (latest SemVer pre-release)](https://img.shields.io/github/v/tag/tanbro/mkdocs-nbconvert)](https://github.com/tanbro/mkdocs-nbconvert)
[![workflow](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml/badge.svg)](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml)

A [MkDocs][] plugin provides a source parser for `*.ipynb` [Jupyter][] Notebook files, based on [nbconvert][].

## References

- <https://tanbro.github.io/mkdocs-nbconvert/>
- <https://www.mkdocs.org/user-guide/plugins/>

## Build the Site

The project's documentation site serves as a demo of how to use it.

To build and serve the doc-site, run the following command in on a virtual environment:

```bash
pip install -e . --group dev
mkdocs serve
```

[MkDocs]: http://www.mkdocs.org/
[Jupyter]: https://jupyter.org/
[nbconvert]: https://pypi.org/project/nbconvert/
