from antlr4 import *
from antlr_parser.PopurriParser import PopurriParser
from popurri_tokens import *
from error_tokens import *
from semantic_cube import bailaMijaConElSeñor
from memory import MemoryHandler
from copy import deepcopy
import jsbeautifier as js
import json


def pprint(*args):
    opts = js.default_options()
    opts.indent_size = 2
    for arg in args:
        print(js.beautify(json.dumps(arg, default=vars), opts))


def error(ctx, msg):
    return Exception(f'ERROR ON LINE {ctx.start.line}: {msg}')


class QuadWrapper():
    '''
    Handles all quadruple generation related stuff
    '''

    def __init__(self):
        self.quads = []
        self.quads_ptr = 0
        self.type_stack = []
        self.operator_stack = []
        self.address_stack = []
        self.jump_stack = []
        self.break_stack = []

    def insertQuad(self, quad, at=None):
        self.quads_ptr += 1
        if at is not None:
            self.quads.insert(at, quad.__str__())
        else:
            self.quads.append(quad.__str__())

    def fillQuadWith(self, filler, at):
        new_quad = list(self.quads[at])
        new_quad[3] = filler
        self.quads[at] = tuple(new_quad)

    def topOperator(self):
        if len(self.operator_stack) == 0 or self.operator_stack[-1] == OPENPAREN:
            return None

        return self.operator_stack[-1]

    def topJump(self):
        return self.jump_stack[-1] if len(self.jump_stack) > 0 else None

    def popOperator(self):
        if len(self.operator_stack) == 0 or self.topOperator() == OPENPAREN:
            return None

        return self.operator_stack.pop()

    def popAddress(self):
        return self.address_stack.pop() if len(self.address_stack) > 0 else None

    def popJump(self):
        return self.jump_stack.pop() if len(self.jump_stack) > 0 else None

    def popType(self):
        return self.type_stack.pop() if len(self.type_stack) > 0 else None

    # Flushes jumps until either stack is empty or it encounters a false-bottom
    def flushJumps(self):
        jumps = []
        while True:
            j = self.popJump()
            if j is None or j is OPENPAREN:
                break
            jumps.insert(0, j)
        return jumps

    def insertType(self, type):
        self.type_stack.append(str(type))

    def insertAddress(self, address):
        self.address_stack.append(address)

    def insertOperator(self, operator):
        self.operator_stack.append(tokenize(operator))

    def insertJump(self, jump=None):
        self.jump_stack.append(self.quads_ptr if jump is None else jump)

    def validateTypes(self, ctx):
        op = self.topOperator()
        r_type = self.popType()
        l_type = self.popType()
        res_type = bailaMijaConElSeñor(op, l_type, r_type)
        if res_type is None:
            raise error(ctx, TYPE_MISMATCH.format(op, l_type, r_type))
        # Push resulting type into stack
        self.insertType(res_type)

        return res_type

    def generateQuad(self, ctx, memHandler):
        tmp_type = self.validateTypes(ctx)

        tmp = memHandler.reserve(
            context=TEMPORAL,
            dtype=tokenize(tmp_type)
        )

        self.insertQuad(Quadruple(
            op=self.popOperator(),
            r=self.popAddress(),
            l=self.popAddress(),
            res=tmp
        ))
        self.insertAddress(tmp)


class Quadruple():

    def __init__(self, op, l=None, r=None, res=None):
        self.op = op
        # Arguments (In some cases one of both of them would be -1 indicating there is no value)
        self.l = l
        self.r = r
        # Where result of op(l, r) is stored
        # This is an address rather than a value
        self.res = res

    def __str__(self):
        return (self.op, self.l, self.r, self.res)


