from cmp.pycompiler import NonTerminal, Production, Symbol, Terminal
from cmp.tools.parsing.shared import compute_firsts, compute_follows
from cmp.parser import Parser

class LL1Parser(Parser):
    def __init__(self, G):
        self.M: dict[(NonTerminal, Terminal), Production] = {}
        super().__init__(G)

    def _build_parsing_table(self):
        G = self.G
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        M = {} # [NonTerminal, Terminal] -> [Production]
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            if not alpha.IsEpsilon:
                for first in firsts[alpha]:
                    if (X, first) in M:
                        raise Exception(f'The grammar is not LL(1) because the pair({X}, {first}) has already asociated the production {M[X, first]} and want assign the production {production}')
                    M[X, first] = [production, ]
            else:
                for follow in follows[X]:
                    if (X, follow) in M:
                        raise Exception('La gramatica no es LL(1)')
                    M[X, follow] = [production, ]
        self.M = M

    def __call__(self, w: list[Symbol]):
        G, M = self.G, self.M

        stack =  [G.EOF, G.startSymbol]
        cursor = 0
        output = []
        
        while True:
            top = stack.pop()
            a = w[cursor]
            
            if top.IsEpsilon:
                pass
            elif top.IsTerminal:
                assert top == a
                if top == G.EOF:
                    break
                cursor += 1
            else:
                [production, ] = M[top, a]
                output.append(production)
                production = list(production.Right)
                stack.extend(production[::-1])

        return output
