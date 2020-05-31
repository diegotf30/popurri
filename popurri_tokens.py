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
MINUS = 11
MINUSASSIGN = 12
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

# Unary Operators
UNARYADD = 29
UNARYMINUS = 30

# Special functions
PRINT = 31
PRINTLN = 32
INPUT = 33

# Parenthesis
OPENPAREN = 34
CLOSEPAREN = 35

# Types
INT = 36
FLOAT = 37
BOOL = 38
STRING = 39
POINTER = 40

# Contexts
GLOBAL = 41
LOCAL = 42
TEMPORAL = 43
CONSTANT = 44

# Arrays
VERIFY = 45

# (Internal use only)
FALSEBOTTOM = 999999

tokens = [
    'GOTO', 'GOTOV', 'GOTOF', 'GOSUB', 'GOTOR',  # GOTOs
    'ERAC',  # Classes
    'ERA', 'PARAM', 'ENDPROC',  # Functions
    '+', '+=', '-', '-=', '*', '*=', '/', '/=', '%', '%=', '**', 'is', 'is not', '>', '>=', '<', '<=', 'and', 'or', '=',  # Operators
    '+', '-',  # Unary Operators
    'print', 'println', 'input',  # Special Functions
    '(', ')',  # Parenthesis
    'int', 'float', 'bool', 'string', 'pointer',  # Types
    'global', 'local', 'temporal', 'constant',  # Contexts
    'verify',  # Arrays
]


def tokenize(v):
    if type(v) == int:  # Already tokenized
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
