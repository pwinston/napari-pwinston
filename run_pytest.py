#!/usr/bin/env python3
"""

To cause segfault:
    import ctypes
    ctypes.string_at(0)
"""
import json
import sys
import subprocess

NAPARI_DIR = "/Users/pbw/dev/napari"


def run_pytest(start, end, tests):
    cmd = ["pytest"] + tests[start:end]
    print(f"Running {len(tests)} tests")
    print(cmd)
    process = subprocess.run(cmd, cwd=NAPARI_DIR)
    return_code = process.returncode
    with open("tests.log", "a") as log:
        result = {
            "return_code": return_code,
            "start": start,
            "end": end,
            "num_tests": len(tests),
        }
        log.write(json.dumps(result))
        log.write("\n")
    return return_code


def read_tests():
    with open(sys.argv[1]) as infile:
        return [x.strip() for x in infile.readlines()]


def run_all_tests(tests):
    for test_name in tests:
        run_pytest(0, 1, [test_name])


def search_tests(start, end, tests):
    if run_pytest(start, end, tests) == -11:
        num_tests = end - start
        if num_tests > 1:
            middle = (start - end) // 2
            search_tests(start, middle, tests)
            search_tests(middle, end, tests)


def main():
    tests = read_tests()
    tests = tests
    search_tests(0, len(tests), tests)


if __name__ == '__main__':
    sys.exit(main())

