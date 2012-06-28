
import decorator

builtins = {}

def builtin(name):
    def decorated(f):
        builtins[name] = f
        return f
    return decorated

@builtin('+')
def add(x, y):
  return x + y


@builtin('-')
def sub(x, y):
  return x - y


