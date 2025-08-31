from __future__ import annotations

import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from glob import iglob
from itertools import repeat
from multiprocessing import cpu_count
from os import makedirs, path, remove, removedirs
from pprint import pformat
from time import time
from typing import TYPE_CHECKING

if sys.version_info < (3, 12):  # pragma: no cover
    from typing_extensions import override
else:  # pragma: no cover
    from typing import override

import nbformat
from mkdocs.config import base, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.utils import log
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import (  # pyright: ignore[reportPrivateImportUsage]
    CellExecutionError,
    ExecutePreprocessor,
)

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files


__all__ = ["NbConvertPlugin"]


class _ExecuteOptions(base.Config):
    run_path = config_options.Optional(config_options.Dir())
    kernel_name = config_options.Optional(config_options.Type(str))
    timeout = config_options.Optional(config_options.Type(int))
    write_back = config_options.Type(bool, default=False)
    exit_on_error = config_options.Type(bool, default=True)


class _PluginConfig(base.Config):
    input_dir = config_options.Dir(exists=True, default="notebooks")
    output_dir = config_options.Type(str, default="notebooks")
    recursive = config_options.Type(bool, default=True)
    execute_enabled = config_options.Type(bool, default=False)
    execute_options = config_options.SubConfig(_ExecuteOptions)
    # Add concurrency control parameter, default to CPU count
    max_workers = config_options.Type(int, default=cpu_count())


def _convert_notebook(nb_path, docs_dir, site_dir, use_directory_urls, input_dir, output_dir, execute_options):
    """
    Standalone function to convert notebook in a separate thread
    """
    execute_options = execute_options or {}

    # Prepare output file/directory
    nb_dirname, nb_basename = path.split(nb_path)
    nb_basename_root, _ = path.splitext(nb_basename)
    nb_subdir = path.relpath(nb_dirname, input_dir)
    md_dir = path.join(output_dir, nb_subdir)
    md_basename = f"{nb_basename_root}.md"
    md_path = path.join(md_dir, md_basename)
    md_rel_dir = path.relpath(md_dir, docs_dir)
    md_rel_path = path.join(md_rel_dir, md_basename)

    file_obj = File(
        path=md_rel_path,
        src_dir=docs_dir,
        dest_dir=site_dir,
        use_directory_urls=use_directory_urls,
    )

    assert file_obj.abs_src_path is not None
    src_files = [file_obj.abs_src_path]

    log.info("[NbConvertPlugin] %r => %r", nb_path, file_obj)

    # Read notebook
    with open(nb_path, encoding="utf-8") as fp:
        nb = nbformat.read(fp, nbformat.NO_CONVERT)

    # Pre-execute
    if execute_options is not None:
        log.debug("[NbConvertPlugin] notebook execution start: %s", nb_path)
        ts = time()
        exe_completed = False
        exe_opts = {k: v for k, v in execute_options.items() if k in ("timeout", "kernel_name") and v is not None}
        exe_path, exe_save, exe_exit_on_error = (execute_options.get(a) for a in ("run_path", "write_back", "exit_on_error"))

        ep = ExecutePreprocessor(**exe_opts)
        try:
            ep.preprocess(nb, {"metadata": {"path": exe_path if exe_path else input_dir}})
        except CellExecutionError as err:
            if exe_exit_on_error:
                raise
            exe_completed = True
            log.error("[NbConvertPlugin] notebook execution error(%.3fs): %s: %s", time() - ts, err, nb_path)
        else:
            exe_completed = True
            log.debug("[NbConvertPlugin] notebook execution finish(%.3fs): %s", time() - ts, nb_path)
        finally:
            if exe_save and exe_completed:
                log.debug("[NbConvertPlugin] save notebook: %s", nb_path)
                with open(nb_path, "w", encoding="utf-8") as fp:
                    nbformat.write(nb, fp)

    # Convert
    exporter = MarkdownExporter()
    body, resources = exporter.from_notebook_node(nb)

    # Save exported file
    makedirs(md_dir, exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as fp:
        fp.write(body)

    for resource_name, resource_data in resources["outputs"].items():
        resource_src_dir = path.dirname(file_obj.abs_src_path)
        resource_src_path = path.join(resource_src_dir, resource_name)
        makedirs(resource_src_dir, exist_ok=True)
        with open(resource_src_path, "wb") as fp:
            fp.write(resource_data)
        src_files.append(resource_src_path)
        resource_dest_dir = path.dirname(file_obj.abs_dest_path)
        resource_dest_path = path.join(resource_dest_dir, resource_name)
        log.debug(
            "[NbConvertPlugin] resource output(%dBytes): %s => %s",
            len(resource_data),
            resource_name,
            resource_dest_path,
        )
        makedirs(resource_dest_dir, exist_ok=True)
        with open(resource_dest_path, "wb") as fp:
            fp.write(resource_data)

    return file_obj, src_files


class NbConvertPlugin(BasePlugin[_PluginConfig]):
    @override
    def on_files(self, files: Files, /, *, config: MkDocsConfig) -> Files:
        log.debug("[NbConvertPlugin] config: %s", pformat(self.config))
        self._src_files = []
        # deal with dirs
        config_file_dir = path.dirname(config["config_file_path"])
        input_dir = path.normpath(self.config["input_dir"])
        output_dir = path.realpath(path.join(config["docs_dir"], path.normpath(self.config["output_dir"])))
        if not path.isabs(input_dir):
            input_dir = path.realpath(path.join(config_file_dir, input_dir))
        # glob match
        nb_finder = iglob(path.join(config_file_dir, input_dir, "**", "*.ipynb"), recursive=self.config["recursive"])

        # Pre-execute args
        execute_options = None
        if self.config.get("execute_enabled"):
            execute_options = self.config.get("execute_options") or {}

            # On windows:
            #   Proactor event loop does not implement add_reader family of methods required for zmq.
            #   Registering an additional selector thread for add_reader support via tornado.
            #   Use `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` to avoid this warning.
            if sys.platform == "win32":
                from asyncio import windows_events

                asyncio.set_event_loop_policy(windows_events.WindowsSelectorEventLoopPolicy())

        # Use ThreadPoolExecutor to process notebooks in parallel
        # nbconvert will start separate processes when executing notebooks, so using thread pool is more appropriate
        # Use max_workers parameter to control concurrency, default to CPU count
        with ThreadPoolExecutor(max_workers=self.config["max_workers"]) as pool:
            results = pool.map(
                _convert_notebook,
                nb_finder,
                repeat(config["docs_dir"]),
                repeat(config["site_dir"]),
                repeat(config["use_directory_urls"]),
                repeat(input_dir),
                repeat(output_dir),
                repeat(execute_options),
            )

            # Collect results
            for file_obj, src_files in results:
                self._src_files.extend(src_files)
                files.append(file_obj)

        return files

    @override
    def on_post_build(self, *, config: MkDocsConfig):
        for file in self._src_files:
            log.debug("[NbConvertPlugin] remove: %r", file)
            remove(file)
        output_dir = path.join(config["docs_dir"], path.normpath(self.config["output_dir"]))
        log.debug("[NbConvertPlugin] removedirs: %r", output_dir)
        try:
            removedirs(output_dir)
        except OSError as err:
            log.warning("[NbConvertPlugin] OSError on removedirs %r: %s", output_dir, err)
