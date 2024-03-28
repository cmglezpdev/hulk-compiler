from cmp.parser import ShiftReduceParser
from cmp.pycompiler import Grammar, Item, Symbol
from cmp.tools.parsing.shared import compute_firsts, compute_local_first
from cmp.utils import ContainerSet
from cmp.automata import State, multiline_formatter



class LR1Parser(ShiftReduceParser):
    
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = self.build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: 
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in item.lookaheads:
                            self._register(self.action, (idx, symbol), (self.REDUCE, item.production))
                else:
                    symbol = item.NextSymbol
                    goto = node[symbol.Name][0]
                    if symbol.IsTerminal:
                        self._register(self.action, (idx, symbol), (self.SHIFT, goto.idx))
                    else:
                        self._register(self.goto, (idx, symbol), goto.idx)
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value

    def expand(self, item: Item, firsts):
        print('entra al expand')
        G = self.G
        next_symbol = item.NextSymbol
        if next_symbol is None or not next_symbol.IsNonTerminal:
            return []
        
        lookaheads = ContainerSet()
        # (Compute lookahead for child items)
        print(item)
        print(item.Preview())
        for sentence in item.Preview():
            print(sentence)
            local_firsts = compute_local_first(firsts, sentence)
            lookaheads.update(local_firsts)
        
        print('primer for')
        assert not lookaheads.contains_epsilon
        # (Build and return child items)
        children = []
        for prod in G.Productions:
            if prod.Left == next_symbol:
                children.append(Item(prod, 0, lookaheads))
        
        print('sale del expand')
        return children

    def compress(self, items: list[Item]):
        centers = {}

        for item in items:
            center = item.Center()
            try:
                lookaheads = centers[center]
            except KeyError:
                centers[center] = lookaheads = set()
            lookaheads.update(item.lookaheads)
        
        return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

    def closure_lr1(self, items: list[Item], firsts: dict[Symbol, ContainerSet]):
        closure = ContainerSet(*items)
        print('ejaqui la cosa')
        print(items)
        
        changed = True

        while changed:
            changed = False
            
            new_items = ContainerSet()
            for item in closure:
                print('elitem',item)
                new_items.extend(self.expand(item, firsts))
                print('bien')

            changed = closure.update(new_items)
            
        print('salio del while')
        return self.compress(closure)

    def goto_lr1(self, items: list[Item], symbol: Symbol, firsts=None, just_kernel=False):
        assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
        items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
        return items if just_kernel else self.closure_lr1(items, firsts)

    def build_LR1_automaton(self, G: Grammar):
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
        
        firsts = compute_firsts(G)
        firsts[G.EOF] = ContainerSet(G.EOF)
        print('no se parte aqui') 
        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0, lookaheads=[G.EOF])
        start = frozenset([start_item])
        
        print('no se parte aqui') 
        closure = self.closure_lr1(start, firsts)
        print('no se parte aqui') 
        automaton = State(frozenset(closure), True)
        
        print('no se parte aqui') 
        pending = [ start ]
        visited = { start: automaton }
        
        while pending:
            current = pending.pop()
            current_state = visited[current]
            
            for symbol in G.terminals + G.nonTerminals:
                # (Get/Build `next_state`)
                next_items = self.goto_lr1(current_state.state, symbol, just_kernel=True)
                if not next_items:
                    continue
                
                try:
                    next_state = visited[next_items]
                except KeyError:
                    pending.append(next_items)
                    closure = self.closure_lr1(next_items, firsts)
                    visited[next_items] = State(frozenset(closure), True)
                    next_state = visited[next_items]
                
                current_state.add_transition(symbol.Name, next_state)
        
        automaton.set_formatter(multiline_formatter)
        return automaton

            
        
    