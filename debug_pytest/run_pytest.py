#!/usr/bin/env python3
"""

To cause segfault:
    import ctypes
    ctypes.string_at(0)
"""
import json
import math
import sys
import subprocess

NAPARI_DIR = "/Users/pbw/dev/napari"


def run_pytest(start, end, tests):
    cmd = ["pytest", "-v", "-s"] + tests[start:end]
    print(f"Running {len(tests)} tests")
    print(cmd)
    process = subprocess.run(cmd, cwd=NAPARI_DIR)
    return_code = process.returncode
    with open("tests.log", "a") as log:
        result = {
            "return_code": return_code,
            "start": start,
            "end": end,
            "num_tests": end - start + 1,
        }
        log.write(json.dumps(result))
        log.write("\n")
    return return_code


def read_tests(path):
    with open(path) as infile:
        return [x.strip() for x in infile.readlines()]


def run_all_tests(tests):
    for test_name in tests:
        run_pytest(0, 1, [test_name])


def search_tests(start, end, tests):
    if run_pytest(start, end, tests) == -11:
        num_tests = end - start
        sys.stdout.flush()
        if num_tests > 1:
            middle1 = start + (end - start) // 3
            middle2 = start + 2 * (end - start) // 3
            search_tests(start, middle1, tests)
            search_tests(middle1, middle2, tests)
            search_tests(middle2, end, tests)


def main():
    path = sys.argv[1]
    tests = read_tests(path)

    if len(sys.argv) == 4:
        start = int(sys.argv[2])
        end = int(sys.argv[3])
    else:
        start = 0
        end = len(tests)

    if end <= start:
        print("Invalid range")
        return 1

    tests = tests
    search_tests(start, end, tests)


if __name__ == '__main__':
    sys.exit(main())

