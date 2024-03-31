
from cmp.semantic import Context
from cmp.tools.ast import *
from cmp import visitor



class TypeCollectorVisitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on("node")
    def visit(self, node,context:Context):
        pass    
    
        
           