import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto

from parser.PopurriLexer import PopurriLexer
from parser.PopurriParser import PopurriParser
from PopurriListener import PopurriListener
from antlr4 import *
import sys

# 10000 direcciones para cada tipo [INT, FLOAT, STRING, BOOL]
MEM_DEFAULT = 10000


class Compiler(object):
    def __init__(self, mem_size=MEM_DEFAULT):
        self.mem_size = mem_size
        self.int_mem_counter = self.float_mem_counter = self.string_mem_counter = self.bool_mem_counter = 0
        self.int_mem_slots = self.float_mem_slots = self.string_mem_slots = self.bool_mem_slots = [
            None] * mem_size

    def compile(self, file):
        input_stream = FileStream(file, encoding='utf-8')
        lexer = PopurriLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PopurriParser(stream)

        tree = parser.program()
        walker = ParseTreeWalker()
        listener = PopurriListener()
        walker.walk(listener, tree)
        return parser.getNumberOfSyntaxErrors()


if __name__ == '__main__':
    compiler = Compiler()
    try:
        compiler.compile(sys.argv[1])
    except Exception as e:
        print('Failed to compile!')
        print('Got error:', e)
        exit(1)
