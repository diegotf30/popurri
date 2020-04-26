# Generated from Popurri.g4 by ANTLR 4.7.1
from antlr4 import *
from parser.PopurriParser import PopurriParser

# This class defines a complete listener for a parse tree produced by PopurriParser.
class PopurriListener(ParseTreeListener):
    '''
    -Esta clase nos permite simular la creacion de tabla de variables
    -[Tal vez podamos usar esta clase para simular la semantica basica de expresiones]
    -Cada funcion 'enter' representa el estado cuando se inicia una  regla
    -Cada funcion 'exit' representa el estado cuando se acaba una regla
    -[global_dir] es el directorio global [module, declarations, classes, functions]
    -[local_dir] es el directorio local de una clase [declarations, functions]
    -[var_dir] es el directorio de variables de una funcion [declarations]
    '''
def __init__(self, mem_slots=None, mem_size=None):
        '''
        *- [global_dir] es el directorio global [declarations, classes, functions]
        '''
        self.mem_slots = mem_slots
        self.mem_ptr_dict = {
            INT: 0,
            FLOAT: mem_size,
            STRING: mem_size * 2,
            BOOL: mem_size * 3
        }
        self.global_dir_ptr = 0
        self.curr_level_global = True

    def getSymbolFromStr(self, symbol_str=None):
        symbolTable = ['', 'int', 'float', 'string', 'bool']
        if symbol_str is None:
            return None
        return symbolTable.index(str(symbol_str))

    def getGlobalPtrFromId(self, id=None):
        for iterator in range(len(self.global_dir)):
            if id is self.global_dir[iterator]['id']:
                return iterator
        return None

    def enterModule(self, ctx):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module')
        pass

    def exitModule(self, ctx):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module exit')
        pass

    def enterProgram(self, ctx):
        '''
        [Program] marca el inicio de las reglas de la gramatica. Aqui inicia la fase de compilacion.
        '''
        # Inicializa las direcciones globales [no es necesario hacerlo explicito]
        self.global_dir = [
            {
                'id': 'global',
                'declarations': [],
                'classes': [],
                'functions': [],
                'statements': [],
            },
        ]
        print('program')
        pass

    def exitProgram(self, ctx):
        '''
        [Program] marca el final de las reglas de la gramatia. Aqui termina la fase de compilacion.
        '''
        # Libera la memoria del compilador [Elimina las entradas de la tabla de direccines globales]
        self.global_dir.clear()
        self.mem_slots = []
        pass

    def enterDeclarations(self, ctx):
        pass

    def exitDeclarations(self, ctx):
        pass

    def enterDeclaration(self, ctx):

        print(ctx.TYPE())
        # Checks if var is already created in mem_slots
        for slot in self.mem_slots:
            if slot[0] is ctx.ID():
                raise 'ERROR VAR ALREADY CREATED'

        # Creates var
        symbol_token = self.getSymbolFromStr(ctx.TYPE())
        self.mem_slots[self.mem_ptr_dict[symbol_token]] = (ctx.ID(), 0)
        self.global_dir[self.global_dir_ptr]['declarations'].append(
            self.mem_ptr_dict[symbol_token])

        # increments the ptr for ctx.TYPE()in mem_ptr_dict
        self.mem_ptr_dict[symbol_token] += 1

        # Check if everything is correct[Debugging]
        print(self.global_dir, self.mem_ptr_dict)
        print('declaration')

    def exitDeclaration(self, ctx):
        pass

    def enterClassDeclaration(self, ctx):
        print('class')

        created_class = {
            'type': 'class',
            'id': None,
            'class_parent': None,
            'node_parent': 0,
            'attributes': [],
            'functions': [],
        }
        created_class['id'] = str(ctx.ID())

        if ctx.parent() is not None:
            created_class['class_parent'] = self.getGlobalPtrFromId(
                ctx.parent())
            if created_class['class_parent'] is None:
                print('Error')

        self.global_dir.append(created_class)
        self.global_dir_ptr = len(self.global_dir) - 1
        self.global_dir[created_class['node_parent']
                        ]['classes'].append(self.global_dir_ptr)
        print(self.global_dir, self.mem_ptr_dict, self.global_dir_ptr)

    def exitClassDeclaration(self, ctx):
        self.global_dir_ptr = 0
        pass

    def enterParent(self, ctx):
        self.global_dir[self.global_dir_ptr]['parent'] = str(ctx.ID())
        pass

    # Exit a parse tree produced by PopurriParser#parent.
    def exitParent(self, ctx:PopurriParser.ParentContext):
        pass


    # Enter a parse tree produced by PopurriParser#accessType.
    def enterAccessType(self, ctx:PopurriParser.AccessTypeContext):
        pass

    # Exit a parse tree produced by PopurriParser#accessType.
    def exitAccessType(self, ctx:PopurriParser.AccessTypeContext):
        pass


    # Enter a parse tree produced by PopurriParser#attributes.
    def enterAttributes(self, ctx:PopurriParser.AttributesContext):
        pass

    # Exit a parse tree produced by PopurriParser#attributes.
    def exitAttributes(self, ctx:PopurriParser.AttributesContext):
        pass


    # Enter a parse tree produced by PopurriParser#attribute.
    def enterAttribute(self, ctx:PopurriParser.AttributeContext):
        pass

    # Exit a parse tree produced by PopurriParser#attribute.
    def exitAttribute(self, ctx:PopurriParser.AttributeContext):
        pass


    # Enter a parse tree produced by PopurriParser#statement.
    def enterStatement(self, ctx:PopurriParser.StatementContext):
        pass

    # Exit a parse tree produced by PopurriParser#statement.
    def exitStatement(self, ctx:PopurriParser.StatementContext):
        pass


    # Enter a parse tree produced by PopurriParser#whileLoop.
    def enterWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by PopurriParser#whileLoop.
    def exitWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by PopurriParser#forLoop.
    def enterForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass

    # Exit a parse tree produced by PopurriParser#forLoop.
    def exitForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass


    # Enter a parse tree produced by PopurriParser#branch.
    def enterBranch(self, ctx:PopurriParser.BranchContext):
        pass

    # Exit a parse tree produced by PopurriParser#branch.
    def exitBranch(self, ctx:PopurriParser.BranchContext):
        pass


    # Enter a parse tree produced by PopurriParser#ifStmt.
    def enterIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#ifStmt.
    def exitIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#elseIf.
    def enterElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass

    # Exit a parse tree produced by PopurriParser#elseIf.
    def exitElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass


    # Enter a parse tree produced by PopurriParser#elseStmt.
    def enterElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#elseStmt.
    def exitElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#returnStmt.
    def enterReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#returnStmt.
    def exitReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#cond.
    def enterCond(self, ctx:PopurriParser.CondContext):
        pass

    # Exit a parse tree produced by PopurriParser#cond.
    def exitCond(self, ctx:PopurriParser.CondContext):
        pass


    # Enter a parse tree produced by PopurriParser#cmp.
    def enterCmp(self, ctx:PopurriParser.CmpContext):
        pass

    # Exit a parse tree produced by PopurriParser#cmp.
    def exitCmp(self, ctx:PopurriParser.CmpContext):
        pass


    # Enter a parse tree produced by PopurriParser#exp.
    def enterExp(self, ctx:PopurriParser.ExpContext):
        pass

    # Exit a parse tree produced by PopurriParser#exp.
    def exitExp(self, ctx:PopurriParser.ExpContext):
        pass


    # Enter a parse tree produced by PopurriParser#add.
    def enterAdd(self, ctx:PopurriParser.AddContext):
        pass

    # Exit a parse tree produced by PopurriParser#add.
    def exitAdd(self, ctx:PopurriParser.AddContext):
        pass


    # Enter a parse tree produced by PopurriParser#multModDiv.
    def enterMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass

    # Exit a parse tree produced by PopurriParser#multModDiv.
    def exitMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass


    # Enter a parse tree produced by PopurriParser#val.
    def enterVal(self, ctx:PopurriParser.ValContext):
        pass

    # Exit a parse tree produced by PopurriParser#val.
    def exitVal(self, ctx:PopurriParser.ValContext):
        pass


    # Enter a parse tree produced by PopurriParser#indexation.
    def enterIndexation(self, ctx:PopurriParser.IndexationContext):
        pass

    # Exit a parse tree produced by PopurriParser#indexation.
    def exitIndexation(self, ctx:PopurriParser.IndexationContext):
        pass


    # Enter a parse tree produced by PopurriParser#assignment.
    def enterAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PopurriParser#assignment.
    def exitAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PopurriParser#funcCall.
    def enterFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass

    # Exit a parse tree produced by PopurriParser#funcCall.
    def exitFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass


    # Enter a parse tree produced by PopurriParser#boolOp.
    def enterBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#boolOp.
    def exitBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#cmpOp.
    def enterCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#cmpOp.
    def exitCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#addOp.
    def enterAddOp(self, ctx:PopurriParser.AddOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#addOp.
    def exitAddOp(self, ctx:PopurriParser.AddOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#multDivOp.
    def enterMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#multDivOp.
    def exitMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#assignOp.
    def enterAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#assignOp.
    def exitAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#constant.
    def enterConstant(self, ctx:PopurriParser.ConstantContext):
        pass

    # Exit a parse tree produced by PopurriParser#constant.
    def exitConstant(self, ctx:PopurriParser.ConstantContext):
        pass


    # Enter a parse tree produced by PopurriParser#const_arr.
    def enterConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass

    # Exit a parse tree produced by PopurriParser#const_arr.
    def exitConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass


    # Enter a parse tree produced by PopurriParser#iterable.
    def enterIterable(self, ctx:PopurriParser.IterableContext):
        pass

    # Exit a parse tree produced by PopurriParser#iterable.
    def exitIterable(self, ctx:PopurriParser.IterableContext):
        pass


    # Enter a parse tree produced by PopurriParser#printStmt.
    def enterPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#printStmt.
    def exitPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#inputStmt.
    def enterInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#inputStmt.
    def exitInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#condParam.
    def enterCondParam(self, ctx:PopurriParser.CondParamContext):
        pass

    # Exit a parse tree produced by PopurriParser#condParam.
    def exitCondParam(self, ctx:PopurriParser.CondParamContext):
        pass


    # Enter a parse tree produced by PopurriParser#funcParams.
    def enterFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass

    # Exit a parse tree produced by PopurriParser#funcParams.
    def exitFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass
