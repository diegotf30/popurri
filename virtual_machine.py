from PopurriListener import ContextWrapper, QuadWrapper, Variable, Function, pprint
from memory import MemoryHandler, Memory
from popurri_tokens import *
from error_tokens import *
from operator import *
import json

def importMemory(f):
    memHandler = MemoryHandler()
    mem_dict = json.loads(f.readline())
    for ctx, mem in mem_dict.items():
        memObj = Memory(mem['start'], mem['max_size'])
        for section, spaces in mem['sections'].items():
            memObj.sections[int(section)] = spaces

        memHandler.contexts[int(ctx)] = memObj

    return memHandler

def importContext(f):
    # Import Variables
    vars = json.loads(f.readline())
    for ctx in vars.values(): # Iterate over contexts
        for k,v in ctx.items():
            if 'func ' in k or 'self' in v: # Inside method/object varTable
                for vid, vdict in v.items():
                    if 'self' in vdict: # Var is object, iterate over attributes
                        for attrid, attrdict in vdict.items():
                            vdict[attrid] = Variable(**attrdict)
                    else:
                        v[vid] = Variable(**vdict)
            else:
                ctx[k] = Variable(**v)

    # Import Functions
    funcs = json.loads(f.readline())
    for ctx in funcs.values():
        for fid, fdict in ctx.items():
            ctx[fid] = Function(**fdict)

    return ContextWrapper(variables=vars, functions=funcs)


opMap = {
    ADD: add,
    SUBS: sub,
    MULT: mul,
    DIV: truediv,
    MOD: mod,
    POWER: pow,
    EQUAL: eq,
    NOTEQUAL: ne,
    GREATER: gt,
    GREATEREQ: ge,
    LESSER: lt,
    LESSEREQ: le,
}
def handleOperation(memHandler, op, l_val, r_val, res):
    opFunc = opMap[op]
    memHandler.update(res, opFunc(l_val, r_val))

def run(obj_file):
    with open(obj_file, 'r') as f:
        ctx = importContext(f)
        memHandler = importMemory(f)
        quads = json.loads(f.readline())

    # Reutilizing the ctx_stack in this wrapper to handle memory stacks
    memCtxWrapper = ContextWrapper()
    memCtxWrapper.pop() # Remove global context
    # Flag
    method_call = False
    # Instruction Pointer
    ip = 0
    ip_stack = []
    while ip < len(quads):
        quad = quads[ip]
        # print(ip + 1, '(', end='')
        # print(stringifyToken(quad[0]), *quad[1:], sep=', ', end='')
        # print(')')

        op, l, r, res = quad
        if type(l) == int:
            l_val = memHandler.getValue(l)
        if type(r) == int:
            r_val = memHandler.getValue(r)

        # GOTOs
        if op == GOTO:
            ip = res - 1
            continue
        elif (op == GOTOF and l_val == False or
              op == GOTOV and l_val == True):
            ip = res - 1
            continue

        # Operations
        elif op == ASSIGN:
            memHandler.update(res, l_val)
        elif op in [ADD, SUBS, MULT, DIV, MOD, POWER, EQUAL, NOTEQUAL, GREATER, GREATEREQ, LESSER, LESSEREQ]:
            handleOperation(memHandler, op, l_val, r_val, res)
        elif op == ANDOP: # For some reason these arent implemented in operator pkg, so do them manually
            memHandler.update(res, l_val and r_val)
        elif op == OROP:
            memHandler.update(res, l_val or r_val)
        elif op in [ADDASSIGN, SUBSASSIGN, MULTASSIGN, DIVASSIGN, MODASSIGN]:
            res_val = memHandler.getValue(res)
            # Move token one pos up, so ADDASSIGN -> ADD, SUBSASSIGN -> SUBS, etc.
            op -= 1
            # Applies short-hand operator and stores it in res
            handleOperation(memHandler, op, res_val, l_val, res)

        # Special Functions
        elif op == INPUT:
            res_type = memHandler.getAddressType(res)
            tmp = input()
            try:
                if res_type == INT:
                    tmp = int(tmp)
                elif res_type == FLOAT:
                    tmp = float(tmp)
                elif res_type == BOOL:
                    tmp = tmp == 'true'
                # Input is casted to string by default, so no need to cast
            except Exception:
                raise Exception(CANNOT_CAST.format(tmp, stringifyToken(res_type)))

            memHandler.update(res, tmp)
        elif op == PRINT:
            print(memHandler.getValue(res))

        # Classes
        elif op == ERAC:
            # Sleep current context
            memCtxWrapper.push(memHandler)
            memHandler.flush(LOCAL)
            memHandler.flush(TEMPORAL)

            class_var = ctx.getVariable(
                l,
                context=ctx.top(),
                insideClass=ctx.top() != 'global'
            )
            for attr in class_var.values():
                if attr.id == 'self': # this attribute only contains the class name
                    continue

                memHandler.reserve(
                    context=LOCAL,
                    dtype=tokenize(attr.type),
                )

            ctx.push('class ' + class_var['self'].type)
            method_call = True # Set flag so ERA quad doesnt flush mem

        # Function Calls
        elif op == ERA:
            # Sleep current context if calling regular function
            if not method_call:
                memCtxWrapper.push(memHandler)
                memHandler.flush(LOCAL)
                memHandler.flush(TEMPORAL)

            ctx.push('func ' + l)
            func = ctx.getCurrentFunction()

            # Allocate required function memory
            ctxs = [LOCAL, TEMPORAL]
            dtypes = [INT, FLOAT, BOOL, STRING]
            for i, era in enumerate([func.era_local, func.era_tmp]):
                for j, type_allocations in enumerate(era):
                    for _ in range(type_allocations):
                        memHandler.reserve(
                            context=ctxs[i],
                            dtype=dtypes[j],
                        )

            method_call = False # Reset flag
        elif op == PARAM:
            if ctx.insideClass():
                params = ctx.variables[ctx.getClassContext()][ctx.top()]
            else:
                params = ctx.variables[ctx.top()]

            paramNo = int(res.split(' ')[1]) # res is formatted as 'param N'
            # Update the local param address with the passed value
            for param in params.values():
                if param.paramNo == paramNo:
                    memHandler.update(
                        address=param.address,
                        value=l_val,
                    )
                    break

        elif op == GOSUB:
            func_id = l.split('.')[-1]
            func_ctx = ctx.getClassContext() if ctx.insideClass() else 'global'
            func = ctx.getFunction(func_id, func_ctx)
            if func.quads_range != (-1, -1):
                # Gonna return to this ip when returning from func
                ip_stack.append(ip + 1)
                # Go to function start
                ip = func.quads_range[0] - 1
                continue

        elif op == ENDPROC:
            # Return to
            ip = ip_stack.pop()
            continue

        ip += 1