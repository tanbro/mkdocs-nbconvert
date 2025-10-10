# mkdocs-nbconvert

[![PyPI](https://img.shields.io/pypi/v/mkdocs-nbconvert.svg)](https://pypi.org/project/mkdocs-nbconvert/)
[![GitHub tag (latest SemVer pre-release)](https://img.shields.io/github/v/tag/tanbro/mkdocs-nbconvert)](https://github.com/tanbro/mkdocs-nbconvert)
[![workflow](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml/badge.svg)](https://github.com/tanbro/mkdocs-nbconvert/actions/workflows/workflow.yml)

A [MkDocs][] plugin provides a source parser for `*.ipynb` [Jupyter][] Notebook files, based on [nbconvert][].

## Features

- Converts Jupyter Notebook files (`.ipynb`) to Markdown during the MkDocs build process
- Supports executing notebooks before conversion to include output results
- Concurrent processing for faster builds with `max_workers` option
- Flexible configuration for input/output directories and execution options
- Automatic cleanup of temporary files after build

## Installation

This [MkDocs](http://www.mkdocs.org/) plugin is based on [Jupyter](https://jupyter.org/) [nbconvert](https://nbconvert.readthedocs.io/).

When install the plugin, jupyter and nbconvert will also be installed.

### Install by pip

```sh
pip install mkdocs-nbconvert
```

### Install from source

```
git clone https://github.com/tanbro/mkdocs-nbconvert.git
cd mkdocs-nbconvert
pip install .
```

## Quick Start

### Mkdocs configuration

Add the `nbconvert` into configuration file (`mkdocs.yml`)'s `plugins` list

```yaml
plugins:
    - nbconvert
```

In `nav` section, add `*.ipynb` files as normal markdown files with replacing extension `*.ipynb` to `*.md`, since they're converted to markdown files in `output_dir`:

```yaml
nav:
    - index.md
    - Notebooks:
          - notebooks/installation.md
          - notebooks/usage.md
          - notebooks/image.md
          - notebooks/matplotlib.md
    - authors.md
    - changelog.md
```

> **Warning:**
>
> converted `notebooks/*.md` files will be removed at the end of building.

## Configuration

The plugin provides several configuration options:

- `input_dir`: Directory where to scan `*.ipynb` files

    Either absolute or relative path.
    When relative, it's from `mkdocs` configuration file's directory.

    When omitted, default value is `notebooks`

- `output_dir`: Export notebook files to markdown files in the directory.

    It **MUST** be a **relative** path to [`doc_dir`](https://www.mkdocs.org/user-guide/configuration/#docs_dir)

    When omitted, default value is `notebooks`.

- `recursive`: Whether scan `*.ipynb` files in subdirectories recursively

    When omitted, default value is `True`

- `execute_enabled`: Whether executing notebooks before convert. `false` by default

- `max_workers`: Number of concurrent threads used to process notebooks. Defaults to the number of CPU cores.

- `execute_options`: Options for execution:

    - `execute_options.run_path`: Specifies in which folder to execute the notebook. The plugin in will take `input_dir` as the path if not specified.

    - `execute_options.kernel_name`: The execution kernel. When not specified, the default Python kernel is chosen.

    - `execute_options.timeout`: The cell execution timeout. No timeout when not specified.

    - `execute_options.write_back`: Whether save executed result to the notebook file. `false` by default.

    - `execute_options.exit_on_error`: Whether exit when an error occurred. Default is `true`.

Options can be add to configuration file as below:

```yaml
plugins:
    - nbconvert:
         input_dir: notebooks
         recursive: true
         output_dir: notebooks
         execute_enabled: true
         max_workers: 4
         execute_options:
             write_back: true
             exit_on_error: true
```

In the above example, the plugin recursively searches Jupyter notebook files in `{{project_dir}}\notebooks`, then converts them to markdown files to `{{project_dir}}\docs\notebooks`, where `{{project_dir}}\docs` is the default value of [`doc_dir`](https://www.mkdocs.org/user-guide/configuration/#docs_dir) configure. A pre-execution will be performed, and the running result will be saved to original notebook files. The conversion will be processed using 4 concurrent threads.

## References

- <https://tanbro.github.io/mkdocs-nbconvert/>
- <https://www.mkdocs.org/user-guide/plugins/>

## Build the Site

The project's documentation site serves as a demo of how to use it.

To build and serve the doc-site, run the following command in on a virtual environment:

```bash
pip install -e . --group docs
mkdocs serve
```

[MkDocs]: http://www.mkdocs.org/
[Jupyter]: https://jupyter.org/
[nbconvert]: https://pypi.org/project/nbconvert/
