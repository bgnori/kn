
from decorator import decorator


instructions = {}

def bytecode(bytepattern):
  def wrapper(f):
    instructions[bytepattern] = f
    return f
  return wrapper

@bytecode('0')
def stop(vm):
  assert False

@bytecode('1')
def nop(vm):
  print 'this is nop'
  pass

@bytecode('2')
def prn(vm):
  print vm.stack.pop()


class VM:
  def __init__(self, program):
    self.pc = 0
    self.program = program
    self.stack = []
  
  def run(self):
    op = self.program[self.pc]
    while(op != '0'):
      f = instructions[op]
      f(self)
      self.pc += 1
      op = self.program[self.pc]


vm = VM(['1', '0'])

vm.run()

