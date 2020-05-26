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
    var_dict = json.loads(f.readline())
    func_dict = json.loads(f.readline())
    return ContextWrapper(variables=var_dict, functions=func_dict)


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

    ip = 0
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
        elif op == GOTOF:
            if l_val == False:
                ip = res - 1
                continue
        elif op == GOTOV:
            if l_val == True:
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

        # Function Calls
        elif op == ERA:
            print('era')

        ip += 1