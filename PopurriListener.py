from antlr4 import *
from parser.PopurriParser import PopurriParser
from popurri_tokens import *
import json

def pprint(*args):
    for arg in args:
        print(json.dumps(arg.__dict__, indent=2))

class Variable():
    def __init__(self, id, type=None, value=None, context="global"):
        self.id = id
        self.type = type
        self.value = value
        self.context = context

class Object():
    attributes = []
    fuctions = []

    def __init__(self, id, parent_id=None):
        self.id = id
        self.parent_id = parent_id 

class PopurriListener(ParseTreeListener):
    '''
    -Esta clase nos permite simular la creacion de tabla de variables
    -[Tal vez podamos usar esta clase para simular la semantica basica de expresiones]
    -Cada funcion 'enter' representa el estado cuando se inicia una  regla
    -Cada funcion 'exit' representa el estado cuando se acaba una regla
    '''
    memory = {
        "vars": [],
        "classes": [],
        "functions": []
    }


    def enterProgram(self, ctx:PopurriParser.ProgramContext):
        '''
        [Program] marca el inicio de las reglas de la gramatica. Aqui inicia la fase de compilacion.
        '''
        print('program')
        pass

    def exitProgram(self, ctx:PopurriParser.ProgramContext):
        '''
        [Program] marca el final de las reglas de la gramatica. Aqui termina la fase de compilacion.
        '''
        pass

    def enterModule(self, ctx:PopurriParser.ModuleContext):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module')
        pass

    def exitModule(self, ctx:PopurriParser.ModuleContext):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module exit')
        pass

    def enterDeclarations(self, ctx:PopurriParser.DeclarationsContext):
        pass

    def exitDeclarations(self, ctx:PopurriParser.DeclarationsContext):
        pass

    def enterDeclaration(self, ctx:PopurriParser.DeclarationContext):
        # Checks if var is already created in mem_slots
        if any(var.id is str(ctx.ID()) for var in self.memory["vars"]):
            raise 'ERROR VAR ALREADY CREATED'

        new_variable = ""
        # var has data_type : INT, FLOAT, STRING, BOOL
        # TODO: Arrays are not yet implemented
        if ctx.TYPE() is not None:
            new_variable = Variable(
                id=str(ctx.ID()[0]),
                type=str(ctx.TYPE())
            )
        # var is type object
        else:
            new_variable = Variable(
                id=str(ctx.ID()[0]),
                type=str(ctx.ID()[1])
            )

        self.memory["vars"].append(new_variable)
        pprint(new_variable)
        print('declaration')

    def exitDeclaration(self, ctx:PopurriParser.DeclarationContext):
        pass

    def enterFunction(self, ctx:PopurriParser.FunctionContext):
        pass

    def exitFunction(self, ctx:PopurriParser.FunctionContext):
        pass

    def enterClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        new_class = Object(id=str(ctx.ID()))
        if ctx.parent() is not None:
            new_class.parent_id = str(ctx.parent().ID())

        self.memory["classes"].append(new_class)
        print('class')
        pass

    def exitClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        pass

    def enterParent(self, ctx:PopurriParser.ParentContext):
        pass

    def exitParent(self, ctx:PopurriParser.ParentContext):
        pass

    def enterAccessType(self, ctx:PopurriParser.AccessTypeContext):
        pass

    def exitAccessType(self, ctx:PopurriParser.AccessTypeContext):
        pass

    def enterAttributes(self, ctx:PopurriParser.AttributesContext):
        pass

    def exitAttributes(self, ctx:PopurriParser.AttributesContext):
        pass

    # HOLD
    def enterAttribute(self, ctx:PopurriParser.AttributeContext):
        print('attribute')

    def exitAttribute(self, ctx:PopurriParser.AttributeContext):
        pass

    def enterStatement(self, ctx:PopurriParser.StatementContext):
        pass

    def exitStatement(self, ctx:PopurriParser.StatementContext):
        pass

    def enterWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass

    def exitWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass

    def enterForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass

    def exitForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass

    def enterBranch(self, ctx:PopurriParser.BranchContext):
        pass

    def exitBranch(self, ctx:PopurriParser.BranchContext):
        pass

    def enterIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass

    def exitIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass

    def enterElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass

    def exitElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass

    def enterElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass

    def exitElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass

    def enterReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass

    def exitReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass

    def enterCond(self, ctx:PopurriParser.CondContext):
        pass

    def exitCond(self, ctx:PopurriParser.CondContext):
        pass

    def enterCmp(self, ctx:PopurriParser.CmpContext):
        pass

    def exitCmp(self, ctx:PopurriParser.CmpContext):
        pass

    def enterExp(self, ctx:PopurriParser.ExpContext):
        pass

    def exitExp(self, ctx:PopurriParser.ExpContext):
        pass

    def enterAdd(self, ctx:PopurriParser.AddContext):
        pass

    def exitAdd(self, ctx:PopurriParser.AddContext):
        pass

    def enterMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass

    def exitMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass

    def enterVal(self, ctx:PopurriParser.ValContext):
        pass

    def exitVal(self, ctx:PopurriParser.ValContext):
        pass

    def enterIndexation(self, ctx:PopurriParser.IndexationContext):
        pass

    def exitIndexation(self, ctx:PopurriParser.IndexationContext):
        pass

    def enterAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass

    def exitAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass

    def enterFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass

    def exitFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass

    def enterBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass

    def exitBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass

    def enterCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass

    def exitCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass

    def enterAddOp(self, ctx:PopurriParser.AddOpContext):
        pass

    def exitAddOp(self, ctx:PopurriParser.AddOpContext):
        pass

    def enterMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass

    def exitMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass

    def enterAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass

    def exitAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass

    def enterConstant(self, ctx:PopurriParser.ConstantContext):
        pass

    def exitConstant(self, ctx:PopurriParser.ConstantContext):
        pass

    def enterConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass

    def exitConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass

    def enterIterable(self, ctx:PopurriParser.IterableContext):
        pass

    def exitIterable(self, ctx:PopurriParser.IterableContext):
        pass

    def enterPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass

    def exitPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass

    def enterInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass

    def exitInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass

    def enterCondParam(self, ctx:PopurriParser.CondParamContext):
        pass

    def exitCondParam(self, ctx:PopurriParser.CondParamContext):
        pass

    def enterFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass

    def exitFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass
