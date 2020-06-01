# Generated from Popurri.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PopurriParser import PopurriParser
else:
    from PopurriParser import PopurriParser

# This class defines a complete listener for a parse tree produced by PopurriParser.
class PopurriListener(ParseTreeListener):

    # Enter a parse tree produced by PopurriParser#program.
    def enterProgram(self, ctx:PopurriParser.ProgramContext):
        pass

    # Exit a parse tree produced by PopurriParser#program.
    def exitProgram(self, ctx:PopurriParser.ProgramContext):
        pass


    # Enter a parse tree produced by PopurriParser#module.
    def enterModule(self, ctx:PopurriParser.ModuleContext):
        pass

    # Exit a parse tree produced by PopurriParser#module.
    def exitModule(self, ctx:PopurriParser.ModuleContext):
        pass


    # Enter a parse tree produced by PopurriParser#declarations.
    def enterDeclarations(self, ctx:PopurriParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by PopurriParser#declarations.
    def exitDeclarations(self, ctx:PopurriParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by PopurriParser#declaration.
    def enterDeclaration(self, ctx:PopurriParser.DeclarationContext):
        pass

    # Exit a parse tree produced by PopurriParser#declaration.
    def exitDeclaration(self, ctx:PopurriParser.DeclarationContext):
        pass


    # Enter a parse tree produced by PopurriParser#function.
    def enterFunction(self, ctx:PopurriParser.FunctionContext):
        pass

    # Exit a parse tree produced by PopurriParser#function.
    def exitFunction(self, ctx:PopurriParser.FunctionContext):
        pass


    # Enter a parse tree produced by PopurriParser#classDeclaration.
    def enterClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by PopurriParser#classDeclaration.
    def exitClassDeclaration(self, ctx:PopurriParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by PopurriParser#parent.
    def enterParent(self, ctx:PopurriParser.ParentContext):
        pass

    # Exit a parse tree produced by PopurriParser#parent.
    def exitParent(self, ctx:PopurriParser.ParentContext):
        pass


    # Enter a parse tree produced by PopurriParser#attributes.
    def enterAttributes(self, ctx:PopurriParser.AttributesContext):
        pass

    # Exit a parse tree produced by PopurriParser#attributes.
    def exitAttributes(self, ctx:PopurriParser.AttributesContext):
        pass


    # Enter a parse tree produced by PopurriParser#attribute.
    def enterAttribute(self, ctx:PopurriParser.AttributeContext):
        pass

    # Exit a parse tree produced by PopurriParser#attribute.
    def exitAttribute(self, ctx:PopurriParser.AttributeContext):
        pass


    # Enter a parse tree produced by PopurriParser#method.
    def enterMethod(self, ctx:PopurriParser.MethodContext):
        pass

    # Exit a parse tree produced by PopurriParser#method.
    def exitMethod(self, ctx:PopurriParser.MethodContext):
        pass


    # Enter a parse tree produced by PopurriParser#statement.
    def enterStatement(self, ctx:PopurriParser.StatementContext):
        pass

    # Exit a parse tree produced by PopurriParser#statement.
    def exitStatement(self, ctx:PopurriParser.StatementContext):
        pass


    # Enter a parse tree produced by PopurriParser#whileLoop.
    def enterWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by PopurriParser#whileLoop.
    def exitWhileLoop(self, ctx:PopurriParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by PopurriParser#forLoop.
    def enterForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass

    # Exit a parse tree produced by PopurriParser#forLoop.
    def exitForLoop(self, ctx:PopurriParser.ForLoopContext):
        pass


    # Enter a parse tree produced by PopurriParser#branch.
    def enterBranch(self, ctx:PopurriParser.BranchContext):
        pass

    # Exit a parse tree produced by PopurriParser#branch.
    def exitBranch(self, ctx:PopurriParser.BranchContext):
        pass


    # Enter a parse tree produced by PopurriParser#ifStmt.
    def enterIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#ifStmt.
    def exitIfStmt(self, ctx:PopurriParser.IfStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#elseIf.
    def enterElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass

    # Exit a parse tree produced by PopurriParser#elseIf.
    def exitElseIf(self, ctx:PopurriParser.ElseIfContext):
        pass


    # Enter a parse tree produced by PopurriParser#elseStmt.
    def enterElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#elseStmt.
    def exitElseStmt(self, ctx:PopurriParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#returnStmt.
    def enterReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#returnStmt.
    def exitReturnStmt(self, ctx:PopurriParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#breakStmt.
    def enterBreakStmt(self, ctx:PopurriParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#breakStmt.
    def exitBreakStmt(self, ctx:PopurriParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#cond.
    def enterCond(self, ctx:PopurriParser.CondContext):
        pass

    # Exit a parse tree produced by PopurriParser#cond.
    def exitCond(self, ctx:PopurriParser.CondContext):
        pass


    # Enter a parse tree produced by PopurriParser#cmp.
    def enterCmp(self, ctx:PopurriParser.CmpContext):
        pass

    # Exit a parse tree produced by PopurriParser#cmp.
    def exitCmp(self, ctx:PopurriParser.CmpContext):
        pass


    # Enter a parse tree produced by PopurriParser#exp.
    def enterExp(self, ctx:PopurriParser.ExpContext):
        pass

    # Exit a parse tree produced by PopurriParser#exp.
    def exitExp(self, ctx:PopurriParser.ExpContext):
        pass


    # Enter a parse tree produced by PopurriParser#add.
    def enterAdd(self, ctx:PopurriParser.AddContext):
        pass

    # Exit a parse tree produced by PopurriParser#add.
    def exitAdd(self, ctx:PopurriParser.AddContext):
        pass


    # Enter a parse tree produced by PopurriParser#multModDiv.
    def enterMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass

    # Exit a parse tree produced by PopurriParser#multModDiv.
    def exitMultModDiv(self, ctx:PopurriParser.MultModDivContext):
        pass


    # Enter a parse tree produced by PopurriParser#val.
    def enterVal(self, ctx:PopurriParser.ValContext):
        pass

    # Exit a parse tree produced by PopurriParser#val.
    def exitVal(self, ctx:PopurriParser.ValContext):
        pass


    # Enter a parse tree produced by PopurriParser#indexation.
    def enterIndexation(self, ctx:PopurriParser.IndexationContext):
        pass

    # Exit a parse tree produced by PopurriParser#indexation.
    def exitIndexation(self, ctx:PopurriParser.IndexationContext):
        pass


    # Enter a parse tree produced by PopurriParser#boolOp.
    def enterBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#boolOp.
    def exitBoolOp(self, ctx:PopurriParser.BoolOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#cmpOp.
    def enterCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#cmpOp.
    def exitCmpOp(self, ctx:PopurriParser.CmpOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#addOp.
    def enterAddOp(self, ctx:PopurriParser.AddOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#addOp.
    def exitAddOp(self, ctx:PopurriParser.AddOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#unaryAddOp.
    def enterUnaryAddOp(self, ctx:PopurriParser.UnaryAddOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#unaryAddOp.
    def exitUnaryAddOp(self, ctx:PopurriParser.UnaryAddOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#multDivOp.
    def enterMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#multDivOp.
    def exitMultDivOp(self, ctx:PopurriParser.MultDivOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#expOp.
    def enterExpOp(self, ctx:PopurriParser.ExpOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#expOp.
    def exitExpOp(self, ctx:PopurriParser.ExpOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#assignOp.
    def enterAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass

    # Exit a parse tree produced by PopurriParser#assignOp.
    def exitAssignOp(self, ctx:PopurriParser.AssignOpContext):
        pass


    # Enter a parse tree produced by PopurriParser#assignment.
    def enterAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PopurriParser#assignment.
    def exitAssignment(self, ctx:PopurriParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PopurriParser#funcCall.
    def enterFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass

    # Exit a parse tree produced by PopurriParser#funcCall.
    def exitFuncCall(self, ctx:PopurriParser.FuncCallContext):
        pass


    # Enter a parse tree produced by PopurriParser#constant.
    def enterConstant(self, ctx:PopurriParser.ConstantContext):
        pass

    # Exit a parse tree produced by PopurriParser#constant.
    def exitConstant(self, ctx:PopurriParser.ConstantContext):
        pass


    # Enter a parse tree produced by PopurriParser#const_arr.
    def enterConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass

    # Exit a parse tree produced by PopurriParser#const_arr.
    def exitConst_arr(self, ctx:PopurriParser.Const_arrContext):
        pass


    # Enter a parse tree produced by PopurriParser#iterable.
    def enterIterable(self, ctx:PopurriParser.IterableContext):
        pass

    # Exit a parse tree produced by PopurriParser#iterable.
    def exitIterable(self, ctx:PopurriParser.IterableContext):
        pass


    # Enter a parse tree produced by PopurriParser#printStmt.
    def enterPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#printStmt.
    def exitPrintStmt(self, ctx:PopurriParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#printlnStmt.
    def enterPrintlnStmt(self, ctx:PopurriParser.PrintlnStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#printlnStmt.
    def exitPrintlnStmt(self, ctx:PopurriParser.PrintlnStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#inputStmt.
    def enterInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass

    # Exit a parse tree produced by PopurriParser#inputStmt.
    def exitInputStmt(self, ctx:PopurriParser.InputStmtContext):
        pass


    # Enter a parse tree produced by PopurriParser#condParam.
    def enterCondParam(self, ctx:PopurriParser.CondParamContext):
        pass

    # Exit a parse tree produced by PopurriParser#condParam.
    def exitCondParam(self, ctx:PopurriParser.CondParamContext):
        pass


    # Enter a parse tree produced by PopurriParser#funcParams.
    def enterFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass

    # Exit a parse tree produced by PopurriParser#funcParams.
    def exitFuncParams(self, ctx:PopurriParser.FuncParamsContext):
        pass



del PopurriParser