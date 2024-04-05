
from cmp.semantic import Context
from cmp.tools.ast import *
from cmp import visitor



class TypeCollectorVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on("node")
    def visit(self, node,context:Context):
        pass    
    
    @visitor.when(ProgramNode)
    def visit(self, node, context=None):
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
    def visit(self, node,context):
        self.visit(node.expr)
        self.global_context.define_attribute(node.id,node.expr.type_of())

    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node,context):
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append('Object')
            param_names.append(param)
        try:
            self.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
        except Exception as e:
          pass
    
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node,context):        
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append('Object')
            param_names.append(param)
        try:
            self.global_context.define_method(node.id,param_names,param_types,node.body.type_of())
        except Exception as e:
            pass
    