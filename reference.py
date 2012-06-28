
import yaml
import sys

from builtins import builtins


class Evaluator:
    specialForms = ("let", "quote", "defn")

    def __init__(self, env):
        self.env = env

    def handleSpecialForms(self, item):
        handler = getattr(self, item[0])
        return handler(item)

    def let(self, item):
        name = item[1]
        value = self.eval(item[2])
        self.define(name, value)
        return None

    def quote(self, item):
        return item[1]

    def defn(self, item):
        params = item[2]
        body = item[3]
        def foo(item):
            for k, v in dict(zip(params, item)).iteritems():
                self.define(k, v)
            r = self.eval(body) #, scope) #FIXME
            return r
        self.define(item[1], foo)

    def resolve(self, name):
        return self.env.get(name, None)

    def define(self, name, obj):
        self.env[name] = obj
        return None


    def call(self, item):
        if len(item) == 0:
            return 
        name = item[0]
        args = item[1:]

        func = self.resolve(name)
        if not func:
            func = builtins.get(name, None)

        if not func:
            print "No such function"
            print self.evn
            sys.exit(1)
        
        myevaled = [self.eval(item) for item in args]

        return func(myevaled)

    def mapping(self, d):
        return dict([(k, self.eval(v)) for k, v in d.iteritems()])

    def eval(self, item):
        if False:
            pass
        elif isinstance(item, str):
            if item[0] in ('"', "'"):
                return item.strip(""""'""")
            else:
                return self.resolve(item)
        elif isinstance(item, list):
            if len(item) == 0:
                return item
            elif item[0] in self.specialForms:
                return self.handleSpecialForms(item)
            else:
                return self.call(item)

        elif isinstance(item, dict):
            return self.mapping(item)

        elif isinstance(item, int):
            return item
        else:
            pass

    def run(self, s):
        ast = yaml.load(s)
        #print ast
        return self.eval(ast)



'''
class Parser:
with open(sys.argv[1]) as f:
    src = yaml.load(f)
    print src

    for item in src:
        print myeval(item, environ)

'''
