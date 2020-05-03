from antlr4 import *
from popurri_tokens import *
import json


def pprint(*args):
    for arg in args:
        print(json.dumps(arg, indent=2, default=vars))


class Cuadruple():

    def __init__(self, op, l, r, res):
        self.op = op
        # Arguments
        self.l = l
        self.r = r
        # Where result of op(l, r) is stored
        self.res = res

# antes FuncTable


class GlobalContext():
    '''
    Esta es una tabla de procedimientos
    '''

    def __init__(self):
        self.variables = {}
        self.functions = {}

    def addVariable(self, var, context="global"):
        if context in self.variables:
            self.variables[context][var.id] = var
        else:
            self.variables[context] = {
                var.id: var
            }

    def addFunction(self, func, context="global"):
        if context in self.functions:
            self.functions[context][func.id] = func
        else:
            self.functions[context] = {
                func.id: func
            }

    def varExistsInContext(self, var_id, ctx_id):
        if ctx_id not in self.variables:
            return False

        return self.variables[ctx_id].get(str(var_id), False)

    def functionExistsInContext(self, func_id, ctx_id):
        if ctx_id not in self.functions:
            return False

        return self.functions[ctx_id].get(str(func_id), False)

    def classExists(self, id):
        id = str(id)
        if 'class' not in id:
            id = 'class ' + id

        return id in self.variables or id in self.functions


class Variable():
    '''
    Esto nos permite simular la creacion de variables. Inicializandolas con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la actual variable. Ej. var edad : int. Donde edad es el ID.
    [type] es el tipo de dato con el que la variable estara relacionada. Ej. var edad : int. Donde int es el tipo de dato.
    [value] es el valor inicial que tendra la variable. Ej. var edad = 25. Donde 25 es el valor inicial.
    '''

    def __init__(self, id, access_type="public", type=None, value=None):
        self.access_type = str(access_type)
        self.id = str(id)
        self.type = str(type)
        self.value = value


class Object():
    '''
    Esto nos permite simular la creacion de clases. Inicializandolos con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la clase actual. Ej. class Humano {}. Donde Humano es el identificador.
    [parent_id] es el identificador del cual la clase actual heredara todas las propiedades. Ej. class Humano -> Persona. Donde Humano es el identificador
    padre.
    '''

    def __init__(self, id, parent_id=None):
        self.id = str(id)
        self.parent_id = str(parent_id)


class Function():
    '''
    Esto nos permite simular la creacion de funciones. Inicializandolas con atributos predeterminados.
    [id] es el identificador con el que se podra localizar la funcion actual. Ej. func habla() {}. Donde habla es el identificador.
    [return_type] es el tipo de dato que regresara la funcion al terminar su ejecucion. Void es el tipo predeterminado.
    '''

    def __init__(self, id, return_type="void", access_type="public"):
        self.id = str(id)
        self.return_type = str(return_type)
        self.access_type = str(access_type)


