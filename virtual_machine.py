from PopurriListener import ContextWrapper, QuadWrapper, Variable, Function, pprint
from memory import MemoryHandler, Memory
from popurri_tokens import *
import json

def importMemory(f):
    memHandler = MemoryHandler()
    mem_dict = json.loads(f.readline())
    for ctx, mem_dict in mem_dict.items():
        memCtx = Memory(mem_dict['start'], mem_dict['max_size'])
        for section, spaces in mem_dict['sections'].items():
            memCtx.sections[int(section)] = spaces
        memHandler.contexts[int(ctx)] = memCtx

    return memHandler

def run(obj_file):
    with open(obj_file, 'r') as f:
        memHandler = importMemory(f)
        quads = json.loads(f.readline())

    for q in quads:
        print('[', stringifyToken(q[0]), *q[1:], ']', sep=' ')