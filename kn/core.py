
import sys
import yaml

from kn.builtins import builtins, make_builtin


class RuntimeError(Exception):
    pass

class UnboundError(RuntimeError):
    pass

class NotInvokableError(RuntimeError):
    pass

class Scope:
    def __init__(self, initial=None):
        self.blocks = []
        self.push(initial)

    def dump(self):
        for b in reversed(self.blocks):
            print b

    def clone(self):
        x = Scope()
        x.blocks = [b for b in self.blocks]
        return x

    def push(self, d=None):
        '''
            creates new scope block. i.e. let 
        '''
        if d is None:
            d = {}
        self.blocks.append(d)

    def pop(self, count = None):
        assert self.blocks
        if count is None:
            count = 1
        while count:
            self.blocks.pop(-1)
            count -= 1
    
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
                return b[identifier]
            except KeyError:
                pass
        raise KeyError(identifier)



class Evaluator:
    specialForms = ("let", "quote", "fn", "defn", "define", "if",)

    def __init__(self, env=None):
        if env is None:
            env = {}
        self.scope = Scope(env)
        
        self.scope.define("evaluator", self)

    def handleSpecialForms(self, item):
        handler = getattr(self, "handle_"+item[0])
        return handler(item)

    def handle_define(self, item):
        name = item[1]
        value = self.eval(item[2])
        self.define(name, value)

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

    def handle_if(self, item):
        cond = self.eval(item[1])
        if cond: #FIXME !! it maps kn bool to python bool.
            v = self.eval(item[2])
        else:
            v = self.eval(item[3])
        return v

    def handle_fn(self, item):
        d = {
                "__scope__": self.scope.clone(),
                "__param__": item[1],
                "__body__": item[2],
        }
        return d

    def handle_defn(self, item):
        d = {}
        self.define(item[1], d)
        d.update({
                "__scope__": self.scope.clone(),
                "__param__": item[2],
                "__body__": item[3],
        })


    @make_builtin("parse")
    def _parse(self, item):
        ast = yaml.load(item)
        return ast

    @make_builtin("eval")
    def _eval(self, item):
        return self.eval(item)

    def swap(self, scope):
        s = self.scope 
        self.scope = scope
        return s

    def resolve(self, name):
        return self.scope.resolve(name)

    def define(self, name, obj):
        self.scope.define(name, obj)

    def eval(self, item):
        print 'eval-----', item
        self.scope.dump()
        type2name = {str:"str", list:"list", dict:"dict", int:"int", type(None):"NoneType"}

        t = type(item)

        name = type2name[t]
        handler = getattr(self, "eval_" + name)
        v = handler(item)

        print '===>', v
        print '---------'
        print
        return v

    def eval_NoneType(self, itme):
        return None

    def eval_str(self, item):
        assert isinstance(item, str)
        if item[0] in ('"', "'"):
            return item.strip(""""'""")
        else:
            try:
                return self.resolve(item)
            except KeyError:
                print "No such identifier"
                print item
                print type(item)
                self.scope.dump()
                print self.specialForms
                print builtins
                raise UnboundError


    def eval_list(self, item):
        assert isinstance(item, list)
    
        if isinstance(item[0], str):
            if item[0] in self.specialForms:
                return self.handleSpecialForms(item)

            if item[0] in builtins:
                obj = builtins[item[0]]
                args = item[1:]
                myevaled = [self.eval(item) for item in args]
                return obj(self, myevaled)

        v = self.eval(item[0])
        return self.apply(v, item[1:])

    def callable(self, obj):
        return isinstance(obj, dict) and "__scope__" in obj and "__param__" in obj and "__body__" in obj

    def apply(self, obj, args):
        if not self.callable(obj):
            raise NotInvokableError

        #setup scope for callee
        my = obj["__scope__"]

        #point is "self.eval(a) may cause some effect on scope"
        my.push(dict(zip(obj["__param__"], [self.eval(a) for a in args])))

        s = self.swap(my) 

        r = self.eval(obj["__body__"])

        self.swap(s) #rewind back scope to caller
        my.pop()
        return r

    def eval_dict(self, item):
        assert isinstance(item, dict)
        return dict([(k, self.eval(v)) for k, v in item.iteritems()])

    def eval_int(self, item):
        return item

    def run(self, s):
        ast = yaml.load(s)
        return self.eval(ast)

