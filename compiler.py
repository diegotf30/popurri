import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto

from parser.PopurriLexer import PopurriLexer
from popurriRuleHandler import PopurriRuleHandler
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
        listener = PopurriListener(mem_size=self.mem_size, mem_slots=[(None, None)] * self.mem_size * 4)
        walker.walk(listener, tree)
        if parser.getNumberOfSyntaxErrors() is 0:
            print("Compiled successfully!")


if __name__ == '__main__':
    compiler = Compiler()
    compiler.compile(sys.argv[1])
