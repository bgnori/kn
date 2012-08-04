
from decorator import decorator
import struct

def quad(n):
  return struct.pack('@q', n),

instructions = {}


def bytecode(bytepattern):
  def wrapper(f):
    instructions[bytepattern] = f
    return f
  return wrapper

OP_STOP = quad(0)
@bytecode(OP_STOP)
def stop(vm):
  assert False

OP_NOP = quad(1)
@bytecode(OP_NOP)
def nop(vm):
  print 'this is nop'
  pass

OP_PRN = quad(2)
@bytecode(OP_PRN)
def prn(vm):
  print vm.stack.pop()


OP_ZERO = quad(3)
@bytecode(OP_ZERO)
def prn(vm):
  #vm.stack.push(0)
  vm.stack.append(0)

OP_ONE = quad(4)
@bytecode(OP_ONE)
def prn(vm):
  vm.stack.append(1)


class VM:
  def __init__(self, program):
    self.pc = 0
    self.program = program
    self.stack = []
  
  def run(self):
    op = self.program[self.pc]
    while(op != OP_STOP):
      f = instructions[op]
      f(self)
      self.pc += 1
      op = self.program[self.pc]

p = [OP_ZERO, OP_PRN, OP_STOP]

vm = VM(p)

vm.run()

