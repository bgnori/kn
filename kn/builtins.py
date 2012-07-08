
import decorator

builtins = {}

def builtin(name):
    def decorated(target_function):
        def adapter(item):
            return target_function(*item)
        builtins[name] = adapter
        return adapter
    return decorated

@builtin('prn')
def prn(x):
    print x
    return None

@builtin('eq')
def eq(x, y):
    return x == y

@builtin('+')
def add(x, y):
    return x + y

@builtin('-')
def sub(x, y):
    return x - y

@builtin('open')
def topen(f):
    return open(f)

@builtin('close')
def tclose(f):
    return f.close()

@builtin('read')
def tread(f):
    x = f.read()
    return x 
