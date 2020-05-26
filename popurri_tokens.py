# Tokens - Code operation

# GOTOS
GOTO = 0
GOTOV = 1
GOTOF = 2
GOSUB = 3
GOTOR = 4

# Class
ERAC = 5

# Functions
ERA = 6
PARAM = 7
ENDPROC = 8

# Operators
ADD = 9
ADDASSIGN = 10
SUBS = 11
SUBSASSIGN = 12
MULT = 13
MULTASSIGN = 14
DIV = 15
DIVASSIGN = 16
MOD = 17
MODASSIGN = 18
POWER = 19
EQUAL = 20
NOTEQUAL = 21
GREATER = 22
GREATEREQ = 23
LESSER = 24
LESSEREQ = 25
ANDOP = 26
OROP = 27
ASSIGN = 28

# Special functions
PRINT = 29
INPUT = 30

# Parenthesis
OPENPAREN = 31
CLOSEPAREN = 32

# Types
INT = 33
FLOAT = 34
BOOL = 35
STRING = 36

# Contexts
GLOBAL = 37
LOCAL = 38
TEMPORAL = 39
CONSTANT = 40

# (Internal use only)
FALSEBOTTOM = 999999

tokens = [
    'GOTO', 'GOTOV', 'GOTOF', 'GOSUB', 'GOTOR', # GOTOs
    'ERAC', # Classes
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