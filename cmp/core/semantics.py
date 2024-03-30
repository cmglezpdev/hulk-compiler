from cmp.semantic import Scope,Context
from cmp.tools.ast import *
from cmp import visitor

class SemanticError:
    def __init__(self,message):
        self.message = message
    def str(self):
        return self.message


class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on("node")
    def visit(self, node,context:Context,scope: Scope):
        pass    
    
    @visitor.when(ProgramNode)
    def visit(self, node, context=None ,scope=None):
        scope = Scope()

        scope.define_variable('pi')

        scope.define_function('print',1)
        scope.define_function('sin',1)
        scope.define_function('cos',1)
        scope.define_function('tan',1)
        scope.define_function('pow',2)

        context = Context()
        print(len(node.statements))
        for statement in node.statements:
                self.visit(statement,context,scope)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node,context, scope):
        scope.define_variable(node.id) 
        self.visit(node.expression,context,scope)
    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node,context, scope):
        inner_scope =scope.create_child_scope()
        for n in node.params:
            inner_scope.define_variable(n)
        if scope.is_func_defined(node.id,len(node.params)):
            self.errors.append(f'function {node.id} already defined')
        else:
            scope.define_function(node.id,len(node.params))
        self.visit(node.body,context,inner_scope)
    
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node,context, scope):        
        inner_scope =scope.create_child_scope()
        for n in node.params:
            inner_scope.define_variable(n)

        if scope.is_func_defined(node.id,len(node.params)):
            self.errors.append(f'function {node.id} already defined')
        else:
            scope.define_function(node.id,len(node.params))
        self.visit(node.body,context,inner_scope)

 
    
    @visitor.when(BinaryNode)
    def visit(self, node,context,scope):
        self.visit(node.left,context,scope)
        self.visit(node.right,context,scope)

    @visitor.when(BlockNode)
    def visit(self,node,context,scope):
        new_scope = scope.create_child_scope()
        for expr in node.exprs:
            self.visit(expr,context,new_scope)


    @visitor.when(CallNode)
    def visit(self, node, context ,scope):
        is_valid = scope.is_func_defined(node.id,len(node.args))
        if not is_valid:
           self.errors.append(f'function {node.id} is not defined')
           return
        for arg in node.args:
            self.visit(arg,context,scope)


    @visitor.when(VariableNode)
    def visit(self, node,context ,scope):


        if  isinstance(node.id,str):
            if not scope.is_var_defined(node.id):
                print(type(node),type(node.id),node.id)
                self.errors.append(f'variable not defined {node.id}')
        else:
            self.visit(node.id)



    @visitor.when(VarAssignation)
    def visit(self,node,context,scope):
        if scope.is_var_defined(node.id):
            self.visit(node.expr,context,scope)
        else:
            self.errors.append(f'cannot asign to undefined var {node.id}')

    

    @visitor.when(VecDecExplSyntaxNode)
    def visit(self,node,context,scope):
          for arg in node.args:
              self.visit(arg,context,scope)

    @visitor.when(VecDecImplSyntaxNode)
    def visit (self,node,context,scope):
        new_scope = scope.create_child_scope()
        new_scope.define_variable(node.var.id)
        self.visit(node.expr,context,new_scope)

    @visitor.when(TypeDeclarationNode)
    def visit(self,node,context,scope):
        inner_scope = scope.create_child_scope()
        inner_scope.define_variable('self')
        context.create_type(node.id)
        if node.inherit :
            self.visit(node.inherit,context,inner_scope)
        for feature in node.features:
            self.visit(feature,context,inner_scope)
        
        for attr in inner_scope.local_vars:
            try:
                context.get_type(node.id).define_attribute(attr.name,'Any')
            except e:
                self.errors.append(e.message)

        for method in inner_scope.local_funcs:
            print(method.name)
            try:
                context.get_type(node.id).define_method(method.name,'Any','Any','Any')
            except e:
                self.errors.append(e.message)
           
    @visitor.when(TypeInheritNode)
    def visit(self,node,context,scope):
        context.get_type(node.id)
        pass

    @visitor.when(AttrDeclarationNode)
    def visit(self,node,context,scope):
        if scope.is_var_defined(node.id):
            self.errors.append(f'atribute duplication {node.id}')
            return
        scope.define_variable(node.id)
        child_scope = scope.create_child_scope()
        self.visit(node.expr,context,child_scope)

    @visitor.when(VecInstNode)
    def visit(self,node,context,scope):
        self.visit(node.var,context,scope)
        self.visit(node.index,context,scope)
    
    @visitor.when(InstantiateTypeNode)
    def visit(self,node,context,scope):
        context.get_type(node.id)

    
    @visitor.when(VarsDeclarationsListNode)
    def visit(self,node,context,scope):
        self.visit(node.declarations,context,scope)

    @visitor.when(VarDeclarationNode)
    def visit(self,node,context,scope):
        if scope.is_var_defined(node.id):
            self.errors.append(f'variable {node.id} already defined')
        self.visit(node.expr,context,scope.create_child_scope())

    @visitor.when(VarAssignation)
    def visit(self,node,context,scope):
        if isinstance(node.id,str):
            if not scope.is_var_defined(node.id):
                self.errors.append(f'variable {node.id} is not defined')
        else:
            self.visit(node.id,context,scope)
        self.visit(node.expr,context,scope.create_child_scope())
       
    @visitor.when(WhileLoopNode)
    def visit(self,node,context,scope):
        self.visit(node.expr,context,scope)
        self.visit(node.body,context,scope)

    @visitor.when(IfNode)
    def visit(self,node,context,scope):
        self.visit(node.if_expr,context,scope.create_child_scope())
        self.visit(node.then_expr,context,scope,scope.create_child_scope())
        self.visit(node.else_expr,context,scope,scope.create_child_scope())

    @visitor.when(WhileLoopNode)
    def visit(self,node,context,scope):
        self.visit(node.if_expr)

    @visitor.when(CallTypeAttr)
    def visit(self,node,context,scope):
       if not scope.is_var_defined(node.type_id) or  not scope.is_local_var(node.attr):
          self.errors.append(f'atribute {node.type_id}.{node.attr} not defined') 

   
    @visitor.when(VecInstNode)
    def visit(self,node,context,scope):
        if not scope.is_var_defined(node.var):
            self.errors.append(f'variable{node.var} not defined')