class ContextWrapper():
    '''
    Esta es una tabla de procedimientos y stack de contextos
    Antes GlobalContext
    '''

    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.context_stack = ['global']
        self.loop_stack = []

    def pushLoop(self):
        return self.loop_stack.append(True)

    def popLoop(self):
        return self.loop_stack.pop()

    def insideLoop(self):
        return len(self.loop_stack) > 0

    def insideClass(self):
        if len(self.context_stack) < 2:
            return False

        return 'class' in self.top() or 'class' in self.context_stack[-2]

    def top(self):
        return self.context_stack[-1]

    def pop(self):
        return self.context_stack.pop()

    def push(self, ctx):
        return self.context_stack.append(str(ctx))

    def getVariableByAddress(self, address):
        for ctx in self.variables.values(): # Iterate over contexts
            for var in ctx.values():
                if type(var) == dict: # Inside function varTable
                    for var in var.values():
                        if type(var) == dict: # Var is object, iterate over attributes
                            for attr in var.values():
                                if address == attr.address:
                                    return attr
                        elif address == var.address:
                            return var
                elif address == var.address:
                    return var
        return None

    def getVariable(self, var_id, context="global"):
        if context in self.variables:
            return self.variables[context].get(str(var_id), None)
        else:
            return None

    def getFunction(self, func_id, context="global"):
        func_id = str(func_id)
        if 'func ' not in func_id:
            func_id = 'func ' + func_id

        if context in self.functions:
            return self.functions[context].get(str(func_id), None)
        else:
            return None

    def getCurrentFunction(self):
        func_id = self.pop()
        func_ctx_id = self.top()
        self.push(func_id)  # Re-push current context
        return self.getFunction(func_id, context=func_ctx_id)

    def getClassContext(self):
        if len(self.context_stack) < 2:
            return None

        if 'class' in self.top():
            return self.top()
        elif 'class' in self.context_stack[-2]:
            return self.context_stack[-2]

        return None

    def getAttributes(self, class_id):
        if 'class' not in class_id:
            class_id = 'class ' + class_id

        if class_id not in self.variables:
            return None

        return { k:deepcopy(v) for k,v in self.variables[class_id].items() if type(v) != dict}

    def addVariable(self, var, context="global", insideClass=False):
        variables = self.variables[self.getClassContext()] if insideClass else self.variables

        if context in variables:
            variables[context][var.id] = var
        else:
            variables[context] = {
                var.id: var
            }

    def addFunction(self, func, context="global"):
        func_id = 'func ' + func.id
        if context in self.functions:
            self.functions[context][func_id] = func
        else:
            self.functions[context] = {
                func_id: func
            }

    def getVariableIfExists(self, var_id):
        if self.insideClass():
            class_name = self.getClassContext()
            if self.top() not in self.variables[class_name]:
                return None

            return self.variables[class_name][self.top()].get(str(var_id), None), self.top()

        for ctx in self.context_stack[::-1]:
            if ctx not in self.variables:
                continue

            var = self.variables[ctx].get(str(var_id), None)
            if var is not None:
                return var, ctx

        return None, None

    def getFunctionIfExists(self, func_id):
        func_id = str(func_id)
        if 'func ' not in func_id:
            func_id = 'func ' + func_id

        for ctx in self.context_stack[::-1]:
            if ctx not in self.functions:
                continue

            var = self.functions[ctx].get(str(func_id), None)
            if var is not None:
                return var

        return None

    def varExistsInContext(self, var_id, ctx='global'):
        if ctx not in self.variables:
            return False

        return self.variables[ctx].get(str(var_id), False)

    def functionExistsInContext(self, func_id, ctx='global'):
        func_id = str(func_id)
        if 'func ' not in func_id:
            func_id = 'func ' + func_id

        if ctx not in self.functions:
            return False

        return self.functions[ctx].get(str(func_id), False)

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

    def __init__(self, id, access_type="public", type=None, address=None, isArray=False):
        self.access_type = str(access_type)
        self.id = str(id)
        self.type = str(type)
        self.address = address
        self.isArray = isArray


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
        self.quads_range = (-1, -1)
        self.paramTypes = []

    def updateQuadsRange(self, start=None, end=None):
        quads_range = list(self.quads_range)
        if start is not None:
            quads_range[0] = start
        if end is not None:
            quads_range[1] = end
        self.quads_range = tuple(quads_range)

    def addParamType(self, ty):
        self.paramTypes.append(ty)


