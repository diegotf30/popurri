from compiler import Compiler
from virtual_machine import run
import sys

if __name__ == '__main__':
    compiler = Compiler()
    try:
        filename = compiler.compile(sys.argv[1], debug=False)
        print('Compiled successfully!')
    except Exception as e:
        print('Failed to compile!')
        print('Got error:', e)
        exit(1)

    run(filename)