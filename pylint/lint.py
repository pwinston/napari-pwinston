#!/usr/bin/env python3
"""lint.py
"""
import click

from pylint.lint import Run
from pathlib import Path

ROOT = Path("/Users/pbw/dev/napari")

PATHS = [
    "napari/_vispy/experimental/*.py",
    "napari/layers/image/experimental/*.py",
    "napari/_qt/experimental/*.py",
    "napari/_qt/experimental/render/*.py",
]


# Run(['--errors-only', 'myfile.py'])


def _run_pylint(paths):
    str_paths = [str(path) for path in paths]
    Run(str_paths, do_exit=False)


def _split_path_pattern(path):
    directory, pattern = path.split('*')
    return ROOT / directory, '*' + pattern


@click.command()
@click.argument('match_string', required=False)
def lint(match_string):
    for spec in PATHS:
        dir_path, pattern = _split_path_pattern(spec)

        paths = Path(dir_path).glob(pattern)

        if match_string is not None:
            paths = [path for path in paths if match_string in str(path)]

        if paths:
            print(f"====== LINTING: {dir_path}/{pattern}")
            _run_pylint(paths)


if __name__ == '__main__':
    lint()
