class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements) -> None:
        self.statements = statements
        
class StatementNode(Node):
    pass

class ExpressionNode(Node):
    pass



       
# Declarations Nodes
class VarsDeclarationsListNode(StatementNode):
    def __init__(self, declarations) -> None:
        self.declarations = declarations

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr

class VarAssignation(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr

class FuncFullDeclarationNode(StatementNode):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body
    
class FuncInlineDeclarationNode(StatementNode):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body
    




class AtomicNode(ExpressionNode):
    def __init__(self, lex) -> None:
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, lnode, rnode) -> None:
        self.left = lnode
        self.right = rnode

class BlockNode(ExpressionNode):
    def __init__(self, exprs) -> None:
        self.exprs = exprs

class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex





class NumberNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BooleanNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass





# Operations

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class PowNode(BinaryNode):
    pass

class AndNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

class NotNode(AtomicNode):
    pass

class GreaterThatNode(BinaryNode):
    pass

class LessThatNode(BinaryNode):
    pass

class GreaterOrEqualThatNode(BinaryNode):
    pass

class LessOrEqualThatNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class NotEqualNode(BinaryNode):
    pass


class StringSimpleConcatNode(BinaryNode):
    """<string> @ <string>"""
    pass


class StringSpaceConcatNode(BinaryNode):
    """<string> @@ <string>"""
    pass



class WhileLoopNode(ExpressionNode):
    def __init__(self, expr, body) -> None:
        self.expr = expr
        self.body = body

class ForLoopNode(ExpressionNode):
    def __init__(self, ) -> None:
        super().__init__()

class IfNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, elif_expr, else_expr) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.elif_expr = elif_expr
        self.else_expr = else_expr






class TypeDeclarationNode(StatementNode):
    def __init__(self, idx, args, attrs, funcs, inherit=None) -> None:
        self.id = idx
        self.args = args
        self.attrs = attrs
        self.funcs = funcs
        self.inherit = inherit

class AttrDeclarationNode(StatementNode):
    def __init__(self, idx, typex, expr=None) -> None:
        self.id = idx
        self.type = typex
        self.expr = expr

# class ParamNode(StatementNode):
#     def __init__(self, idx, typex) -> None:
#         self.id = idx
#         self.type = typex

# Expressions Nodes
# class SimpleExpressionNode(ExpressionNode):
#     def __init__(self, expr) -> None:
#         self.expr = expr

# list of variables declarations
# class VarsDeclarationsListNode(ExpressionNode):
#     def __init__(self, decls, body) -> None:
#         self.decls = decls
#         self.body = body

# simple variable declaration

# class ParenthesisExpr(ExpressionNode):
#     def __init__(self, expr) -> None:
#         self.expr = expr




