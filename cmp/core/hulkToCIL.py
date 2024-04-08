from cmp import cil
from cmp.semantic import VariableInfo
import cmp.visitor as visitor
from cmp.tools.ast import *
import math

class BaseHULKToCIL:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context

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
        self.dotdata.append(cil.DataNode('pi', math.pi))

        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        self.current_type = self.context.get_type('Global')

        for statements in node.statements:
            print(statements)
            self.visit(statements, scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        var = self.register_local(VariableInfo(node.id, self.context.get_type(node.type_of())))
        self.current_vars[node.id] = var
        value = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(var, value))
        return var 
    
    @visitor.when(VarsDeclarationsListNode)
    def visit(self, node, scope):
        self.visit(node.declarations,scope)
        print('------------------')
        print(node.declarations)
        print(type(node.body))
        # var = self.register_local(VariableInfo(node.id, self.context.get_type(node.type_of())))
        # self.current_vars[node.id] = var
        # value = self.visit(node.expr, scope)
        # self.register_instruction(cil.AssignNode(var, value))
        # return var 
    
    @visitor.when(FuncFullDeclarationNode)
    def visit(self, node, scope):
        
        self.current_method = self.current_type.get_method(node.id)
        
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, self.current_type.name))
        self.current_vars = {}
        self.params.append(cil.ParamNode('self'))
        self.params.extend([cil.ParamNode(p) for p in self.current_method.param_names]) 
        value = None
        value = self.visit(node.body, scope)
        
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
        
    @visitor.when(FuncInlineDeclarationNode)
    def visit(self, node, scope):
        
        self.current_method = self.current_type.get_method(node.id)

        self.current_function = self.register_function(self.to_function_name(self.current_method.name, self.current_type.name))
        self.current_vars = {}
        self.params.append(cil.ParamNode('self'))
        self.params.extend([cil.ParamNode(p) for p in self.current_method.param_names]) 
        
        value = None
        value = self.visit(node.body, scope)
        
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        
        type_node = self.register_type(self.current_type.name)
        
        visited_func = []
        current = self.current_type
        while current is not None:
            attributes = [attr.name for attr in current.attributes]
            methods = [func.name for func in current.methods if func.name not in visited_func]
            visited_func.extend(methods)
            type_node.attributes.extend(attributes[::-1])
            type_node.methods.extend([(item, self.to_function_name(item, current.name)) for item in methods[::-1]])
            current = current.parent
        
        type_node.attributes.reverse()
        type_node.methods.reverse()
        
              
        func_declarations = (f for f in node.features if (isinstance(f, FuncInlineDeclarationNode) or isinstance(f, FuncFullDeclarationNode) ))
        for feature in func_declarations:
            self.visit(feature, scope)
                
        self.current_type = self.context.get_type('Global')

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            self.visit(expr, scope)

    @visitor.when(CallNode)
    def visit(self, node, scope):
        value = self.visit(node.args[0], scope)
        if node.id == 'print':
            self.register_instruction(cil.PrintNode(value))
        elif node.id == 'sin':
            var = self.define_internal_local()
            self.register_instruction(cil.SenNode(var, value))
            return var
        elif node.id == 'cos':
            var = self.define_internal_local()
            self.register_instruction(cil.CosNode(var, value))
            return var
        elif node.id == 'tan':
            var = self.define_internal_local()
            self.register_instruction(cil.TanNode(var, value))
            return var
        elif node.id == 'pow':
            var = self.define_internal_local()
            self.register_instruction(cil.PowNode(var, value))
            return var
    
    @visitor.when(CallTypeAttr)
    def visit(self, node, scope):
        var = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(var, node.type_id, node.attr))
        return var

    @visitor.when(VarAssignation)
    def visit(self, node, scope):
        dest = self.visit(node.id, scope)
        self.register_instruction(cil.SetAttribNode(node.expr, dest))

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        self.register_instruction(cil.AssignNode(var, node.id))
        return var
    
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
    
    @visitor.when(NumberNode)
    def visit(self, node, scope):
        return node 