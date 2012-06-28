
import decorator

builtins = {}

def builtin(name):
    def decorated(f):
        def adapter(item, environ):
            return f(*item)
        builtins[name] = adapter
        return adapter
    return decorated

@builtin('+')
def add(x, y):
  return x + y

@builtin('-')
def sub(x, y):
  return x - y

@builtin('*')
def mul(x, y):
  return x * y

@builtin('/')
def div(x, y):
  return x / y

