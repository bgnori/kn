
import yaml
import sys

from builtins import builtins




def call(item, environ):
    if len(item) == 0:
        return 
    name = item[0]
    args = item[1:]

    func = environ.get(name, None)
    if not func:
        func = builtins.get(name, None)

    if not func:
        print "No such function"
        sys.exit(1)
    
    return func(*args)


def eval(item, environ):
    if isinstance(item, list):
        return call(item, environ)
    elif isinstance(item, dict):
        return define(item, environ)
    elif isinstance(item, int):
        return item
    elif isinstance(item, str):
        return item
    else:
        pass


environ = {}
with open(sys.argv[1]) as f:
    src = yaml.load(f)
    print src

    for item in src:
        print eval(item, environ)

