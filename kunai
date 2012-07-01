#!/usr/bin/python


from reference import Evaluator
from argparse import ArgumentParser

import sys

parser = ArgumentParser(description="Starting kn. kn is yaml based lisp like thing...")

parser.add_argument("script", nargs="?", default=None,
    help="script file name to run. if not available, it uses stdin.")
parser.add_argument("-version", action='version', version='%(prog)s 0.0')

m = parser.parse_args()

ev = Evaluator()

if m.script is None:
    ev.run(sys.stdin)
else:
    with open(m.script) as f:
        ev.run(f)
