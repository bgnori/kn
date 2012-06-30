
import yaml
import sys

from builtins import builtins


class Scope:
    def __init__(self, initial=None):
        self.blocks = []
        self.push(initial)

    def dump(self):
        for b in reversed(self.blocks):
            print b

    def clone(self):
        x = Scope()
        x.blocks = [dict(b) for b in self.blocks]
        return x

    def push(self, d=None):
        '''
            creates new scope block. i.e. let 
        '''
        if d is None:
            d = {}
        self.blocks.append(d)

    def pop(self):
        assert self.blocks
        self.blocks.pop(-1)
    
    def top(self):
        assert self.blocks
        return self.blocks[-1]

    def define(self, identifier, obj):
        assert self.blocks
        b = self.top()
        b[identifier] = obj

    def resolve(self, identifier):
        assert self.blocks
        for b in reversed(self.blocks):
            try:
                obj = b[identifier]
            except KeyError:
                pass
        try:
            return obj
        except UnboundLocalError:
            raise KeyError(identifier)


class Evaluator:
    specialForms = ("let", "quote", "defn")

    def __init__(self, env=None):
        if env is None:
            env = {}
        self.scope = Scope(env)

    def handleSpecialForms(self, item):
        handler = getattr(self, "handle_"+item[0])
        return handler(item)

    def handle_let(self, item):
        self.scope.push()
        name = item[1]
        value = self.eval(item[2])
        self.define(name, value)
        v = self.eval(item[3])
        self.scope.pop()
        return v

    def handle_quote(self, item):
        return item[1]

    def handle_defn(self, item):
        d = {
                "__scope__": self.scope.clone(),
                "__param__": item[2],
                "__body__": item[3],
        }
        self.define(item[1], d)

    def swap(self, scope):
        s = self.scope 
        self.scope = scope
        return s

    def resolve(self, name):
        return self.scope.resolve(name)

    def define(self, name, obj):
        self.scope.define(name, obj)

    def eval(self, item):
        type2name = {str:"str", list:"list", dict:"dict", int:"int", type(None):"NoneType"}

        t = type(item)

        name = type2name[t]
        handler = getattr(self, "eval_" + name)
        return handler(item)

    def eval_NoneType(self, itme):
        return None

    def eval_str(self, item):
        assert isinstance(item, str)
        if item[0] in ('"', "'"):
            return item.strip(""""'""")
        else:
            return self.resolve(item)

    def eval_list(self, item):
        assert isinstance(item, list)

        if len(item) == 0:
            return item

        if item[0] in self.specialForms:
            return self.handleSpecialForms(item)

        if item[0] in builtins:
            obj = builtins[item[0]]
            args = item[1:]
            myevaled = [self.eval(item) for item in args]
            return obj(myevaled)

        try:
            obj = self.resolve(item[0])
        except:
            print "No such identifier"
            print item[0]
            print type(item[0])
            self.scope.dump()
            raise

        if isinstance(obj, dict) and \
            "__scope__" in obj and \
            "__param__" in obj and \
            "__body__" in obj:
            args = item[1:]
            myevaled = [self.eval(a) for a in args]

            v = self.call_object(obj, myevaled)
            return v

        return [self.eval(v) for v in item]

    def call_object(self, obj, args):

        s = self.swap(obj["__scope__"])
        for k, v in dict(zip(obj["__param__"], args)).iteritems():
            self.define(k, v)
        r = self.eval(obj["__body__"])
        self.swap(s)
        return r

    def eval_dict(self, item):
        assert isinstance(item, dict)
        return dict([(k, self.eval(v)) for k, v in item.iteritems()])

    def eval_int(self, item):
        return item

    def run(self, s):
        ast = yaml.load(s)
        print ast
        return self.eval(ast)



