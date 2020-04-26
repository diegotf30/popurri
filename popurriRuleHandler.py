from parser.PopurriListener import PopurriListener
from popurri_tokens import *


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
            if str(id) == str(self.global_dir[iterator]['id']):
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

        self.global_dir.append(created_class)
        self.global_dir_ptr = len(self.global_dir) - 1
        self.global_dir[created_class['node_parent']
                        ]['classes'].append(self.global_dir_ptr)
        print(self.global_dir, self.mem_ptr_dict, self.global_dir_ptr)

    def exitClassDeclaration(self, ctx):
        self.global_dir_ptr = 0
        pass

    def enterParent(self, ctx):
        if ctx.ID() is not None:
            self.global_dir[self.global_dir_ptr]['class_parent'] = self.getGlobalPtrFromId(
                ctx.ID())
            if self.global_dir[self.global_dir_ptr]['class_parent'] is None:
                print('Error')

        self.global_dir[self.global_dir_ptr]['class_parent'] = str(ctx.ID())
        print(self.global_dir, self.mem_ptr_dict, self.global_dir_ptr)
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
        # Checks if var is already created in mem_slots
        for slot in self.mem_slots:
            if slot[0] is ctx.ID():
                raise 'ERROR VAR ALREADY CREATED'

        # Creates var
        symbol_token = self.getSymbolFromStr(ctx.TYPE())
        self.mem_slots[self.mem_ptr_dict[symbol_token]] = (ctx.ID(), 0)
        self.global_dir[self.global_dir_ptr]['attributes'].append(
            self.mem_ptr_dict[symbol_token])

        # increments the ptr for ctx.TYPE()in mem_ptr_dict
        self.mem_ptr_dict[symbol_token] += 1

        # Check if everything is correct[Debugging]
        print(self.global_dir, self.mem_ptr_dict)
        print('attribute')

    def exitAttribute(self, ctx):
        pass

    def enterType(self, ctx):
        print()
        pass

    def exitType(self, ctx):
        print('type')
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
