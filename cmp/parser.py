from abc import ABC
from cmp.pycompiler import Grammar
from cmp.utils import Token

class Parser(ABC):
    def __init__(self, G: Grammar):
        self.G = G
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()
    
    def __call__(self, w):
        raise NotImplementedError()



class ShiftReduceParser(Parser, ABC):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        super().__init__(G)

    def __call__(self, w: list[Token], get_shift_reduce=False):
        stack = [ 0 ]
        cursor = 0
        output = []
        operations = []
        
        while True:
            state = stack[-1]
            lookahead = w[cursor].token_type
            if self.verbose: 
                print(stack, '<---||--->', w[cursor:])
                
            # (Detect error)
            if (state, lookahead) not in self.action:
                print('pila',stack)
                print((state, lookahead))
                print((w[:cursor], lookahead))
                print('Error, Aborting...')

                return None
            
            action, tag = self.action[state, lookahead]
            # (Shift case)
            if action == self.SHIFT:
                operations.append(self.SHIFT)
                stack += [lookahead, tag] # symbol, id
                cursor += 1
            # (Reduce case)
            elif action == self.REDUCE:
                operations.append(self.REDUCE)
                output.append(tag) # tag is a production
                head, body = tag
                for symbol in reversed(body):
                    stack.pop()
                    pop=stack.pop() # remove tag(id)
                    assert pop == symbol # remove symbol(lookahead)
                # transition with symbol(head)
                state=stack[-1]
                goto=self.goto[state,head]
                stack+=[head,goto]
            # (OK case)
            elif action == self.OK:
                stack.pop()
                pop = stack.pop()
                assert pop == self.G.startSymbol
                assert len(stack) == 1 # initial number 0
                return output if not get_shift_reduce else (output, operations)
            else:
            # (Invalid case)
                raise Exception(f'{action} is an invalid action!!')
