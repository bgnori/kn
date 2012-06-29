
import yaml
import sys

from builtins import builtins

class Scope:
    def __init__(self, initial):
        self.map = initial

    def define(self, identifier, obj):
        self.map[identifier] = obj

    def resolve(self, identifier):
        return self.map[identifier]

    def clone(self):
        return dict(self.map)

class Frame: #UGH! bad name, may be.
    def __init__(self, initial=None):
        self.scopes = []
        if initial is None:
            initial = {}
        self.push(Scope(initial))

    def push(self, scope):
        self.scopes.append(scope)

    def pop(self):
        self.scopes.pop(-1)

    def clone(self):
        f = Frame()
        f.scopes = [s.clone() for s in self.scopes]
        return f

    def define(self, identifier, obj):
        s = self.scopes[-1]
        s.define(identifier, obj)

    def resolve(self, identifier):
        '''
            searchs identifier from top scope to bottom scope
        '''
        for scope in reversed(self.scopes):
            try:
                obj = scope.resolve(identifier)
            except KeyError:
                pass
        try:
            return obj
        except UnboundLocalError:
            raise KeyError(identifier)


class Evaluator:
    specialForms = ("let", "quote", "defn")

    def __init__(self, env=None):
        self.frames = []
        if env is None:
            env = {}
        self.new_frame(env)

    def top_frame(self):
        return self.frames[-1]

    def new_frame(self, initial):
        self.frames.append(Frame(initial))

    def pop_frame(self):
        self.frames.pop(-1)

    def clone_e(self):
        e = [f.clone() for f in self.frames]
        return e

    def handleSpecialForms(self, item):
        handler = getattr(self, "handle_"+item[0])
        return handler(item)

    def handle_let(self, item):
        self.top_frame().push(Scope({})) #FIXME
        name = item[1]
        value = self.eval(item[2])
        self.define(name, value)
        v = self.eval(item[3])
        self.top_frame().pop()
        return v

    def handle_quote(self, item):
        return item[1]

    def handle_defn(self, item):
        params = item[2]
        body = item[3]
        e = self.clone_e()
        def foo(item):
            for k, v in dict(zip(params, item)).iteritems():
                self.define(k, v)
            r = self.eval(body) #, scope) #FIXME
            return r
        self.define(item[1], foo)

    def resolve(self, name):
        return self.top_frame().resolve(name)

    def define(self, name, obj):
        self.top_frame().define(name, obj)
        return None


    def call(self, item):
        if len(item) == 0:
            return 
        name = item[0]
        args = item[1:]

        try:
            func = self.resolve(name)
        except KeyError:
            func = None
        if not func:
            func = builtins.get(name, None)

        if not func:
            print "No such function"
            print self.evn
            sys.exit(1)
        
        myevaled = [self.eval(item) for item in args]

        self.new_frame({})
        v = func(myevaled)

        return v

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
