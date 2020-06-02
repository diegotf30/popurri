grammar Popurri;

// Terminals

WS: [ \t\r\n]+ -> skip;
COMMENT: '#' .*? '\n' -> skip;
CONST_BOOL: 'true' | 'false';
CONST_I: [1-9][0-9]* | '0';
CONST_F: [0-9]* '.' [0-9]+;
CONST_STR: '\'' .*? '\'' | '"' .*? '"';

TYPE: 'int' | 'float' | 'string' | 'bool';
ACCESS_TYPE: 'public' | 'protected' | 'private';

ID: [_a-zA-Z][_a-zA-Z0-9]* [!?]?;

program:
	module classDeclaration* declarations* function* statement* EOF;
module: 'module' ID;

declarations: 'var' declaration (',' declaration)*;
//solamente he encontrado esta solucion al momento. Meter el parseo del arreglo en declaration, lo
// demas, por alguna razon, ignoraba el '['
declaration:
	ID (':' (TYPE | ID | '[' TYPE ']' '[' CONST_I ']'))? assignment?;

function:
	'func' ID '(' funcParams? ')' (TYPE | ID)? '{' declarations* statement* '}';

classDeclaration:
	'class' parent? ID '{' (attributes | method)+ '}';
parent: ID '->';
attributes: ACCESS_TYPE? 'var' attribute (',' attribute)*;
attribute: ID (':' (TYPE | '[' TYPE ']' '[' CONST_I ']'))?;
method:
	ACCESS_TYPE? 'func' ID '(' funcParams? ')' (TYPE | ID)? '{' declarations* statement* '}';

// Statements
statement: (
		(ID '.')? ID indexation? assignment
		| whileLoop
		| forLoop
		| branch
		| returnStmt
		| funcCall
		| printStmt
		| printlnStmt
		| inputStmt
		| breakStmt
	) COMMENT?;
whileLoop: 'while' cond '{' statement* '}';
forLoop: 'for' ID 'in' iterable '{' statement* '}';
branch: ifStmt elseIf* elseStmt?;
ifStmt: 'if' cond '{' statement* '}';
elseIf: 'else if' cond '{' statement* '}';
elseStmt: 'else' '{' statement* '}';
returnStmt: 'return' cond;
breakStmt: 'break';

cond: cmp (boolOp cmp)*;
cmp: exp (cmpOp exp)*;
exp: add (addOp add)*;
add: multModDiv (multDivOp multModDiv)*;
multModDiv: val (expOp val)*;
val:
	unaryAddOp? (
		'(' cond ')'
		| funcCall
		| ID ('.' ID)? indexation?
		| constant // TODO "addOp?"
	);
indexation: '[' exp ']';

// Operators
boolOp: 'and' | 'or';
cmpOp: '<' | '<=' | '>' | '>=' | 'is' | 'is not';
addOp: '+' | '-';
unaryAddOp: '+' | '-';
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
const_arr: '[' condParam? ']';
iterable: (ID '.')? ID | CONST_STR | const_arr;

// Special functions
printStmt: 'print' '(' condParam? ')';
printlnStmt: 'println' '(' condParam? ')';

inputStmt: 'input' '(' (ID '.')? ID ')';

// Parameters
condParam: cond (',' cond)*;
funcParams: TYPE ID (',' TYPE ID)*;

