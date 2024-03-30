class Node:
    def __init__(self, children=None):
        self.children = children if children is not None else []

    def __repr__(self):
        return self.__class__.__name__ + "(" + ", ".join(map(repr, self.children)) + ")"

class ProgramNode(Node):
    pass

class InstructionListNode(Node):
    pass

class InstructionNode(Node):
    pass

class ScopeNode(Node):
    pass

class FluxControlNode(Node):
    pass

class ExpressionNode(Node):
    pass

class VarDecNode(Node):
    pass

class VarInitializationListNode(Node):
    pass

class VarInitializationNode(Node):
    pass

class IdListNode(Node):
    pass

class IdentifierNode(Node):
    pass

class FullyTypedParamNode(Node):
    pass

class TypeAnotationNode(Node):
    pass

class ScopeNode(Node):
    pass

class AritmeticOperationNode(Node):
    pass

class FactorNode(Node):
    pass

class TermNode(Node):
    pass

class AtomNode(Node):
    pass

class VarAsignationNode(Node):
    pass

class FunctionDeclarationNode(Node):
    pass

class FunctionInlineDeclarationNode(Node):
    pass

class ConditionalNode(Node):
    pass

class InlineConditionalNode(Node):
    pass

class FullConditionalNode(Node):
    pass

class ElseStatementNode(Node):
    pass

class WhileLoopNode(Node):
    pass

class ForLoopNode(Node):
    pass

class ConditionalExpressionNode(Node):
    pass

class ComparationNode(Node):
    pass

class BooleanNode(Node):
    pass

class TypeDeclarationNode(Node):
    pass

class DeclBodyNode(Node):
    pass

class DeclListNode(Node):
    pass

class DeclarationNode(Node):
    pass

class AtributeDeclarationNode(Node):
    pass

class MethodDeclarationNode(Node):
    pass

class FunctionCallNode(Node):
    pass

class TypeInstanciationNode(Node):
    pass

class ParamListNode(Node):
    pass

class ParamNode(Node):
    pass

class VarUseNode(Node):
    pass

class VariableAtributeNode(Node):
    pass

class VariableMethodNode(Node):
    pass

class ProtocolDeclarationNode(Node):
    pass

class ProtocolDefinerNode(Node):
    pass

class ProtocolBodyNode(Node):
    pass

class VirtualMethodListNode(Node):
    pass

class VirtualMethodNode(Node):
    pass

class FullyTypedParamsNode(Node):
    pass

class VectorNode(Node):
    pass

class VectorDeclarationNode(Node):
    pass

class InlineFunctionNode(Node):
    pass

class ConditionalExpressionNode(Node):
    pass

class ComparationNode(Node):
    pass

class BooleanNode(Node):
    pass
