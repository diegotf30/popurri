import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto

from antlr_parser.PopurriLexer import PopurriLexer
from antlr_parser.PopurriParser import PopurriParser
from PopurriListener import PopurriListener
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from os.path import isfile, basename
import sys

# 10000 direcciones para cada tipo [INT, FLOAT, STRING, BOOL]
MEM_DEFAULT = 10000

class PopurriErrorListener(ErrorListener):
    def __init__(self):
        super(PopurriErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print('Terminating compilation because of syntax error')
        sys.exit(1)

class Compiler(object):
    def __init__(self, mem_size=MEM_DEFAULT):
        self.mem_size = mem_size

    def compile(self, file):
        if not isfile(file):
            raise Exception(f'Error: {file} not found')

        input_stream = FileStream(file, encoding='utf-8')
        lexer = PopurriLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PopurriParser(stream)
        parser.addErrorListener(PopurriErrorListener())

        tree = parser.program()
        walker = ParseTreeWalker()
        listener = PopurriListener(self.mem_size)
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
