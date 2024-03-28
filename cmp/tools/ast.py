class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements) -> None:
        self.statements = statements
        
class StatementNode(Node):
    pass

class ExpressionNode(Node):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self, lex) -> None:
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, lnode, rnode) -> None:
        self.left = lnode
        self.right = rnode
        
# Declarations Nodes
class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr

class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body
    
 # Builtin Math functions

class SqrtNode(StatementNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class SinNode(StatementNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class CosNode(StatementNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class ExpNode(StatementNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class RandNode(AtomicNode):
    pass

class LogNode(StatementNode):
    def __init__(self, base_exp, exp_expr) -> None:
        self.base_expr = base_exp
        self.exp_expr = exp_expr
   
        
    
        
class ConstantNode(AtomicNode):
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























        
   
# class ClassDeclarationNode(StatementNode):
#     def __init__(self, idx, features, parent=None) -> None:
#         self.id = idx
#         self.features = features
#         self.parent = parent

# class AttrDeclarationNode(StatementNode):
#     def __init__(self, idx, typex, expr=None) -> None:
#         self.id = idx
#         self.type = typex
#         self.expr = expr

# class ParamNode(StatementNode):
#     def __init__(self, idx, typex) -> None:
#         self.id = idx
#         self.type = typex

# Expressions Nodes
class SimpleExpressionNode(ExpressionNode):
    def __init__(self, expr) -> None:
        self.expr = expr
            
class ConditionalNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, elif_expr, else_expr) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.elif_expr = elif_expr
        self.else_expr = else_expr

class WhileNode(ExpressionNode):
    def __init__(self, expr, body) -> None:
        self.expr = expr
        self.body = body

# list of variables declarations
class VarsDeclarationsNode(ExpressionNode):
    def __init__(self, decls, body) -> None:
        self.decls = decls
        self.body = body

# simple variable declaration
class VarNode(ExpressionNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr



class ParenthesisExpr(ExpressionNode):
    def __init__(self, expr) -> None:
        self.expr = expr

class BlockNode(ExpressionNode):
    def __init__(self, exprs) -> None:
        self.exprs = exprs

        




