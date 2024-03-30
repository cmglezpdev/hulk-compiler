class Node:
    def __str__(self):
        return "<Node>"

class TypeAnotationNode(Node):
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return "<TypeAnotationNode>"

class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements
    def __str__(self):
        ret = "<ProgramNode>"
        for statem in self.statements:
            ret+=str(statem)
        return ret

class StatementNode(Node):
    def __str__(self):
        return "<StatementNode>"

class ExpressionNode(Node):
    def __str__(self):
        return "<ExpressionNode>"

class VarsDeclarationsListNode(StatementNode):
    def __init__(self, declarations, body):
        self.declarations = declarations
        self.body = body
    def __str__(self):
        return f"<VarsDeclarationsListNode>: {str(self.declarations)} in {str(self.body)}"

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr
    def __str__(self):
        return f"<VarDeclarationNode>: let {self.id} = { str(self.expr) }"

class VarAssignation(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr
    def __str__(self):
        return f"<VarAssignation> {self.id} := {str(self.expr)}"

class FuncFullDeclarationNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body
    def __str__(self):
        return f"<FuncFullDeclarationNode> {self.id} ({str(self.params)}) {str(self.body)}"

class FuncInlineDeclarationNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body
    def __str__(self):
        return f"<FuncInlineDeclarationNode> {self.id}{str(self.params)} => {str(self.body)}"

class TypeDeclarationNode(StatementNode):
    def __init__(self, idx, args, features, inherit=None):
        self.id = idx
        self.args = args
        self.features = features
        self.inherit = inherit
    def __str__(self):
        return f"<TypeDeclarationNode> type {self.id} {self.features}"

class TypeInheritNode(StatementNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    def __str__(self):
        return "<TypeInheritNode>"

class AttrDeclarationNode(StatementNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr
    def __str__(self):
        return f"<AttrDeclarationNode> {self.id} {str(self.expr)}"

class VecDecExplSyntaxNode(StatementNode):
    def __init__(self, args):
        self.args = args
    def __str__(self):
        return f"<VecDecExplSyntaxNode> {str(self.args)}"

class VecDecImplSyntaxNode(ExpressionNode):
    def __init__(self, expr, var, in_):
        self.expr = expr
        self.var = var
        self.in_ = in_
    def __str__(self):
        return "<VecDecImplSyntaxNode>"

class VecInstNode(ExpressionNode):
    def __init__(self, var, index):
        self.var = var
        self.index = index
    def __str__(self):
        return "<VecInstNode>"

class ProtocolNode(ExpressionNode):
    def __init__(self, idx, methods, extends=None):
        self.id = idx
        self.extends = extends
        self.methods = methods
    def __str__(self):
        return "<ProtocolNode>"

class ProtocolMethod(ExpressionNode):
    def __init__(self, idx, typex, params):
        self.id = idx
        self.type = typex
        self.params = params
    def __str__(self):
        return "<ProtocolMethod>"

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex
    def __str__(self):
        return "<AtomicNode>"

class BinaryNode(ExpressionNode):
    def __init__(self, lnode, rnode):
        self.left = lnode
        self.right = rnode
    def __str__(self):
        return "<BinaryNode>"

class BlockNode(ExpressionNode):
    def __init__(self, exprs):
        self.exprs = exprs
    def __str__(self):
        return "<BlockNode>"

class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
    def __str__(self):
        return "<CallNode>"

class CallTypeAttr(ExpressionNode):
    def __init__(self, type_id, attr):
        self.type_id = type_id
        self.attr = attr
    def __str__(self):
        return "<CallTypeAttr>"

class CallTypeFunc(ExpressionNode):
    def __init__(self, type_id, func):
        self.type_id = type_id
        self.func = func
    def __str__(self):
        return "<CallTypeFunc>"

class NumberNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BooleanNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    def __init__(self, id, type='Any'):
        self.id = id
        self.type = type
    def __str__(self):
        return "<VariableNode>"

class InstantiateTypeNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
    def __str__(self):
        return "<InstantiateTypeNode>"

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
    pass

class StringSpaceConcatNode(BinaryNode):
    pass

class WhileLoopNode(ExpressionNode):
    def __init__(self, expr, body):
        self.expr = expr
        self.body = body
    def __str__(self):
        return "<WhileLoopNode>"

class ForLoopNode(ExpressionNode):
    def __init__(self, var, expr, body):
        self.var = var
        self.expr = expr
        self.body = body
    def __str__(self):
        return "<ForLoopNode>"

class IfNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, else_expr) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr
    def __str__(self):
        return "<IfNode>"

class ParamNode(StatementNode):
    def __init__(self, idx, typex=None):
        self.id = idx
        self.type = typex
    def __str__(self):
        return "<ParamNode>"

class ParenthesisExpr(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return "<ParenthesisExpr>"