class PopurriListener(ParseTreeListener):
    '''
    -Esta clase nos permite simular la creacion de tabla de variables
    -[Tal vez podamos usar esta clase para simular la semantica basica de expresiones]
    -Cada funcion 'enter' representa el estado cuando se inicia una  regla
    -Cada funcion 'exit' representa el estado cuando se acaba una regla
    '''

    def __init__(self, mem_size):
        self.ctxWrapper = ContextWrapper()
        self.quadWrapper = QuadWrapper()
        self.memHandler = MemoryHandler(mem_size)
        self.if_cond = False
        self.statement = False
        self.param_count = -1
        self.func_count = -1
        self.func_returned_val = False
        # a[ array_indexation_exp ]
        self.array_indexation_exp = False

    def enterProgram(self, ctx):
        '''
        [Program] marca el inicio de las reglas de la gramatica. Aqui inicia la fase de compilacion.
        '''
        goto_quad = Quadruple(GOTO)
        self.quadWrapper.insertQuad(goto_quad)
        self.quadWrapper.insertJump()
        self.func_count = len(ctx.function())
        pass

    def exitProgram(self, ctx):
        '''
        [Program] marca el final de las reglas de la gramatica. Aqui termina la fase de compilacion.
        '''
        print("--VARIABLES--")
        pprint(self.ctxWrapper.variables)
        print("--FUNCTIONS--")
        pprint(self.ctxWrapper.functions)

        print('quads_stack = [')
        for i, x in enumerate(self.quadWrapper.quads, start=1):
            tmp = list(x)
            tmp[0] = stringifyToken(x[0])
            print('\t', i, tuple(tmp))
        print(']')

        print('address_stack = ', end='')
        pprint(self.quadWrapper.address_stack)
        print('operator_stack = ', end='')
        pprint(self.quadWrapper.operator_stack)
        print('type_stack = ', end='')
        pprint(self.quadWrapper.type_stack)
        print('jump_stack = ', end='')
        pprint(self.quadWrapper.jump_stack)
        print('quad_ptr = ', end='')
        pprint(self.quadWrapper.quads_ptr)

        for ctx in [GLOBAL, LOCAL, CONSTANT, TEMPORAL]:
            context = self.memHandler.contexts[ctx].sections
            print(stringifyToken(ctx), '= {')
            for section in context:
                print('    ', stringifyToken(section), context[section])
            print('}')

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
        if self.ctxWrapper.top() == 'global':
            # Fill GOTO to declarations start (so classes dont get executed)
            self.quadWrapper.fillQuadWith(
                self.quadWrapper.quads_ptr + 1,
                at=self.quadWrapper.popJump() - 1
            )

    def exitDeclarations(self, ctx):
        if self.ctxWrapper.top() == 'global':
            goto_quad = Quadruple(GOTO)
            self.quadWrapper.insertQuad(goto_quad)
            self.quadWrapper.insertJump()

    def enterDeclaration(self, ctx):
        # Checks if global is already declared
        if self.ctxWrapper.varExistsInContext(ctx.ID(0), ctx=self.ctxWrapper.top()):
            raise error(ctx, VAR_REDEFINITION.format(str(ctx.ID(0))))

        var = None
        # var has data_type : INT, FLOAT, STRING, BOOL
        # TODO: Arrays are not yet implemented
        if ctx.TYPE() is not None:

            dtype = tokenize(ctx.TYPE())

            reserved_address = self.memHandler.reserve(
                context=tokenizeContext(self.ctxWrapper.top()),
                dtype=dtype
            )

            var = Variable(
                id=ctx.ID(0),
                type=ctx.TYPE(),
                address=reserved_address
            )

            # var is an array
            if ctx.CONST_I() is not None:
                var.isArray = True
                array_size = self.getConstant(ctx, True) - 1

                for _ in range(array_size):
                    reserved_address = self.memHandler.reserve(
                        context=tokenizeContext(self.ctxWrapper.top()),
                        dtype=dtype
                    )

        # var is type object
        elif len(ctx.ID()) == 2:
            if ctx.assignment() is not None:
                raise error(ctx, CLASS_ASSIGNMENT)

            class_name = str(ctx.ID(1))
            if not self.ctxWrapper.classExists(class_name):
                raise error(ctx, UNDEF_CLASS.format(class_name))

            # Re-allocate attributes in current context
            attrs = self.ctxWrapper.getAttributes(class_name)
            for attr in attrs.values():
                attr.address = self.memHandler.reserve(
                    context=tokenizeContext(self.ctxWrapper.top()),
                    dtype=tokenize(attr.type)
                )

            context_vars = self.ctxWrapper.variables
            if self.ctxWrapper.insideClass():
                context_vars = context_vars[self.ctxWrapper.getClassContext()]

            # Add self var (so we know what type is this object)
            var_id = str(ctx.ID(0))
            self_var = Variable(
                id='self',
                type=class_name
            )
            attrs[self_var.id] = self_var

            curr_ctx = self.ctxWrapper.top()
            if curr_ctx not in context_vars:
                context_vars[curr_ctx] = { var_id: attrs }
            else:
                context_vars[curr_ctx][var_id] = attrs

            return

        # Var type will be declared implicitly via assignment
        elif ctx.assignment() is not None:
            var = Variable(id=ctx.ID(0))
        else:
            raise error(ctx, MUST_DECLARE_VAR_TYPE.format(str(ctx.ID(0))))

        if ctx.assignment() is not None:
            if var.address is not None:
                self.quadWrapper.insertAddress(var.address)
            else:
                self.quadWrapper.insertAddress(var.id)
            self.quadWrapper.insertType(var.type)

        self.ctxWrapper.addVariable(
            var,
            context=self.ctxWrapper.top(),
            insideClass=self.ctxWrapper.insideClass()
        )

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
                ty = str(ctx.funcParams().TYPE(i))
                func.addParamType(ty)

        # Function has primitive return type
        if ctx.TYPE() is not None:
            func.return_type = str(ctx.TYPE())
        # Function returns object
        elif len(ctx.ID()) > 1:
            func.return_type = str(ctx.ID(1))

        func.updateQuadsRange(start=self.quadWrapper.quads_ptr + 1)

        return func

    def enterFunction(self, ctx):
        if self.ctxWrapper.functionExistsInContext(ctx.ID(0), 'global'):
            raise error(ctx, FUNC_REDEFINITION.format(str(ctx.ID(0))))

        func = self.createFunction(ctx)
        self.ctxWrapper.addFunction(func)
        self.ctxWrapper.push('func ' + func.id)

    def exitFunction(self, ctx):
        func = self.ctxWrapper.getFunction(self.ctxWrapper.top())
        # If function is non-void verify it had at least one return inside
        if func.return_type != "void" and not self.func_returned_val:
            raise error(ctx, MUST_RETURN_ON_NON_VOID_FUNC.format(func.id))

        if func.quads_range[0] > self.quadWrapper.quads_ptr:
            func.updateQuadsRange(start=-1)
        else:
            func.updateQuadsRange(end=self.quadWrapper.quads_ptr)
            self.quadWrapper.insertQuad(Quadruple(
                op=ENDPROC
            ))

        self.ctxWrapper.pop()
        self.func_count -= 1
        self.func_returned_val = False  # Reset flag
        self.memHandler.flush(LOCAL)
        pass

    def getAccessType(self, ctx):
        ty = ctx.ACCESS_TYPE()
        return 'public' if ty is None else ty

    def enterClassDeclaration(self, ctx):
        class_id = str(ctx.ID())
        if self.ctxWrapper.classExists(class_id):
            raise error(ctx, CLASS_REDEFINITION.format(class_id))

        class_id = 'class ' + class_id
        self.ctxWrapper.push(class_id)

        parent_id = None
        if ctx.parent() is not None:
            parent_id = 'class ' + str(ctx.parent().ID())
            if not self.ctxWrapper.classExists(parent_id):
                raise error(ctx, UNDEF_PARENT.format(parent_id, class_id))

            # Inherit attributes
            for attr in self.ctxWrapper.variables[parent_id].values():
                if (type(attr) != dict # check if it's a method varTable
                        and attr.access_type != 'private'):
                    self.ctxWrapper.addVariable(attr, class_id)

            # Inherit functions
            for func in self.ctxWrapper.functions[parent_id].values():
                if func.access_type != 'private':
                    self.ctxWrapper.addFunction(func, class_id)

        # Parse class attributes
        for declarations in ctx.attributes():
            access_type = self.getAccessType(declarations)

            for attr in declarations.attribute():
                # Raise error if re-declaration (ignore inherited methods)
                if (self.ctxWrapper.varExistsInContext(attr.ID(), class_id)
                    and not self.ctxWrapper.varExistsInContext(attr.ID(), parent_id)):
                    raise error(ctx, VAR_REDEFINITION.format(attr.ID()))

                reserved_address = None
                # Type is defined explicitly, allocate memory
                if attr.TYPE() is not None:
                    reserved_address = self.memHandler.reserve(
                        context=tokenizeContext(class_id),
                        dtype=tokenize(attr.TYPE())
                    )
                # No type defined, raise error
                elif attr.assignment() is None:
                    raise error(
                        ctx, MUST_DECLARE_ATTRIBUTE_TYPE.format(str(attr.ID())))

                var = Variable(
                    id=attr.ID(),
                    type=attr.TYPE(),
                    access_type=access_type,
                    address=reserved_address
                )
                self.ctxWrapper.addVariable(var, class_id)

        # Parse class methods
        for method in ctx.method():
            access_type = self.getAccessType(method)

            # Raise error if re-declaration (ignore inherited methods)
            if (self.ctxWrapper.functionExistsInContext(method.ID(0), class_id)
                and not self.ctxWrapper.functionExistsInContext(method.ID(), parent_id)):
                raise error(ctx, FUNC_REDEFINITION.format(str(method.ID(0))))

            method = self.createFunction(method)
            method.access_type = str(access_type)

            self.ctxWrapper.addFunction(method, class_id)

        # Save snapshot of memory (so we can retain attributes after every method flush)
        self.memHandler.saveSnapshot(LOCAL)
        pass

    def exitClassDeclaration(self, ctx):
        self.ctxWrapper.pop()
        self.memHandler.flush(LOCAL)
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
        class_name = self.ctxWrapper.top()
        self.ctxWrapper.push('func ' + str(ctx.ID(0)))
        method = self.ctxWrapper.getFunction(self.ctxWrapper.top(), context=class_name)
        method.updateQuadsRange(start=self.quadWrapper.quads_ptr + 1)

    def exitMethod(self, ctx):
        name = self.ctxWrapper.pop()
        method = self.ctxWrapper.getFunction(
            name, context=self.ctxWrapper.top())
        if method.quads_range[0] > self.quadWrapper.quads_ptr:
            method.updateQuadsRange(start=-1)
        else:
            method.updateQuadsRange(end=self.quadWrapper.quads_ptr)

        self.quadWrapper.insertQuad(Quadruple(
            op=ENDPROC
        ))
        self.memHandler.restoreSnapshot(LOCAL)

    def enterStatement(self, ctx):
        self.statement = True
        # Check if Main Start
        if self.func_count == 0:
            # Fill GOTO to main start (so funcs dont get executed)
            self.quadWrapper.fillQuadWith(
                self.quadWrapper.quads_ptr + 1,
                at=self.quadWrapper.popJump() - 1
            )
            self.func_count = -1  # Reset flag

        self.if_cond = False
        if ctx.assignment() is not None:
            self.validateCalledIds(ctx)

            # Check if var_id is a single value var, or an array.

            # Before changes, the existence ctx.CONST_I() meant an array was being used as var.
            #

            if ctx.exp() is not None:
                # array_offset = self.getConstant(ctx, True)
                # self.quadWrapper.insertAddress(array_offset)
                self.array_indexation_exp = True

    def exitStatement(self, ctx):
        self.statement = False

    def enterBreakStmt(self, ctx):
        self.quadWrapper.insertJump()
        self.quadWrapper.insertQuad(Quadruple(GOTO))
        if not self.ctxWrapper.insideLoop():
            raise error(ctx, INVALID_BREAK_USE)

    def enterWhileLoop(self, ctx):
        self.if_cond = True
        self.quadWrapper.insertJump()
        self.ctxWrapper.pushLoop()

    def exitWhileLoop(self, ctx):
        goto_quad = Quadruple(GOTO)
        self.quadWrapper.insertQuad(goto_quad)
        self.ctxWrapper.popLoop()

        # Fill any breaks that might've been added inside loop
        while True:
            brk = self.quadWrapper.popJump()
            if brk is None or brk == OPENPAREN:
                break

            self.quadWrapper.fillQuadWith(
                self.quadWrapper.quads_ptr + 1,
                at=brk
            )

        # Fill while gotoF with next quad
        self.quadWrapper.fillQuadWith(
            self.quadWrapper.quads_ptr + 1,
            at=self.quadWrapper.popJump()
        )

        # Fill loop-end goto with loop start
        self.quadWrapper.fillQuadWith(
            self.quadWrapper.popJump() + 1,
            at=self.quadWrapper.quads_ptr - 1
        )

    def enterForLoop(self, ctx):
        pass

    def exitForLoop(self, ctx):
        pass

    def enterBranch(self, ctx):
        self.quadWrapper.insertJump(OPENPAREN)
        pass

    def exitBranch(self, ctx):
        self.if_cond = False

        # Ignore jumps inside else
        if ctx.elseStmt() is not None:
            else_jumps = self.quadWrapper.flushJumps()

        # Fill if and elseif GOTOs with next quad outside branch
        pending_jumps = []
        no_branches = 1 + len(ctx.elseIf())
        for _ in range(no_branches):
            pending_jumps += self.quadWrapper.flushJumps()

            branchEndJump = pending_jumps.pop()
            self.quadWrapper.fillQuadWith(
                self.quadWrapper.quads_ptr + 1,
                at=branchEndJump
            )

        self.quadWrapper.jump_stack += pending_jumps

        # Re-push else jumps
        if ctx.elseStmt() is not None:
            self.quadWrapper.jump_stack += else_jumps

    def enterIfStmt(self, ctx):
        self.if_cond = True

    def exitIfStmt(self, ctx):
        # Other jumps (breaks) might've been pushed inside If
        pending_jumps = self.quadWrapper.flushJumps()

        # Fill GOTOF with next quad
        self.quadWrapper.fillQuadWith(
            self.quadWrapper.quads_ptr + 2,
            at=self.quadWrapper.popJump()
        )

        # Re-push pending jumps
        self.quadWrapper.jump_stack += pending_jumps

        goto_quad = Quadruple(GOTO)
        self.quadWrapper.insertJump()
        self.quadWrapper.insertJump(OPENPAREN)
        self.quadWrapper.insertQuad(goto_quad)

    def enterElseIf(self, ctx):
        self.if_cond = True

    def exitElseIf(self, ctx):
        self.exitIfStmt(ctx)  # Rule is the same as if statement

    def enterElseStmt(self, ctx):
        pass

    def exitElseStmt(self, ctx):
        pass

    def enterReturnStmt(self, ctx):
        if self.ctxWrapper.top() == 'global':
            raise error(ctx, RETURN_OUTSIDE_FUNC)

        # Return is inside function, verify if not void
        func = self.ctxWrapper.getCurrentFunction()
        if func.return_type == 'void':
            raise error(ctx, RETURN_ON_VOID_FUNC.format(func.id))

    def exitReturnStmt(self, ctx):
        # Validate return type matches function return type
        func = self.ctxWrapper.getCurrentFunction()
        return_type = self.quadWrapper.popType()
        if return_type != func.return_type:
            raise error(ctx, INVALID_RETURN_TYPE.format(
                return_type, func.return_type))

        self.quadWrapper.insertQuad(Quadruple(
            op=GOTOR,
            res=self.quadWrapper.popAddress()
        ))
        self.func_returned_val = True

    def exitCond(self, ctx):
        if len(self.quadWrapper.operator_stack) > 0 and self.quadWrapper.operator_stack[-1] is OPENPAREN:
            self.quadWrapper.popOperator()

        if self.if_cond:
            cond_ty = self.quadWrapper.popType()
            if cond_ty != 'bool':
                raise error(ctx, EXPECTED_BOOL.format(cond_ty))

            gotof_quad = Quadruple(
                GOTOF,
                l=self.quadWrapper.popAddress()
            )
            self.quadWrapper.insertQuad(gotof_quad)
            self.quadWrapper.insertJump()
            # False bottom for filling breaks inside if/loop
            self.quadWrapper.insertJump(OPENPAREN)

        # Function call
        if self.param_count != -1:
            self.quadWrapper.insertQuad(Quadruple(
                op=PARAM,
                l=self.quadWrapper.popAddress(),
                res='param ' + str(self.param_count)
            ))
            self.param_count += 1

    def exitCmp(self, ctx):
        if self.quadWrapper.topOperator() in [ANDOP, OROP]:
            self.quadWrapper.generateQuad(ctx, self.memHandler)

    def exitExp(self, ctx):
        if self.quadWrapper.topOperator() in [LESSER, LESSEREQ, GREATER, GREATEREQ, EQUAL, NOTEQUAL]:
            self.quadWrapper.generateQuad(ctx, self.memHandler)

    def exitAdd(self, ctx):
        if self.quadWrapper.topOperator() in [ADD, SUBS]:
            self.quadWrapper.generateQuad(ctx, self.memHandler)

    def exitMultModDiv(self, ctx):
        if self.quadWrapper.topOperator() in [MULT, MOD, DIV]:
            self.quadWrapper.generateQuad(ctx, self.memHandler)

    # Helper to stringify 'constant' rule
    def getConstant(self, ctx, constantOnly=False):
        if constantOnly:
            return int(str(ctx.CONST_I()))
        if ctx.CONST_BOOL() is not None:
            value = str(ctx.CONST_BOOL()) == 'true'
            self.quadWrapper.insertType('bool')
        elif ctx.CONST_I() is not None:
            value = int(str(ctx.CONST_I()))
            self.quadWrapper.insertType('int')
        elif ctx.CONST_F() is not None:
            value = float(str(ctx.CONST_F()))
            self.quadWrapper.insertType('float')
        elif ctx.CONST_STR() is not None:
            value = str(ctx.CONST_STR())[1:-1]
            self.quadWrapper.insertType('string')
        else:
            self.quadWrapper.insertType('none')
            return 'none'

        return self.memHandler.reserve(
            context=CONSTANT,
            dtype=tokenizeByValue(value),
            value=value
        )
        # TODO: add arrays

    # Helper to validate id(s) being called (be them )
    def validateCalledIds(self, ctx, is_function=False):
        ids = [str(id) for id in ctx.ID()]
        if len(ids) == 2:  # class attr/method being called (i.e. myobj.name or myobj.print())
            selfAccess = ids[0] == 'self'
            if selfAccess:
                class_name = self.ctxWrapper.getClassContext()
                if class_name is None:
                    raise error(ctx, SELF_USE_OUTSIDE_CLASS)
            else:
                class_var = self.ctxWrapper.getVariable(ids[0])
                if class_var is None:
                    raise error(ctx, UNDEF_VAR.format(ids[0]))
                class_name = 'class ' + class_var['self'].type

            if is_function:
                method = self.ctxWrapper.getFunction(ids[1], context=class_name)
                if method is None:
                    raise error(ctx, UNDEF_METHOD.format(ids[1], class_name))
                # Validate that we can access method (if outside class)
                if not selfAccess and method.access_type != 'public':
                    raise error(ctx, NOT_PUBLIC_METHOD.format(
                        method.access_type.upper(), ids[1], class_name))
            else:
                attr = self.ctxWrapper.getVariable(ids[1], context=class_name)
                if attr is None:
                    raise error(ctx, UNDEF_ATTRIBUTE.format(ids[1], class_name))
                # Validate that we can access attribute (if outside class)
                if not selfAccess and attr.access_type != 'public':
                    raise error(ctx, NOT_PUBLIC_ATTRIBUTE.format(
                        attr.access_type.upper(), ids[1], class_name))

                self.quadWrapper.insertType(attr.type)
                self.quadWrapper.insertAddress(attr.address)

            return '.'.join(ids)
        else:  # global var/func being called
            id = ids[0]
            if is_function:
                func = self.ctxWrapper.getFunctionIfExists(id)
                if func is None:
                    raise error(ctx, UNDEF_FUNC.format(id))
            else:
                var, _ = self.ctxWrapper.getVariableIfExists(id)
                if var is None:
                    raise error(ctx, UNDEF_VAR.format(id))

                id = var.address
                self.quadWrapper.insertType(var.type)
                self.quadWrapper.insertAddress(var.address)

            return id

    def enterVal(self, ctx):
        if ctx.cond() is not None:  # nested cond
            # Add fake bottom to operator_stack
            self.quadWrapper.insertOperator('(')
        elif len(ctx.ID()) > 0:  # identifier
            self.validateCalledIds(ctx)
        elif ctx.constant() is not None:  # const
            self.quadWrapper.insertAddress(self.getConstant(ctx.constant()))

        # TODO implement arrays

    def exitVal(self, ctx):
        if self.quadWrapper.topOperator() in [POWER]:
            self.quadWrapper.generateQuad(ctx, self.memHandler)

    def enterBoolOp(self, ctx: PopurriParser.BoolOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterCmpOp(self, ctx: PopurriParser.CmpOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterAddOp(self, ctx: PopurriParser.AddOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterMultDivOp(self, ctx: PopurriParser.MultDivOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterAssignOp(self, ctx: PopurriParser.AssignOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterExpOp(self, ctx: PopurriParser.ExpOpContext):
        self.quadWrapper.insertOperator(ctx.getText())

    def enterIndexation(self, ctx):
        pass

    def exitIndexation(self, ctx):
        pass

    def enterAssignment(self, ctx):
        pass

    def exitAssignment(self, ctx):
        if self.quadWrapper.topOperator() in [ASSIGN, ADDASSIGN, SUBSASSIGN, MULTASSIGN, DIVASSIGN, MODASSIGN]:
            res_address = self.quadWrapper.popAddress()
            var_address = self.quadWrapper.popAddress()
            res_type = self.quadWrapper.popType()
            var_type = self.quadWrapper.popType()

            var = None
            # Assign resulting type to variable and allocate in memory
            if var_type == 'None':
                var, _ = self.ctxWrapper.getVariableIfExists(var_address)
                var.type = res_type
                var.address = self.memHandler.reserve(
                    context=tokenizeContext(self.ctxWrapper.top()),
                    dtype=tokenize(var.type)
                )
                var_type = res_type
            # Var already has a defined type (and thus allocated)
            else:
                var = self.ctxWrapper.getVariableByAddress(var_address)

            op = self.quadWrapper.popOperator()
            if op is not ASSIGN:
                res_type = bailaMijaConElSeñor(
                    op - 1, var_type, res_type)
                if res_type is None:
                    raise error(ctx, TYPE_MISMATCH.format(
                        stringifyToken(op), var_type, res_type))

            if var_type != res_type:
                raise error(ctx, TYPE_MISMATCH.format(
                    stringifyToken(op), var_type, res_type))

            if var.isArray:
                self.quadWrapper.insertQuad(Quadruple(
                    op=op,
                    l=res_address,
                    res=var.address + self.quadWrapper.popAddress()
                ))
            else:
                self.quadWrapper.insertQuad(Quadruple(
                    op=op,
                    l=res_address,
                    res=var.address
                ))

    def enterFuncCall(self, ctx):
        # TODO replace the id with its address in memory
        ids = self.validateCalledIds(ctx, is_function=True)
        self.quadWrapper.insertQuad(Quadruple(
            op=ERA,
            l=ids
        ))
        self.param_count = 1

    def exitFuncCall(self, ctx):
        ids = [str(id) for id in ctx.ID()]

        if len(ids) == 2:
            class_var = self.ctxWrapper.getVariable(ids[0])['self']
            func = self.ctxWrapper.getFunction(
                ids[1], 'class ' + class_var.type)
        else:
            func = self.ctxWrapper.getFunctionIfExists(ids[0])

        if self.param_count - 1 != len(func.paramTypes):
            raise error(ctx, PARAM_AMOUNT_MISMATCH.format(
                func.id, len(func.paramTypes)))

        # Validate call signature with function signature
        call_signature = tuple(self.quadWrapper.type_stack)
        func_signature = tuple(func.paramTypes)
        for func_ty in func_signature[::-1]:
            call_ty = self.quadWrapper.popType()
            if func_ty != call_ty:
                raise error(ctx, INVALID_SIGNATURE.format(
                    func.id, call_signature, func_signature))

        call = '.'.join(ids)

        self.quadWrapper.insertQuad(Quadruple(
            op=GOSUB,
            l=call
        ))

        # Allocate return value if using funcCall in expression (and if function returns something)
        if not self.statement:
            # Trying to use void function inside expression
            if func.return_type == 'void':
                raise error(
                    ctx, VOID_FUNCTION_CALL_ON_EXPRESSION.format(func.id))

            tmp = self.memHandler.reserve(
                context=TEMPORAL,
                dtype=tokenize(func.return_type)
            )

            self.quadWrapper.insertQuad(Quadruple(
                op=ASSIGN,
                l=call,
                res=tmp
            ))
            self.quadWrapper.insertAddress(tmp)

        # Reset parameter counter flag (So we dont add func quad when exiting a condition)
        self.param_count = -1

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
        self.quadWrapper.insertAddress('(')
        pass

    def exitPrintStmt(self, ctx):
        print_quads = []
        while True:
            address = self.quadWrapper.popAddress()
            if address is None or address == '(':
                break

            self.quadWrapper.popType()
            print_quads.append(Quadruple(
                op=PRINT,
                res=address
            ))

        # Quads are generated in inverse order (due to being in stack), so push them end to start
        for quad in print_quads[::-1]:
            self.quadWrapper.insertQuad(quad)

    def enterInputStmt(self, ctx):
        self.validateCalledIds(ctx)
        self.quadWrapper.insertQuad(Quadruple(
            op=INPUT,
            res=self.quadWrapper.popAddress()
        ))

    def exitInputStmt(self, ctx):
        pass

    def enterCondParam(self, ctx):
        pass

    def exitCondParam(self, ctx):
        pass

    def enterFuncParams(self, ctx):
        no_params = len(ctx.ID())
        for i in range(no_params):
            param = Variable(
                id=ctx.ID(i),
                type=ctx.TYPE(i),
            )
            param.address = self.memHandler.reserve(
                context=LOCAL,
                dtype=tokenize(param.type)
            )
            self.ctxWrapper.addVariable(
                param,
                context=self.ctxWrapper.top(),
                insideClass=self.ctxWrapper.insideClass()
            )

        pass

    def exitFuncParams(self, ctx):
        pass
