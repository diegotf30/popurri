from antlr4 import *
from parser.PopurriParser import PopurriParser
from popurri_tokens import *
import json


def pprint(*args):
    for arg in args:
        print(json.dumps(arg, indent=2, default=vars))


def getTypeByToken():
    pass


class FuncTable():
    '''
    Esta es una tabla de procedimientos
    '''

    def __init__(self, default_key_ptr):

        # Apunta al inicio de nuestra tabla global [global]
        self.dir_key_ptr = default_key_ptr

        self.func_table = {}

    def insertProc(self, proc_obj):
        self.func_table[proc_obj.id] = proc_obj

    def changeKeyPtr(self, func_table_id):
        self.dir_key_ptr = func_table_id


class Global():

    def __init__(self, global_id="global"):
        self.id = global_id
        self.attributes = []

    def insertAttribute(self, variable_obj):
        self.attributes.append(variable_obj)


class Variable():
    '''
    Esto nos permite simular la creacion de variables. Inicializandolas con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la actual variable. Ej. var edad : int. Donde edad es el ID.
    [address] es la direccion virtual en el que la variable se encuentra alocada.
    [type] es el tipo de dato con el que la variable estara relacionada. Ej. var edad : int. Donde int es el tipo de dato.
    [value] es el valor inicial que tendra la variable. Ej. var edad = 25. Donde 25 es el valor inicial.
    [context] es el scope en donde la variable estara guardada. Esto permite crear variables unicas dentro de un scope.
    '''

    def __init__(self, id, access_type="public", address=None, type=None, value=None, context="global"):
        self.access_type = access_type
        self.id = str(id)
        self.type = str(type)
        self.value = value
        self.context = str(context)
        self.address = address


class Object():
    '''
    Esto nos permite simular la creacion de clases. Inicializandolos con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la clase actual. Ej. class Humano {}. Donde Humano es el identificador.
    [parent_id] es el identificador del cual la clase actual heredara todas las propiedades. Ej. class Humano -> Persona. Donde Humano es el identificador
    padre.
    [attributes] son todas las variables con las que la clase actual cuenta en su cuerpo. Es una lista de variables.
    [functions] son todas las funciones con las que la clase actual cuenta en su cuerpo. Es una lista de funciones.
    '''

    def __init__(self, id, parent_id=None, attributes=[], functions=[]):
        self.id = str(id)
        self.parent_id = str(parent_id)
        self.attributes = attributes
        self.functions = functions

    def insertAttribute(self, attribute):
        self.attributes.append(attribute)


