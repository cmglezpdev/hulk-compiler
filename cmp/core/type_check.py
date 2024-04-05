from cmp.semantic import Context
from cmp.tools.ast import *
from cmp import visitor

class TypeCheckingVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on("node")
    def visit(self, node,context:Context):
        pass    
    
    @visitor.when(ProgramNode)
    def visit(self, node, context=None):
        self.errors=[]
        for statement in node.statements:
                self.visit(statement,context)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node,context):
        self.visit(node.expression,context)

    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node,context):
        self.visit(node.body,context)
        self.visit(node.params,context)
    
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node,context):        
        self.visit(node.body,context)
        self.visit(node.params,context)
    
    @visitor.when(BinaryNode)
    def visit(self, node,context):
        self.visit(node.left,context)
        self.visit(node.right,context)
        
        global_cont = context.get_type('Global')
        
        type1 = context.get_type(node.left.type_of())
        type2 = context.get_type(node.right.type_of())
        
        if not type1.conforms_to(type2):
            self.errors.append(f'mismatch types between {str(node.left)} and {str(node.right)} ({type1.name} and {type2.name})')

    @visitor.when(BlockNode)
    def visit(self,node,context):
        for expr in node.exprs:
            self.visit(expr,context)


    @visitor.when(CallNode)
    def visit(self, node, context):
        for arg in node.args:
            self.visit(arg,context)
        try:
            type = context.get_type(node.id).attributes[0]
            node.set_type(type)
        except:
            pass


        


    @visitor.when(VariableNode)
    def visit(self, node,context):
        try:
            node.set_type(context.get_type(node.type_of()))
        except:
            pass
            # self.errors(f"variable {node.id} is from an invalid type")          
             


    @visitor.when(VarAssignation)
    def visit(self,node,context):
            self.visit(node.expr,context)

            if node.type_of() != node.expr.type_of():
                self.errors(f'no se puede asignar {node.type_of()} a {node.expr.type_of()}')

    

    @visitor.when(VecDecExplSyntaxNode)
    def visit(self,node,context):
          for arg in node.args:
              self.visit(arg,context)

    @visitor.when(VecDecImplSyntaxNode)
    def visit (self,node,context):
        self.visit(node.expr,context)

    @visitor.when(TypeDeclarationNode)
    def visit(self,node,context):
        if node.inherit :
            self.visit(node.inherit,context)
        for feature in node.features:
            self.visit(feature,context)
        
    @visitor.when(CallTypeAttr)
    def visit(self,node,context):
         self.visit(node.attr,context)
           

    @visitor.when(AttrDeclarationNode)
    def visit(self,node,context):
        self.visit(node.expr,context)

    @visitor.when(VecInstNode)
    def visit(self,node,context):
        self.visit(node.var,context)
        self.visit(node.index,context)
    
    @visitor.when(InstantiateTypeNode)
    def visit(self,node,context):
        pass

    
    @visitor.when(VarsDeclarationsListNode)
    def visit(self,node,context):
        self.visit(node.declarations,context)

    @visitor.when(VarDeclarationNode)
    def visit(self,node,context):
        self.visit(node.expr,context)

    @visitor.when(VarAssignation)
    def visit(self,node,context):
        self.visit(node.expr,context)
        if isinstance(node.id,str) and node.type != 'Object':
                if node.type == node.expr.type:
                    self.errors.append(f'variable {node.id} is not defined')
        else:
            self.visit(node.id,context)
       
    @visitor.when(WhileLoopNode)
    def visit(self,node,context):
        self.visit(node.expr,context)
        self.visit(node.body,context)

        if node.expr.type != 'Bool':
            self.errors.append(f'can not use {node.expr.type} as Bool')

    @visitor.when(IfNode)
    def visit(self,node,context):
        self.visit(node.if_expr,context)
        self.visit(node.then_expr,context)
        self.visit(node.elsse_expr,context)

        if node.expr.type != 'Bool':
            self.errors.append(f'can not use {node.expr.type} as Bool')


    @visitor.when(CallTypeAttr)
    def visit(self,node,context):
        pass

   
    @visitor.when(VecInstNode)
    def visit(self,node,context):
        self.visit(node.var,context)
        self.visit(node.index,context)

    @visitor.when(ProtocolNode)
    def visit(self,node,context):
        try:
         context.create_type(node.id)
        except:
            self.errors.append(f'invalid re declaration of {node.id} type')
        if node.extends is not None:
            self.visit(node.extends)
        
           