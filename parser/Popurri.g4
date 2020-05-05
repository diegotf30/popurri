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

ID: [_a-zA-Z][_a-zA-Z0-9]* [!?]?;

program:
	module classDeclaration* declarations* function* statement*;
module: 'module' ID;

declarations: 'var' declaration (',' declaration)*;
declaration: ID (':' (TYPE | ID))? assignment?;

function:
	'func' ID '(' funcParams? ')' (TYPE | ID)? '{' statement* '}';

classDeclaration:
	'class' parent? ID '{' (attributes | method)+ '}';
parent: ID '->';
attributes: ACCESS_TYPE? 'var' attribute (',' attribute)*;
attribute: ID (':' TYPE | assignment)?;
method:
	ACCESS_TYPE? 'func' ID '(' funcParams? ')' (TYPE | ID)? '{' statement* '}';

// Statements
statement:
	(ID '.')? ID assignment
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
elseStmt: 'else' '{' statement* '}';
returnStmt: 'return' cond;

cond: (cmp boolOp?)+;
cmp: (exp cmpOp?)+;
exp: (add addOp?)+;
add: (multModDiv multDivOp?)+;
multModDiv: (val expOp?)+;
val:
	'(' cond ')' |
	ID ('.' ID)? |
	constant |
	indexation; // TODO "addOp?"
indexation: iterable '[' exp ']';

// Operators
boolOp: 'and' | 'or';
cmpOp: '<' | '<=' | '>' | '>=' | 'is' | 'is not';
addOp: '+' | '-';
multDivOp: '*' | '/' | '%';
expOp: '**';
assignOp: '=' | '+=' | '-=' | '*=' | '/=' | '%=';

assignment: assignOp cond;
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

