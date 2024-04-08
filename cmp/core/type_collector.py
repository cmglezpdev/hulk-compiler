
from cmp.semantic import Context
from cmp.tools.ast import *
from cmp import visitor



class TypeCollectorVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on("node")
    def visit(self, node,context:Context,type=None):
        pass    
    
    @visitor.when(ProgramNode)
    def visit(self, node, context=None,type=None):
        context = Context()
        obj =  context.create_type('Object')

        numb =context.create_type('Number')
        none =context.create_type('None')
        bool = context.create_type('Bool')
        str =context.create_type('String')
        void = context.create_type('Void')
        vec = context.create_type('Vec')

        self.global_context = context.create_type('Global')
        
        numb.set_parent(obj) 
        bool.set_parent(obj)
        str.set_parent(obj)
        void.set_parent(obj)
        vec.set_parent(obj)
        none.set_parent(obj)
        
        self.global_context.define_method('print','x','Object','Void')
        self.global_context.define_method('sin','x','Number','Number')
        self.global_context.define_method('cos','x','Number','Number')
        self.global_context.define_method('tan','x','Number','Number')

        self.global_context.define_attribute('pi','Number')
        for statement in node.statements:
                self.visit(statement,context)
        return context
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node,context,type=None):
        self.visit(node.expr,context)
        self.global_context.define_attribute(node.id,node.expr.type_of())

    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node,context,type=None):
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append('Object')
            param_names.append(param)
        try:
            if type is not None:
                type.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
            else:
                self.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
        except Exception as e:
          pass
    
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node,context,type=None):        
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append('Object')
            param_names.append(param)
        try:
            if type is not None:
                type.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
            else:
                self.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
        except Exception as e:
            pass
    
    @visitor.when(TypeDeclarationNode)
    def visit(self,node,context,type=None):
        type = context.create_type(node.id)
        if node.inherit :
            self.visit(node.inherit,context)
            try:
                p_type = context.get_type(node.inherit.id)
                type.set_parent(p_type)
            except Exception as e:
               pass

        for feature in node.features:
            self.visit(feature,context,type)
            
    
    @visitor.when(AttrDeclarationNode)
    def visit(self,node,context,type=None):
        self.visit(node.expr,context)
        try:
            type.define_attribute(node.id,node.expr.type_of())
        except Exception as e:
            self.errors.append(e)

    @visitor.when(ProtocolNode)
    def visit(self,node,context,tye=None):
        try:
         context.create_type(node.id)
        except:
            self.errors.append(f'invalid re declaration of {node.id} type')
        if node.extends is not None:
            self.visit(node.extends,context)
        for method in node.methods:
            self.visit(method,context)