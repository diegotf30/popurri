import popurri_tokens as p_t  # probablemente ni usemos esto
import error_tokens as e  # probablemente si usemos esto

from parser.PopurriLexer import PopurriLexer
from parser.PopurriListener import PopurriListener
from parser.PopurriParser import PopurriParser
from antlr4 import *
import sys

# 10000 direcciones para cada tipo [INT, FLOAT, STRING, BOOL]
MEM_DEFAULT = 10000


class PopurriRuleHandler(PopurriListener):
    '''
    -Esta clase nos permite simular la creacion de tabla de variables
    -[Tal vez podamos usar esta clase para simular la semantica basica de expresiones]
    -Cada funcion 'enter' representa el estado cuando se inicia una  regla
    -Cada funcion 'exit' representa el estado cuando se acaba una regla
    -[global_dir] es el directorio global [module, declarations, classes, functions]
    -[local_dir] es el directorio local de una clase [declarations, functions]
    -[var_dir] es el directorio de variables de una funcion [declarations]
    '''

    def __init__(self, global_dir=None, mem_size=MEM_DEFAULT):
        '''
        *- [global_dir] es el directorio global [declarations, classes, functions]
        '''
        self.global_dir = global_dir
        self.mem_size = mem_size

    def enterModule(self, ctx):
        pass

    def exitModule(self, ctx):

        pass

    def enterProgram(self, ctx):

        # Inicializa las direcciones globales [no es necesario hacerlo explicito]
        self.global_dir = {}
        pass

    def exitProgram(self, ctx):

        # Libera la memoria del compilador [Elimina las entradas de la tabla de direccines globales]
        self.global_dir.clear()
        pass

    def enterDeclarations(self, ctx):
        pass

    def exitDeclarations(self, ctx):
        pass

    def enterDeclaration(self, ctx):
        pass

    def exitDeclaration(self, ctx):
        pass

    def enterClass(self, ctx):
        pass

    def exitClass(self, ctx):
        pass

    def enterParent(self, ctx):
        pass

    def exitParent(self, ctx):
        pass

    def enterFunction(self, ctx):
        pass

    def exitFunction(self, ctx):
        pass

    def enterStatement(self, ctx):
        pass

    def exitStatement(self, ctx):
        pass

    def enterAccessType(self, ctx):
        pass

    def exitAccesType(self, ctx):
        pass

    def enterReturn(self, ctx):
        pass

    def exitReturn(self, ctx):
        pass

    def enterPrint(self, ctx):
        pass

    def exitPrint(self, ctx):
        pass

    def enterInput(self, ctx):
        pass

    def exitInput(self, ctx):
        pass

    def enterIndexation(self, ctx):
        pass

    def exitIndexation(self, ctx):
        pass

    def enterAttribute(self, ctx):
        pass

    def exitAttribute(self, ctx):
        pass

    def enterType(self, ctx):
        pass

    def exitType(self, ctx):
        pass

    def enterIterable(self, ctx):
        pass

    def exitIterable(self, ctx):
        pass

    def enterFuncCall(self, ctx):
        pass

    def exitFuncCall(self, ctx):
        pass

    def enterWhile(self, ctx):
        pass

    def exitWhile(self, ctx):
        pass

    def enterFor(self, ctx):
        pass

    def exitFor(self, ctx):
        pass

    def enterBranch(self, ctx):
        pass

    def exitBranch(self, ctx):
        pass

    def enterIf(self, ctx):
        pass

    def exitIf(self, ctx):
        pass

    def enterElseIf(self, ctx):
        pass

    def exitElseIf(self, ctx):
        pass

    def enterElse(self, ctx):
        pass

    def exitElse(self, ctx):
        pass

    def enterCond(self, ctx):
        pass

    def exitCond(self, ctx):
        pass

    def enterCmp(self, ctx):
        pass

    def exitCmp(self, ctx):
        pass

    def enterExp(self, ctx):
        pass

    def exitExp(self, ctx):
        pass

    def enterAdd(self, ctx):
        pass

    def exitAdd(self, ctx):
        pass

    def enterMultModDiv(self, ctx):
        pass

    def exitMultModDiv(self, ctx):
        pass

    def enterVal(self, ctx):
        pass

    def exitVal(self, ctx):
        pass

    def enterConst(self, ctx):
        pass

    def exitConst(self, ctx):
        pass

    def enterConst_i(self, ctx):
        pass

    def exitConst_i(self, ctx):
        pass

    def enterConst_f(self, ctx):
        pass

    def exitConst_f(self, ctx):
        pass

    def enterConst_str(self, ctx):
        pass

    def exitConst_str(self, ctx):
        pass

    def enterConst_bool(self, ctx):
        pass

    def exitConst_bool(self, ctx):
        pass

    def enterConst_arr(self, ctx):
        pass

    def exitConst_arr(self, ctx):
        pass

    def enterId(self, ctx):
        pass

    def exitId(self, ctx):
        pass

    def enterCondParam(self, ctx):
        pass

    def exitCondParam(self, ctx):
        pass

    def enterCmpOp(self, ctx):
        pass

    def exitCmpOp(self, ctx):
        pass

    def enterAddOp(self, ctx):
        pass

    def exitAddOp(self, ctx):
        pass

    def enterAssignOp(self, ctx):
        pass

    def exitAssignOp(self, ctx):
        pass

    def enterBoolOp(self, ctx):
        pass

    def exitBoolOp(self, ctx):
        pass

    def enterFuncParams(self, ctx):
        pass

    def exitFuncParams(self, ctx):
        pass


class Compiler(object):
    def __init__(self, mem_size=MEM_DEFAULT):
        self.int_mem_counter = 0
        self.float_mem_counter = 0
        self.string_mem_counter = 0
        self.bool_mem_counter = 0

    def compile(self, file):
        input_stream = FileStream(file, encoding='utf-8')
        lexer = PopurriLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PopurriParser(stream)

        tree = parser.program()
        walker = ParseTreeWalker()
        walker.walk(PopurriRuleHandler(), tree)
        if parser.getNumberOfSyntaxErrors() is 0:
            print("Compiled successfully!")

if __name__ == '__main__':
    compiler = Compiler()
    compiler.compile(sys.argv[1])
