
import yaml
import sys

from builtins import builtins

specials = {"let":None, "quote":None, "defn": None}





def handle_special(item, environ):
    if item[0] == 'let':
        name = item[1]
        value = item[2]
        environ[name]=value #FIXME
    elif item[0] == 'quote':
        return item[1]
    elif item[0] == 'defn':
        params = item[2]
        body = item[3]
        def foo(item, environ):
            scope = dict(zip(params, item))
            for b in body:
                r = myeval(b, scope) #FIXME
            return r
        environ[item[1]] = foo
    else:
        pass

    return None

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
        print environ
        sys.exit(1)
    
    myevaled = [myeval(item, environ) for item in args]

    return func(myevaled, environ)

def new(d, environ):
    return dict([(k, myeval(v, environ)) for k, v in d.iteritems()])

def myeval(item, environ):
    if isinstance(item, list):
        if len(item) == 0:
            return []
        elif item[0] in specials:
            return handle_special(item, environ)
        else:
            return call(item, environ)

    elif isinstance(item, dict):
        return new(item, environ)

    elif isinstance(item, int):
        return item
    elif isinstance(item, str):
        if item[0] in ('"', "'"):
            return item
        else:
            return environ[item]
    else:
        pass


environ = {}
with open(sys.argv[1]) as f:
    src = yaml.load(f)
    print src

    for item in src:
        print myeval(item, environ)

