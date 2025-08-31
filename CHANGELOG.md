# CHANGELOG

## v0.4

> 📅 **Date** 2025-08-31

- ✨ **New Features:**
    - Now the plugin will call `nbconvert` to execute notebooks in a poll executor, and the number of currency is `cpu_count` by default. A new configuration `max_workers` is added to control the number of currency.

- 💔 **Breaking Changes:**
    - update `mkdocs` version to `1.6`

## v0.3.1

> 📅 **Date** 2025-1-16

- 🔧 Upgrade:
    - `mkdocs` to 1.6.1
    - `nbconvert` to 7.16.5
    - hooks in pre-commit

- 🔨: Remove unused packages in `requirements.txt` and `pyproject.toml`

## v0.3

> 📅 **Date** 2024-4-7

Mark the package's Development Status to 5 - Production/Stable

## v0.2.2

> 📅 **Date** 2024-3-11

Update dependencies and tools to latest version.

## v0.2.1

Date: 2023-06-29

- Release highlights:
    - Add a new notebook execution configure: `exit_on_error`

- Fixing:
    - `mkdocs` and `nbconvert` dependent versions in `pyproject.toml`
    - Typos

- Docs:
    - Edit usage notebook

## v0.2

Date: 2023-06-28

- Release highlights:
    - Now the plugin can execute notebooks before convert

- Break changes:
    - No longer support for python earlier than 3.7
    - Drop `setup.cfg`, only `pyproject.toml`

- Library:
    - Update to latest mkdocs

- Docs
    - Update to latest mkdocs-material and re-build doc-site

- CI
    - Many pre-commit checks

## v0.1.3

Date: 2022-04-18

- Changes:
    - Switch to BSD 2-Clause License, and add the license file to repo.
    - Drop supports of old python (<=3.6))
    - Change the package's build system to PEP517

## v0.1.2

Date: 2020-07-17

- New documentation site

## v0.1

Date: 2020-01-16

A very early alpha version, not for production.
