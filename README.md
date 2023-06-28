# mkdocs-nbconvert

[![PyPI](https://img.shields.io/pypi/v/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)
[![PyPI - Status](https://img.shields.io/pypi/status/mkdocs-nbconvert)](https://pypi.org/project/mkdocs-nbconvert/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)
[![PyPI - Format](https://img.shields.io/pypi/format/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)

A [MkDocs][] plug-in provides a source parser for `*.ipynb` [Jupyter][] Notebook files, base on [nbconvert][].

## References

- <https://tanbro.github.io/mkdocs-nbconvert/>
- <https://www.mkdocs.org/user-guide/plugins/>

## Build the site

The project itself's documentation site is a demo of how to use it.

To build and serve the doc-site:

```bash
pip install -r dev.requirements.txt
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.

[MkDocs]: http://www.mkdocs.org/
[Jupyter]: https://jupyter.org/
[nbconvert]: https://pypi.org/project/nbconvert/
