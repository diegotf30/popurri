from popurri_tokens import *

# Supported Operators
'''
boolOp    : 'and' | 'or'
cmpOp     : '<' | '<=' | '>' | '>=' | 'is' | 'is' 'not'
addOp     : '+' | '-'
multDivOp : '*' | '/' | '%'
assignOp  : '=' | '+=' | '-=' | '*=' | '/=' | '%='
expOp     : '**'
'''

# Supported Types
'''
TYPE      :  'int' | 'float' | 'str' | 'bool' | '[float]' | '[int]' | '[bool]'
'''


def bailaMijaConElSeñor(baile, mija=None, sr=None):
    return bailes[baile].get((mija, sr), None)

# Operations between user-defined classes are NOT allowed


# This semantic cube should be accesed using .get(), since it only describxes valid operations
# So the get() function handles an unvalid combination of types
bailes = {
    #### boolOp ####
    ANDOP: {
        ("bool", "bool"): "bool"
    },
    OROP: {
        ("bool", "bool"): "bool"
    },
    #### cmpOp ####
    LESSER: {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    LESSEREQ: {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    GREATER: {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    GREATEREQ: {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    EQUAL: {
        # Any
    },
    NOTEQUAL: {
        # Any
    },
    #### addOp ####
    ADD: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" + "bc" = "abc"
        ("str", "str"): "str"
    },
    SUBS: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    #### multDivOp ####
    MULT: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" * 3 = "aaa"
        ("str", "int"): "str",
        ("int", "str"): "str"
    },
    DIV: {
        # 3 / 10 = 0.33333
        ("int", "int"): "float",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    MOD: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    #### assignOp ####
    ASSIGN: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    #### expOp ####
    POWER: {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
}

# Append all combinations to "is" and "is not" operators
types = ['int', 'float', 'str', 'bool']
for op in [EQUAL, NOTEQUAL]:
    for left in types:
        for right in types:
            bailes[op][(left, right)] = "bool"


# TYPE      :  'int' | 'float' | 'str' | 'bool' | '[float]' | '[int]' | '[bool]'
