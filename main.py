#!/usr/bin/env python3
import re
import sys
from napari.__main__ import _run

if __name__ == '__main__':
    print(sys.argv[0])
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(_run())
