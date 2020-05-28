from compiler import Compiler
from virtual_machine import run
import sys

if __name__ == '__main__':
    compiler = Compiler()
    filename = compiler.compile(sys.argv[1])
    print('Compiled successfully!')
    run(filename)