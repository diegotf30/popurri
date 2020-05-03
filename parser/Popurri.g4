grammar Popurri;

// Terminals
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' .*? '\n' -> skip;
CONST_BOOL: 'true' | 'false';
CONST_I: [1-9][0-9]* | '0';
CONST_F: [0-9]* '.' [0-9]+;
CONST_STR: '\'' .*? '\'' | '"' .*? '"';
TYPE:
	'int'
	| 'float'
	| 'string'
	| 'bool'
	| '[' ('float' | 'int' | 'bool') ']';
ACCESS_TYPE: 'public' | 'protected' | 'private';

// Operators
BOOL_OP: 'and' | 'or';
CMP_OP: '<' | '<=' | '>' | '>=' | 'is' | 'is not';
ADD_OP: '+' | '-';
MULT_DIV_OP: '*' | '/' | '%';
ASSIGN_OP: '+=' | '-=' | '*=' | '/=' | '%=';

ID: [_a-zA-Z][_a-zA-Z0-9]* [!?]?;

program:
	module classDeclaration* declarations* function* statement*;
module: 'module' ID;

declarations: 'var' declaration (',' declaration)*;
declaration: ID (':' (TYPE | ID))? ('=' cond)?;

function:
	'func' ID '(' funcParams? ')' (TYPE | ID)? '{' statement* '}';

classDeclaration:
	'class' parent? ID '{' (attributes | method)+ '}';
parent: ID '->';
attributes: ACCESS_TYPE? 'var' attribute (',' attribute)*;
attribute: ID (':' TYPE)? ('=' cond)?;
method:
	ACCESS_TYPE? 'func' ID '(' funcParams? ')' (TYPE | ID)? '{' statement* '}';

// Statements
statement:
	assignment
	| whileLoop
	| forLoop
	| branch
	| returnStmt
	| funcCall
	| printStmt
	| inputStmt
	| 'break';
whileLoop: 'while' cond '{' statement* '}';
forLoop: 'for' ID 'in' iterable '{' statement* '}';
branch: ifStmt elseIf* elseStmt?;
ifStmt: 'if' cond '{' statement* '}';
elseIf: 'else if' cond '{' statement* '}';
elseStmt: 'else' cond '{' statement* '}';
returnStmt: 'return' cond;

cond: (cmp BOOL_OP?)+;
cmp: (exp CMP_OP?)+;
exp: (add ADD_OP?)+;
add: (multModDiv MULT_DIV_OP?)+;
multModDiv: (val '**'?)+;
val:
	'(' cond ')'
	| ADD_OP? (ID ('.' ID)? | constant | indexation);
indexation: iterable '[' exp ']';

assignment: (ID '.')? ID (ASSIGN_OP | '=') cond;
funcCall: (ID '.')? ID '(' condParam? ')';

constant:
	CONST_BOOL
	| CONST_I
	| CONST_F
	| CONST_STR
	| const_arr
	| 'none';
const_arr: '[' (condParam? | exp 'to' exp ('by' exp)?) ']';
iterable: CONST_STR | const_arr | ID;

// Special functions
printStmt: 'print' '(' condParam ')';
inputStmt: 'input' '(' ID ')';

// Parameters
condParam: cond (',' cond)*;
funcParams: TYPE ID (',' TYPE ID)*;

