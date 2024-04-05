from cmp import cil
from cmp.semantic import VariableInfo
import cmp.visitor as visitor
from cmp.tools.ast import *

class BaseHULKToCIL:
    def __init__(self):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None

    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
    
class HULKToCIL(BaseHULKToCIL):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode) 
    def visit(self, node, scope):
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

        for statements, child_scope in zip(node.statements, scope.children):
            self.visit(statements, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        var = self.register_local(VariableInfo(node.id, self.context.get_type(node.type_of())))
        self.current_vars[node.id] = var
        value = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(var, value))
        return var 
    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node, scope):
        
        self.current_function = self.register_function(node.id)
        self.current_vars = {}
        self.params.extend([cil.ParamNode(p) for p in node.params]) 
        
        value = None
        value = self.visit(node.body, scope)
        
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
        
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node, scope):
        
        self.current_function = self.register_function(node.id)
        self.current_vars = {}
        self.params.extend([cil.ParamNode(p) for p in node.params]) 
        
        value = None
        value = self.visit(node.body, scope)
        
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
        
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr, child_scope in zip(node.exprs, scope.children):
            self.visit(expr, child_scope)

    @visitor.when(CallNode)
    def visit(self, node, scope):

        value = self.visit(node.args, scope)
        if node.id == 'print':
            self.register_instruction(cil.PrintNode(value))
        print(node.id)
        print(node.args)

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.PlusNode(var, left, right))
        return var
        
    @visitor.when(MinusNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.MinusNode(var, left, right))
        return var
    
    @visitor.when(BinaryNode)
    def visit(self, node,scope):
        print(node.left)
        self.visit(node.left,scope)
        self.visit(node.right,scope)

    @visitor.when(StarNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.StarNode(var, left, right))
        return var
        

    @visitor.when(DivNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.DivNode(var, left, right))
        return var