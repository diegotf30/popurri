grammar Popurri;

// Terminals
WS : [ \t\r\n]+ -> skip;
COMMENT : '//' .*? '\n' -> skip;
CONST_BOOL : 'true' | 'false';
CONST_I : [1-9][0-9]* | '0';
CONST_F : [0-9]* '.' [0-9]+;
CONST_STR : '\'' .*? '\'' | '"' .*? '"';
TYPE :  'int' | 'float' | 'string' | 'bool' | '[' ('float' | 'int' | 'bool') ']';
ID : [_a-zA-Z][_a-zA-Z0-9]*[!?]?;

program : module classDeclaration* declarations* function* statement*;
module : 'module' ID ;

declarations : 'var' declaration (',' declaration)* ;
declaration : ID (':' (TYPE | ID))? ('=' cond)?;

function : 'func' ID '(' funcParams? ')' (TYPE | ID)? '{' statement* '}' ;

classDeclaration : 'class' parent? ID '{' (accessType? (attributes | function))+ '}' ;
parent : ID '->';
accessType : 'public' | 'protected' | 'private';
attributes : 'var' attribute (',' attribute)* ;
attribute : ID (':' TYPE)? ('=' cond)?;

// Statements
statement : assignment | whileLoop | forLoop | branch | returnStmt | funcCall | printStmt | inputStmt | 'break';
	whileLoop : 'while' cond '{' statement* '}';
	forLoop : 'for' ID 'in' iterable '{' statement* '}';
	branch : ifStmt elseIf* elseStmt?;
		ifStmt : 'if' cond '{' statement* '}';
		elseIf : 'else if' cond '{' statement* '}';
		elseStmt : 'else' cond '{' statement* '}';
	returnStmt : 'return' cond;

	cond : ( cmp boolOp | 'not' )? cmp;
	cmp : exp (cmpOp exp)?;
	exp : add (addOp add)?;
	add : multModDiv (multDivOp multModDiv)?;
	multModDiv : val ('**' val)?;
	val : '(' cond ')' | addOp? (ID ('.' ID)? | constant | indexation);
	indexation : iterable '[' exp ']';

	assignment : (ID '.')? ID assignOp cond;
	funcCall : (ID '.')? ID '(' condParam? ')';

// Operators
boolOp : 'and' | 'or';
cmpOp : '<' | '<=' | '>' | '>=' | 'is' | 'is' 'not';
addOp : '+' | '-';
multDivOp : '*' | '/' | '%';
assignOp : '=' | '+=' | '-=' | '*=' | '/=' | '%=';

constant : CONST_BOOL | CONST_I | CONST_F | CONST_STR | const_arr | 'none';
const_arr : '[' (condParam? | exp 'to' exp ('by' exp)?) ']';
iterable : CONST_STR | const_arr | ID;

// Special functions
printStmt : 'print' '(' condParam ')';
inputStmt : 'input' '(' ID ')';

// Parameters
condParam : cond (',' cond)*;
funcParams : TYPE ID(',' TYPE ID)*;

