# Supported Operators
'''
boolOp    : 'and' | 'or'
cmpOp     : '<' | '<=' | '>' | '>=' | 'is' | 'is' 'not'
addOp     : '+' | '-'
multDivOp : '*' | '/' | '%'
assignOp  : '=' | '+=' | '-=' | '*=' | '/=' | '%='
'''

# Supported Types
'''
TYPE      :  'int' | 'float' | 'string' | 'bool' | '[float]' | '[int]' | '[bool]'
'''

# Operations between user-defined classes are NOT allowed

# This semantic cube should be accesed using .get(), since it only describes valid operations
# So the get() function handles an unvalid combination of types
bailes = {
    #### boolOp ####
    "and": {
        ("bool", "bool"): "bool"
    },
    "or": {
        ("bool", "bool"): "bool"
    },
    #### cmpOp ####
    "<": {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    "<=": {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    ">": {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    ">=": {
        ("int", "int"): "bool",
        ("int", "float"): "bool",
        ("float", "int"): "bool",
        ("float", "float"): "bool"
    },
    "is": {
        # Any
    },
    "is not": {
        # Any
    },
    #### AssignOp ####
    "=": {
        ("int", "int"): "int",
        ("int", "float"): "int",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" + "bc" = "abc"
        ("string", "string"): "string"
    },
    #### addOp ####
    "+": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" + "bc" = "abc"
        ("string", "string"): "string"
    },
    "+=": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" + "bc" = "abc"
        ("string", "string"): "string"
    },
    "-": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    "-=": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    #### multDivOp ####
    "*": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" * 3 = "aaa"
        ("string", "int"): "string",
        ("int", "string"): "string"
    },
    "*=": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float",
        # "a" * 3 = "aaa"
        ("string", "int"): "string",
        ("int", "string"): "string"
    },
    "/": {
        # 3 / 10 = 0.33333
        ("int", "int"): "float",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    "/=": {
        # 3 / 10 = 0.33333
        ("int", "int"): "float",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    "%": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
    "%=": {
        ("int", "int"): "int",
        ("int", "float"): "float",
        ("float", "int"): "float",
        ("float", "float"): "float"
    },
}

# Append all combinations to "is" and "is not" operators
types = ['int', 'float', 'string', 'bool']
for op in ["is", "is not"]:
    for left in types:
        for right in types:
            bailes[op][(left, right)] = "bool"


# TYPE      :  'int' | 'float' | 'string' | 'bool' | '[float]' | '[int]' | '[bool]'
