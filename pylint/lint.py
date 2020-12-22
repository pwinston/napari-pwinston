#!/usr/bin/env python3
"""lint.py
"""
from pathlib import Path

import click

from pylint.lint import Run

PATHS = {
    "/Users/pbw/dev/napari": [
        "napari/_vispy/experimental/*.py",
        "napari/layers/image/experimental/*.py",
        "napari/components/experimental/*.py",
        "napari/components/experimental/chunk/*.py",
        "napari/components/experimental/chunk/_commands/*.py",
        "napari/components/experimental/monitor/*.py",
        "napari/components/experimental/remote/*.py",
    ],
    "/Users/pbw/dev/webmon": ["*.py", "lib/*.py"],
}


# Run(['--errors-only', 'myfile.py'])


def _run_pylint(paths):

    print(f"Checking {len(paths)} files:")
    for path in paths:
        print(f"Checking {path}")

    # Pylint wants string not Path objects.
    str_paths = [str(path) for path in paths]

    Run(str_paths, do_exit=False)


def _split_path_pattern(root, path):
    directory, pattern = path.split('*')
    return root / directory, '*' + pattern


@click.command()
@click.argument('match_string', required=False)
def lint(match_string):
    for root, paths in PATHS.items():
        root = Path(root)
        for spec in paths:
            dir_path, pattern = _split_path_pattern(root, spec)

            paths = Path(dir_path).glob(pattern)

            if match_string is not None:
                paths = [path for path in paths if match_string in str(path)]

            if paths:
                print(f"====== LINTING: {dir_path}/{pattern}")
                _run_pylint(list(paths))


if __name__ == '__main__':
    lint()
