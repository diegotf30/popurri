import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto

from antlr_parser.PopurriLexer import PopurriLexer
from antlr_parser.PopurriParser import PopurriParser
from PopurriListener import PopurriListener
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from os.path import isfile, basename
from os import devnull
import json
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

    def exportOvejota(self, listener, filename):
        with open(filename, 'w') as f:
            variables = listener.ctxWrapper.variables
            funcs = listener.ctxWrapper.functions
            memory = listener.memHandler.contexts
            quads = listener.quadWrapper.quads
            for arg in [variables, funcs, memory, quads]:
                json.dump(arg, f, default=vars)
                f.write('\n')

    def compile(self, file, export=True):
        if not isfile(file):
            raise Exception(f'Error: {file} not found')

        input_stream = FileStream(file, encoding='utf-8')
        lexer = PopurriLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PopurriParser(stream)
        parser.addErrorListener(PopurriErrorListener())

        tree = parser.program()
        walker = ParseTreeWalker()
        listener = PopurriListener(self.mem_size, debug_info=True)
        walker.walk(listener, tree)

        if export:
            filename = basename(file).replace('.pop', '.pobj')
            self.exportOvejota(listener, filename)
            return filename

