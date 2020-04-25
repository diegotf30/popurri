grammar Popurri;

// Operators
BOOLOP : 'and' | 'or';
CMPOP : '<' | '<=' | '>' | '>=' | 'is' | 'is' 'not';
ADDOP : '+' | '-';
MULTDIVOP : '*' | '/' | '%';
ASSIGNOP : '=' | '+=' | '-=' | '*=' | '/=' | '%=';

// Terminals
WS : [ \t\r\n]+ -> skip;
COMMENT : '//' .*? -> skip;
ID : [_a-zA-Z][_a-zA-Z0-9]*[!?]?;
CONST_BOOL : 'true' | 'false';
CONST_I : [1-9][0-9]*;
CONST_F : [0-9]* '.' [0-9]+;
CONST_STR : '\'' .*? '\'' | '"' .*? '"';
TYPE :  'int' | 'float' | 'string' | '[' ('float' | 'int') ']';

program : module declarations* classDeclaration* function* statement*;
module : 'module' ID '\n';

declarations : 'var' declaration (',' declaration)* '\n';
declaration : ID (':' (TYPE | ID))? ('=' cond)?;

function : 'func' ID '(' funcParams ')' TYPE '{' statement* '}' '\n';

classDeclaration : 'class' parent? ID '{' (accessType? (attributes | function) '\n')+ '}' '\n';
parent : ID '->';
accessType : 'public' | 'protected' | 'private';
attributes : 'var' attribute (',' attribute)* ;
attribute : ID (':' TYPE)? ('=' cond)?;

// Statements
statement : (whileLoop | forLoop | branch | returnStmt | assignment | funcCall | printStmt | inputStmt | 'break') '\n';
	whileLoop : 'while' cond '{' statement* '}';
	forLoop : 'for' ID 'in' iterable '{' statement* '}';
	branch : ifStmt elseIf* elseStmt?;
		ifStmt : 'if' cond '{' statement* '}';
		elseIf : 'else if' cond '{' statement* '}';
		elseStmt : 'else' cond '{' statement* '}';
	returnStmt : 'return' cond;

	cond : ( cmp BOOLOP | 'not' )? cmp;
	cmp : exp (CMPOP exp)?;
	exp : add (ADDOP add)?;
	add : multModDiv (MULTDIVOP multModDiv)?;
	multModDiv : val ('**' val)?;
	val : '(' cond ')' | ADDOP? (ID | constant | indexation);
	indexation : iterable '[' exp ']';

	assignment : (ID '.')? ID ASSIGNOP cond;
	funcCall : (ID '.')? ID ('(' condParam ')')?;


constant : CONST_BOOL | CONST_I | CONST_F | CONST_STR | const_arr | 'none';
const_arr : '[' condParam? ']' | '[' exp 'to' exp ('by' exp)? ']';
iterable : CONST_STR | const_arr | ID;

// Special functions
printStmt : 'print' '(' condParam ')';
inputStmt : 'input' '(' ID ')';

// Parameters
condParam : cond (',' cond)*;
funcParams : TYPE ID(',' TYPE ID)*;

