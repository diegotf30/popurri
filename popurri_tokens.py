# Tokens - Code operation

# GOTOS
GOTO = 0
GOTOV = 1
GOTOF = 2
GOSUB = 3
GOTOR = 4

# Functions
ERA = 5
PARAM = 6
ENDPROC = 7

# Operators
ADD = 8
ADDASSIGN = 9
SUBS = 10
SUBSASSIGN = 11
MULT = 12
MULTASSIGN = 13
DIV = 14
DIVASSIGN = 15
MOD = 16
MODASSIGN = 17
POWER = 18
EQUAL = 19
NOTEQUAL = 20
GREATER = 21
GREATEREQ = 22
LESSER = 23
LESSEREQ = 24
ANDOP = 25
OROP = 26
ASSIGN = 27

# Special functions
PRINT = 28
INPUT = 29

# Parenthesis
OPENPAREN = 30
CLOSEPAREN = 31

# Types
INT = 32
FLOAT = 33
BOOL = 34
STRING = 35

# Contexts
GLOBAL = 36
TEMPORAL = 37
LOCAL = 38
CONSTANT = 39

# (Internal use only)
FALSEBOTTOM = 999999

tokens = [
    'GOTO', 'GOTOV', 'GOTOF', 'GOSUB', 'GOTOR', # GOTOs
    'ERA', 'PARAM', 'ENDPROC', # Functions
    '+', '+=', '-', '-=', '*', '*=', '/', '/=', '%', '%=', '**', 'is', 'is not', '>', '>=', '<', '<=', 'and', 'or', '=', # Operators
    'print', 'input', # Special Functions
    '(', ')', # Parenthesis
    'int', 'float', 'bool', 'string', # Types
    'global', 'temporal', 'local', 'constant' # Contexts
]

def tokenize(v):
    if type(v) == int: # Already tokenized
        return v

    return tokens.index(str(v))

def tokenizeByValue(val):
    if type(val).__name__ == 'str':
        return tokens.index('string')

    return tokens.index(type(val).__name__)

def tokenizeContext(ctx_str):
    if ctx_str[:5] == 'class' or ctx_str[:4] == 'func':
        return LOCAL

    return GLOBAL

def stringifyToken(token):
    return tokens[token]