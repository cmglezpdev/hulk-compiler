
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
        context.create_type('Number')
        context.create_type('Bool')
        context.create_type('String')
        context.create_type('Any')
        context.create_type('Void')
        context.create_type('Vec')

        context.create_type('Global')
        
        global_context = context.get_type('Global')
        
        
        global_context.define_method('print','x','Object','Void')
        global_context.define_method('sin','x','Number','Number')
        global_context.define_method('cos','x','Number','Number')
        global_context.define_method('tan','x','Number','Number')

        global_context.define_attribute('pi','Number')
        for statement in node.statements:
                self.visit(statement,context)
        return context
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node,context):
        context.define_attribute(node.id,node.type_of())

    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node,context):
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append('Object')
            param_names.append(param.id)
        context.define_method(node.id,param_names,param_types,node.body.type_of())
    
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node,context):        
        self.visit(node.body,context)
        param_types = []
        param_names = []
        for param in node.params:
            self.visit(param,context)
            param_types.append(param.type_of())
            param_names.append(param.id)
        context.define_method(node.id,param_names,param_types,node.body.type_of())
    