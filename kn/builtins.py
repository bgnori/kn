
import decorator

builtins = {}

def make_builtin(name):
    def decorated(target_function):
        def adapter(evaluator, item):
            return target_function(evaluator, *item)
        builtins[name] = adapter
        return adapter
    return decorated

@make_builtin('prn')
def prn(evaluator, x):
    print x
    return None

@make_builtin('eq')
def eq(evaluator, x, y):
    return x == y

@make_builtin('+')
def add(evaluator, x, y):
    return x + y

@make_builtin('mul')
def mul(evaluator, x, y):
    return x * y

@make_builtin('-')
def sub(evaluator, x, y):
    return x - y

@make_builtin('open')
def topen(evaluator, f):
    return open(f)

@make_builtin('close')
def tclose(evaluator, f):
    return f.close()

@make_builtin('read')
def tread(evaluator, f):
    return f.read()