class PopurriListener(ParseTreeListener):
    '''
    -Esta clase nos permite simular la creacion de tabla de variables
    -[Tal vez podamos usar esta clase para simular la semantica basica de expresiones]
    -Cada funcion 'enter' representa el estado cuando se inicia una  regla
    -Cada funcion 'exit' representa el estado cuando se acaba una regla
    '''

    def __init__(self):
        self.global_ctx = GlobalContext()

    def enterProgram(self, ctx):
        '''
        [Program] marca el inicio de las reglas de la gramatica. Aqui inicia la fase de compilacion.
        '''
        pass

    def exitProgram(self, ctx):
        '''
        [Program] marca el final de las reglas de la gramatica. Aqui termina la fase de compilacion.
        '''
        print("--VARIABLES--")
        pprint(self.global_ctx.variables)
        print("--FUNCTIONS--")
        pprint(self.global_ctx.functions)
        pass

    def enterModule(self, ctx):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        pass

    def exitModule(self, ctx):
        '''
        [Module] no afecta ningun aspecto del compilador o lenguaje, por lo que se ignora
        '''
        pass

    def enterDeclarations(self, ctx):
        pass

    def exitDeclarations(self, ctx):
        pass

    def enterDeclaration(self, ctx):
        # Checks if global is already declared
        if self.global_ctx.varExistsInContext(ctx.ID(0), "global"):
            raise f'ERROR VAR {str(ctx.ID(0))} ALREADY DEFINED'

        var = None
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

        self.global_ctx.addVariable(var)

    def exitDeclaration(self, ctx):
        pass

    def createFunction(self, ctx):
        func = Function(
            id=ctx.ID(0)
        )
        # Function has params
        if ctx.funcParams() is not None:
            no_params = len(ctx.funcParams().ID())
            for i in range(no_params):
                param = Variable(
                    id=ctx.funcParams().ID(i),
                    type=ctx.funcParams().TYPE(i),
                )
                self.global_ctx.addVariable(param, func.id)

        # Function has primitive return type
        if ctx.TYPE() is not None:
            func.return_type = str(ctx.TYPE())
        # Function returns object
        elif len(ctx.ID()) > 1:
            func.return_type = str(ctx.ID(1))

        return func

    def enterFunction(self, ctx):
        if self.global_ctx.functionExistsInContext(ctx.ID(0), "global"):
            raise f'ERROR RE-DEFINITION OF {str(ctx.ID(0))}'

        self.global_ctx.addFunction(self.createFunction(ctx))
        pass

    def exitFunction(self, ctx):
        pass

    def getAccessType(self, ctx):
        ty = ctx.ACCESS_TYPE()
        return 'public' if ty is None else ty

    def enterClassDeclaration(self, ctx):
        class_name = str(ctx.ID())
        if self.global_ctx.classExists(class_name):
            raise f'ERROR RE-DEFINITION OF {class_name}'

        klass = Object(
            id=class_name
        )
        if ctx.parent() is not None:
            klass.parent_id = 'class ' + str(ctx.parent().ID())
            if not self.global_ctx.classExists(klass.parent_id):
                raise 'ERROR PARENT CLASS MUST BE DEFINED BEFORE CHILD CLASS'

            # Inherit attributes
            for attribute in self.global_ctx.variables[klass.parent_id].values():
                if attribute.access_type != 'private':
                    self.global_ctx.addVariable(attribute, 'class ' + klass.id)

            # Inherit functions
            for func in self.global_ctx.functions[klass.parent_id].values():
                if func.access_type != 'private':
                    self.global_ctx.addFunction(func, 'class ' + klass.id)

        # Parse class attributes
        for declarations in ctx.attributes():
            access_type = self.getAccessType(declarations)

            for attr in declarations.attribute():
                # if attribute inherited, do nothing
                if self.global_ctx.varExistsInContext(attr.ID(), klass.parent_id):
                    continue
                # Checks if attribute is already declared within class
                elif self.global_ctx.varExistsInContext(attr.ID(), 'class ' + klass.id):
                    raise f'ERROR ATTRIBUTE {str(attr.ID())} ALREADY DEFINED'

                var = Variable(
                    id=attr.ID(),
                    type=attr.TYPE(),
                    access_type=access_type
                )
                self.global_ctx.addVariable(var, 'class ' + klass.id)

        # Parse class methods
        for method in ctx.method():
            # if attribute inherited, do nothing
            if self.global_ctx.functionExistsInContext(attr.ID(), klass.parent_id):
                continue
            # Checks if attribute is already declared within class
            elif self.global_ctx.functionExistsInContext(method.ID(0), 'class ' + klass.id):
                raise f'ERROR METHOD {str(attr.ID())} ALREADY DEFINED'

            access_type = self.getAccessType(method)

            method = self.createFunction(method)
            method.access_type = str(access_type)

            self.global_ctx.addFunction(method, 'class ' + klass.id)

        pass

    def exitClassDeclaration(self, ctx):
        pass

    def enterParent(self, ctx):
        pass

    def exitParent(self, ctx):
        pass

    def enterAttributes(self, ctx):
        pass

    def exitAttributes(self, ctx):
        pass

    def enterAttribute(self, ctx):
        pass

    def exitAttribute(self, ctx):
        pass

    def enterMethod(self, ctx):
        pass

    def exitMethod(self, ctx):
        pass

    def enterStatement(self, ctx):
        pass

    def exitStatement(self, ctx):
        pass

    def enterWhileLoop(self, ctx):
        pass

    def exitWhileLoop(self, ctx):
        pass

    def enterForLoop(self, ctx):
        pass

    def exitForLoop(self, ctx):
        pass

    def enterBranch(self, ctx):
        pass

    def exitBranch(self, ctx):
        pass

    def enterIfStmt(self, ctx):
        pass

    def exitIfStmt(self, ctx):
        pass

    def enterElseIf(self, ctx):
        pass

    def exitElseIf(self, ctx):
        pass

    def enterElseStmt(self, ctx):
        pass

    def exitElseStmt(self, ctx):
        pass

    def enterReturnStmt(self, ctx):
        pass

    def exitReturnStmt(self, ctx):
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

    def enterIndexation(self, ctx):
        pass

    def exitIndexation(self, ctx):
        pass

    def enterAssignment(self, ctx):
        pass

    def exitAssignment(self, ctx):
        pass

    def enterFuncCall(self, ctx):
        pass

    def exitFuncCall(self, ctx):
        pass

    def enterBoolOp(self, ctx):
        pass

    def exitBoolOp(self, ctx):
        pass

    def enterCmpOp(self, ctx):
        pass

    def exitCmpOp(self, ctx):
        pass

    def enterAddOp(self, ctx):
        pass

    def exitAddOp(self, ctx):
        pass

    def enterMultDivOp(self, ctx):
        pass

    def exitMultDivOp(self, ctx):
        pass

    def enterAssignOp(self, ctx):
        pass

    def exitAssignOp(self, ctx):
        pass

    def enterConstant(self, ctx):
        pass

    def exitConstant(self, ctx):
        pass

    def enterConst_arr(self, ctx):
        pass

    def exitConst_arr(self, ctx):
        pass

    def enterIterable(self, ctx):
        pass

    def exitIterable(self, ctx):
        pass

    def enterPrintStmt(self, ctx):
        pass

    def exitPrintStmt(self, ctx):
        pass

    def enterInputStmt(self, ctx):
        pass

    def exitInputStmt(self, ctx):
        pass

    def enterCondParam(self, ctx):
        pass

    def exitCondParam(self, ctx):
        pass

    def enterFuncParams(self, ctx):
        pass

    def exitFuncParams(self, ctx):
        pass
