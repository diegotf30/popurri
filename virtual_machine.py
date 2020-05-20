from PopurriListener import MemoryHandler, ContextWrapper, QuadWrapper
import json

def run(obj_file):
    with open(obj_file, 'r') as f:
        vars = json.loads(f.readline())
        funcs = json.loads(f.readline())
        memory = json.loads(f.readline())
        quads = json.loads(f.readline())
        # TODO implement import function in each class