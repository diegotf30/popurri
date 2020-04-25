from antlr4 import *
from parser.PopurriLexer import PopurriLexer
from parser.PopurriListener import PopurriListener
from parser.PopurriParser import PopurriParser

import sys

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = PopurriLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PopurriParser(stream)
    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() is 0:
        print("Compiled successfully!")

if __name__ == '__main__':
    main(sys.argv)