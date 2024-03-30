class Node:
    def __str__(self):
        return str(type(Node))

class TypeAnotationNode(Node):
    def __init__(self,type):
        self.type = type

class ProgramNode(Node):
    def __init__(self, statements) -> None:
        self.statements = statements
    def __str__(self):
        code =''
        for staement in self.statements:
            code += str(staement)
            print(staement)
        return code
        
        
class StatementNode(Node):
    pass

class ExpressionNode(Node):
    pass



       
# Declarations Nodes
class VarsDeclarationsListNode(StatementNode):
    def __init__(self, declarations, body) -> None:
        self.declarations = declarations
        self.body = body
    def __str__(self):
            return str(self.declarations) +' in '+str(self.body)

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr
    def __str__(self):
            return'let '+str(self.id)+' = '+str(self.expr)


class VarAssignation(StatementNode):
    def __init__(self, idx, expr) -> None:
        self.id = idx
        self.expr = expr
    def __str__(self):
            return str(self.id) +' := '+str(self.expr)

class FuncFullDeclarationNode(StatementNode):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body
    def __str__(self):
            return 'function '+ str(self.id) +'( '+str(self.params)+')'+str(self.body)
    
class FuncInlineDeclarationNode(StatementNode):
    def __init__(self, idx, params, body) -> None:
        self.id = idx
        self.params = params
        self.body = body
        
class TypeDeclarationNode(StatementNode):
    def __init__(self, idx, args, features, inherit=None) -> None:
        self.id = idx
        self.args = args
        self.features = features
        # self.attrs = attrs
        # self.funcs = funcs
        self.inherit = inherit

class TypeInheritNode(StatementNode):
    def __init__(self, idx, args) -> None:
        self.id = idx
        self.args = args

class AttrDeclarationNode(StatementNode):
    def __init__(self, idx, typex, expr=None) -> None:
        self.id = idx
        self.type = typex
        self.expr = expr

class VecDecExplSyntaxNode(StatementNode):
    def __init__(self, args) -> None:
        self.args = args

class VecDecImplSyntaxNode(ExpressionNode):
    def __init__(self, expr, var, in_) -> None:
        self.expr = expr
        self.var = var
        self.in_ = in_

class VecInstNode(ExpressionNode):
    def __init__(self, var, index) -> None:
        self.var = var
        self.index = index

class ProtocolNode(ExpressionNode):
    def __init__(self, idx, methods ,extends = None) -> None:
        self.id = idx
        self.extends = extends
        self.methods = methods

class ProtocolMethod(ExpressionNode):
    def __init__(self, idx, typex, params) -> None:
        self.id = idx
        self.type = typex
        self.params = params


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

class CallTypeAttr(ExpressionNode):
    def __init__(self, type_id, attr) -> None:
        self.type_id = type_id
        self.attr = attr

class CallTypeFunc(ExpressionNode):
    def __init__(self, type_id, func) -> None:
        self.type_id = type_id
        self.func = func

class NumberNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BooleanNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    def __init__(self,id,type='Any'):
      self.id=id
      self.type =type
    pass

class InstantiateTypeNode(ExpressionNode):
    def __init__(self, idx, args) -> None:
        self.id = idx
        self.args = args


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
    def __init__(self, var, expr, body) -> None:
        self.var = var
        self.expr = expr
        self.body = body

class IfNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, elif_expr, else_expr) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.elif_expr = elif_expr
        self.else_expr = else_expr








class ParamNode(StatementNode):
    def __init__(self, idx, typex=None) -> None:
        self.id = idx
        self.type = typex

class ParenthesisExpr(ExpressionNode):
    def __init__(self, expr) -> None:
        self.expr = expr