class Function():
    '''
    Esto nos permite simular la creacion de funciones. Inicializandolas con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la funcion actual. Ej. func habla() {}. Donde habla es el identificador.
    [params] son los parametros que se le enviaran a la funcion actual. Es una lista de parametros.
    [return_type] es el tipo de dato que regresara la funcion al terminar su ejecucion. Void es el tipo predeterminado.
    '''

    def __init__(self, id, params=None, return_type="void"):
        self.id = str(id)
        self.params = params
        self.return_type = str(return_type)


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
        "funcs": []
    }

    def __init__(self):
        # Crea el unico objeto global
        self.global_ctx = Global()

        # Crea el directorio de funciones/procedimientos
        self.funcs_table_obj = FuncTable(self.global_ctx.id)

    def enterProgram(self, ctx: PopurriParser.ProgramContext):
        '''
        [Program] marca el inicio de las reglas de la gramatica. Aqui inicia la fase de compilacion.
        '''
        self.funcs_table_obj.insertProc(self.global_ctx)
        print('program')
        pass

    def exitProgram(self, ctx: PopurriParser.ProgramContext):
        '''
        [Program] marca el final de las reglas de la gramatica. Aqui termina la fase de compilacion.
        '''
        print('start of func_table')
        print(self.funcs_table_obj.func_table)

        for key, obj in self.funcs_table_obj.func_table.items():
            print(key)
            pprint(obj)

    def enterModule(self, ctx: PopurriParser.ModuleContext):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module')
        pass

    def exitModule(self, ctx: PopurriParser.ModuleContext):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        print('module exit')
        pass

    def enterDeclarations(self, ctx: PopurriParser.DeclarationsContext):
        pass

    def exitDeclarations(self, ctx: PopurriParser.DeclarationsContext):
        pass

    def enterDeclaration(self, ctx: PopurriParser.DeclarationContext):
        # Checks if var is already created in mem_slots
        if any(var.id is str(ctx.ID()) for var in self.funcs_table_obj.func_table[self.funcs_table_obj.dir_key_ptr].attributes):
            raise 'ERROR VAR ALREADY CREATED'

        var = ""
        # var has data_type : INT, FLOAT, STRING, BOOL
        # TODO: Arrays are not yet implemented
        if ctx.TYPE() is not None:
            var = Variable(
                id=ctx.ID(0),
                type=ctx.TYPE()
            )
        # var is type object
        else:
            var = Variable(
                id=ctx.ID(0),
                type=ctx.ID(1)
            )

        self.funcs_table_obj.func_table[self.funcs_table_obj.dir_key_ptr].insertAttribute(
            var)

        pprint(var)
        print('declaration')

    def exitDeclaration(self, ctx: PopurriParser.DeclarationContext):
        pass

    def enterFunction(self, ctx: PopurriParser.FunctionContext):
        if any(id is str(ctx.ID(0)) for id, _ in self.funcs_table_obj.func_table.items()):
            raise f'ERROR RE-DEFINITION OF {str(ctx.ID(0))}'

        func = Function(
            id=ctx.ID(0)
        )
        # Function has params
        if ctx.funcParams() is not None:
            no_params = len(ctx.funcParams().ID())
            params = []
            for i in range(no_params):
                params.append(Variable(
                    id=ctx.funcParams().ID(i),
                    type=ctx.funcParams().TYPE(i),
                    context=func.id
                ))
            func.params = params

        # Function has primitive return type
        if ctx.TYPE() is not None:
            func.return_type = str(ctx.TYPE())
        # Function returns object
        elif len(ctx.ID()) > 1:
            func.return_type = str(ctx.ID(1))

        self.funcs_table_obj.insertProc(func)
        self.funcs_table_obj.changeKeyPtr(func.id)
        pprint(func)
        pass

    def exitFunction(self, ctx: PopurriParser.FunctionContext):
        self.funcs_table_obj.changeKeyPtr(self.global_ctx.id)

    def enterClassDeclaration(self, ctx: PopurriParser.ClassDeclarationContext):
        if any(id is str(ctx.ID()) for id, _ in self.funcs_table_obj.func_table.items()):
            raise f'ERROR RE-DEFINITION OF {str(ctx.ID())}'

        klass = Object(id=str(ctx.ID()))
        if ctx.parent() is not None:
            # TODO: implement inheritance of attrs & functions
            klass.parent_id = str(ctx.parent().ID())

        self.funcs_table_obj.insertProc(klass)
        self.funcs_table_obj.changeKeyPtr(klass.id)
        pprint(klass)
        print('class')
        pass

    def exitClassDeclaration(self, ctx: PopurriParser.ClassDeclarationContext):
        self.funcs_table_obj.changeKeyPtr(self.global_ctx.id)
        pass

    def enterParent(self, ctx: PopurriParser.ParentContext):
        pass

    def exitParent(self, ctx: PopurriParser.ParentContext):
        pass

    def enterAccessType(self, ctx: PopurriParser.AccessTypeContext):
        pass

    def exitAccessType(self, ctx: PopurriParser.AccessTypeContext):
        pass

    def enterAttributes(self, ctx: PopurriParser.AttributesContext):
        pass

    def exitAttributes(self, ctx: PopurriParser.AttributesContext):
        pass

    def enterAttribute(self, ctx: PopurriParser.AttributeContext):
        if any(var.id is str(ctx.ID()) for var in self.funcs_table_obj.func_table[self.funcs_table_obj.dir_key_ptr].attributes):
            raise 'ERROR VAR ALREADY CREATED'

        if ctx.TYPE() is not None:
            var = Variable(
                id=ctx.ID(),
                type=ctx.TYPE(),
            )
        # var is type object
        else:
            var = Variable(
                id=ctx.ID(0),
                type=ctx.ID(1)
            )

        self.funcs_table_obj.func_table[self.funcs_table_obj.dir_key_ptr].insertAttribute(
            var)

        print('attribute')
        pass

    def exitAttribute(self, ctx: PopurriParser.AttributeContext):
        pass

    def enterStatement(self, ctx: PopurriParser.StatementContext):
        pass

    def exitStatement(self, ctx: PopurriParser.StatementContext):
        pass

    def enterWhileLoop(self, ctx: PopurriParser.WhileLoopContext):
        pass

    def exitWhileLoop(self, ctx: PopurriParser.WhileLoopContext):
        pass

    def enterForLoop(self, ctx: PopurriParser.ForLoopContext):
        pass

    def exitForLoop(self, ctx: PopurriParser.ForLoopContext):
        pass

    def enterBranch(self, ctx: PopurriParser.BranchContext):
        pass

    def exitBranch(self, ctx: PopurriParser.BranchContext):
        pass

    def enterIfStmt(self, ctx: PopurriParser.IfStmtContext):
        pass

    def exitIfStmt(self, ctx: PopurriParser.IfStmtContext):
        pass

    def enterElseIf(self, ctx: PopurriParser.ElseIfContext):
        pass

    def exitElseIf(self, ctx: PopurriParser.ElseIfContext):
        pass

    def enterElseStmt(self, ctx: PopurriParser.ElseStmtContext):
        pass

    def exitElseStmt(self, ctx: PopurriParser.ElseStmtContext):
        pass

    def enterReturnStmt(self, ctx: PopurriParser.ReturnStmtContext):
        pass

    def exitReturnStmt(self, ctx: PopurriParser.ReturnStmtContext):
        pass

    def enterCond(self, ctx: PopurriParser.CondContext):
        pass

    def exitCond(self, ctx: PopurriParser.CondContext):
        pass

    def enterCmp(self, ctx: PopurriParser.CmpContext):
        pass

    def exitCmp(self, ctx: PopurriParser.CmpContext):
        pass

    def enterExp(self, ctx: PopurriParser.ExpContext):
        pass

    def exitExp(self, ctx: PopurriParser.ExpContext):
        pass

    def enterAdd(self, ctx: PopurriParser.AddContext):
        pass

    def exitAdd(self, ctx: PopurriParser.AddContext):
        pass

    def enterMultModDiv(self, ctx: PopurriParser.MultModDivContext):
        pass

    def exitMultModDiv(self, ctx: PopurriParser.MultModDivContext):
        pass

    def enterVal(self, ctx: PopurriParser.ValContext):
        pass

    def exitVal(self, ctx: PopurriParser.ValContext):
        pass

    def enterIndexation(self, ctx: PopurriParser.IndexationContext):
        pass

    def exitIndexation(self, ctx: PopurriParser.IndexationContext):
        pass

    def enterAssignment(self, ctx: PopurriParser.AssignmentContext):
        pass

    def exitAssignment(self, ctx: PopurriParser.AssignmentContext):
        pass

    def enterFuncCall(self, ctx: PopurriParser.FuncCallContext):
        pass

    def exitFuncCall(self, ctx: PopurriParser.FuncCallContext):
        pass

    def enterBoolOp(self, ctx: PopurriParser.BoolOpContext):
        pass

    def exitBoolOp(self, ctx: PopurriParser.BoolOpContext):
        pass

    def enterCmpOp(self, ctx: PopurriParser.CmpOpContext):
        pass

    def exitCmpOp(self, ctx: PopurriParser.CmpOpContext):
        pass

    def enterAddOp(self, ctx: PopurriParser.AddOpContext):
        pass

    def exitAddOp(self, ctx: PopurriParser.AddOpContext):
        pass

    def enterMultDivOp(self, ctx: PopurriParser.MultDivOpContext):
        pass

    def exitMultDivOp(self, ctx: PopurriParser.MultDivOpContext):
        pass

    def enterAssignOp(self, ctx: PopurriParser.AssignOpContext):
        pass

    def exitAssignOp(self, ctx: PopurriParser.AssignOpContext):
        pass

    def enterConstant(self, ctx: PopurriParser.ConstantContext):
        pass

    def exitConstant(self, ctx: PopurriParser.ConstantContext):
        pass

    def enterConst_arr(self, ctx: PopurriParser.Const_arrContext):
        pass

    def exitConst_arr(self, ctx: PopurriParser.Const_arrContext):
        pass

    def enterIterable(self, ctx: PopurriParser.IterableContext):
        pass

    def exitIterable(self, ctx: PopurriParser.IterableContext):
        pass

    def enterPrintStmt(self, ctx: PopurriParser.PrintStmtContext):
        pass

    def exitPrintStmt(self, ctx: PopurriParser.PrintStmtContext):
        pass

    def enterInputStmt(self, ctx: PopurriParser.InputStmtContext):
        pass

    def exitInputStmt(self, ctx: PopurriParser.InputStmtContext):
        pass

    def enterCondParam(self, ctx: PopurriParser.CondParamContext):
        pass

    def exitCondParam(self, ctx: PopurriParser.CondParamContext):
        pass

    def enterFuncParams(self, ctx: PopurriParser.FuncParamsContext):
        pass

    def exitFuncParams(self, ctx: PopurriParser.FuncParamsContext):
        pass
