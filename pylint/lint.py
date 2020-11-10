#!/usr/bin/env python3
"""lint.py
"""
from pylint.lint import Run
from pathlib import Path

ROOT = Path("/Users/pbw/dev/napari")

PATHS = [
    "napari/_vispy/experimental/*.py",
    "napari/layers/image/experimental/*.py",
]


# Run(['--errors-only', 'myfile.py'])


def _run_lint(paths):
    str_paths = [str(path) for path in paths]
    Run(str_paths)


def _split_path_pattern(path):
    directory, pattern = path.split('*')
    return ROOT / directory, '*' + pattern


def main():
    paths = []

    for spec in PATHS:
        dir_path, pattern = _split_path_pattern(spec)

        print(f"Searching {dir_path} for {pattern}")
        paths.extend(Path(dir_path).glob(pattern))

    _run_lint(paths)


if __name__ == '__main__':
    main()
