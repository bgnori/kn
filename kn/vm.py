
from decorator import decorator


instructions = {}

def bytecode(bytepattern):
  def wrapper(f):
    instructions[bytepattern] = f
    return f
  return wrapper


@bytecode('1')
def nop(vm):
  print vm
  pass


class VM:
  def __init__(self):
    self.pc = 0
  
  def run(self, program):
    op = program[self.pc]
    while(op):
      f = instructions[op]
      f(self)
      self.pc+=1
      op = program[self.pc]


vm = VM()

vm.run(['1'])

