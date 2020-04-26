from antlr4 import *
from parser.PopurriParser import PopurriParser
from popurri_tokens import *

def getSymbolFromStr(symbol_str=None):
        symbolTable = ['', 'int', 'float', 'string', 'bool']
        if symbol_str is None:
            return None
        return symbolTable.index(str(symbol_str))

def getGlobalPtrFromId(id=None):
    for iterator in range(len(self.global_dir)):
        if str(id) == str(self.global_dir[iterator]['id']):
            return iterator
    return None

def getGlobalPtrFromClassName(class_name=None):
    for iterator in range(len(self.global_dir)):
        if self.global_dir[iterator]['type'] == 'template_class':
            if self.global_dir[iterator]['class_name'] == str(class_name):
                return iterator
    return None

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


    def enterProgram(self, ctx:PopurriParser.ProgramContext):
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

    def exitProgram(self, ctx:PopurriParser.ProgramContext):
        '''
        [Program] marca el final de las reglas de la gramatia. Aqui termina la fase de compilacion.
        '''
        # Libera la memoria del compilador [Elimina las entradas de la tabla de direccines globales]
        self.global_dir.clear()
        self.mem_slots = []
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
        for slot in self.mem_slots:
            if slot[0] is ctx.ID():
                raise 'ERROR VAR ALREADY CREATED'

        # Creates var

        # if var has data_type : INT, FLOAT, STRING, BOOL, [Arrays are not yet implemented]
        if ctx.TYPE() is not None:
            symbol_token = getSymbolFromStr(ctx.TYPE())
            self.mem_slots[self.mem_ptr_dict[symbol_token]] = (
                str(ctx.ID()), 0)
            self.global_dir[self.global_dir_ptr]['declarations'].append(
                self.mem_ptr_dict[symbol_token])
            # increments the ptr for ctx.TYPE()in mem_ptr_dict
            self.mem_ptr_dict[symbol_token] += 1

        # if var is an object of ID
        else:
            object_class_template_ptr = getGlobalPtrFromClassName(ctx.ID()[1])

            if object_class_template_ptr is None:
                print('ERROR')
            else:
                object_class = self.global_dir[object_class_template_ptr]
                object_class['id'] = ctx.ID()[0]
                self.global_dir.append(object_class)
                self.global_dir_ptr = len(self.global_dir) - 1
                self.global_dir[object_class['node_parent']
                                ]['classes'].append(self.global_dir_ptr)

        # Check if everything is correct[Debugging]
        print(self.global_dir, self.mem_ptr_dict)
        print('declaration')

    def exitDeclaration(self, ctx:PopurriParser.DeclarationContext):
        self.global_dir_ptr = 0
        pass

    def enterFunction(self, ctx:PopurriParser.FunctionContext):
        pass

    def exitFunction(self, ctx:PopurriParser.FunctionContext):
        pass

    def enterClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        print('class')

        created_class = {
            'type': 'template_class',
            'class_name': None,
            'id': None,
            'class_parent': None,
            'node_parent': 0,
            'attributes': [],
            'functions': [],
        }
        created_class['class_name'] = str(ctx.ID())

        self.global_dir.append(created_class)

        print(self.global_dir, self.mem_ptr_dict, self.global_dir_ptr)
        pass

    def exitClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        pass

    def enterParent(self, ctx:PopurriParser.ParentContext):
        if ctx.ID() is not None:
            self.global_dir[self.global_dir_ptr]['class_parent'] = getGlobalPtrFromId(ctx.ID())
            if self.global_dir[self.global_dir_ptr]['class_parent'] is None:
                print('Error')

        self.global_dir[self.global_dir_ptr]['class_parent'] = str(ctx.ID())
        print(self.global_dir, self.mem_ptr_dict, self.global_dir_ptr)

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
        return
        # Checks if var is already created in mem_slots
        for slot in self.mem_slots:
            if slot[0] is ctx.ID():
                raise 'ERROR VAR ALREADY CREATED'

        # Creates var
        symbol_token = getSymbolFromStr(ctx.TYPE())
        self.mem_slots[self.mem_ptr_dict[symbol_token]] = (str(ctx.ID()), 0)
        self.global_dir[self.global_dir_ptr]['attributes'].append(
            self.mem_ptr_dict[symbol_token])

        # increments the ptr for ctx.TYPE()in mem_ptr_dict
        self.mem_ptr_dict[symbol_token] += 1

        # Check if everything is correct[Debugging]
        print(self.global_dir, self.mem_ptr_dict)
        print(self.mem_slots[:10])
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
