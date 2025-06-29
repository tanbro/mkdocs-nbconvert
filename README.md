# mkdocs-nbconvert

[![PyPI](https://img.shields.io/pypi/v/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)
[![GitHub tag (latest SemVer pre-release)](https://img.shields.io/github/v/tag/tanbro/mkdocs-nbconvert)](https://github.com/tanbro/mkdocs-nbconvert)
[![workflow](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml/badge.svg)](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml)

A [MkDocs][] plug-in provides a source parser for `*.ipynb` [Jupyter][] Notebook files, base on [nbconvert][].

## References

- <https://tanbro.github.io/mkdocs-nbconvert/>
- <https://www.mkdocs.org/user-guide/plugins/>

## Build the site

The project itself's documentation site is a demo of how to use it.

To build and serve the doc-site, run the following command in on a virtual environment:

```bash
pip install -e . --group dev
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.

[MkDocs]: http://www.mkdocs.org/
[Jupyter]: https://jupyter.org/
[nbconvert]: https://pypi.org/project/nbconvert/
