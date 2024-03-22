
from cmp.pycompiler import Grammar
from cmp.automata import State
from cmp.parser import ShiftReduceParser
from cmp.pycompiler import Item
from cmp.tools.parsing.shared import compute_firsts, compute_follows

class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self) -> None:
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = self.build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: 
                print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item: Item = state.state
                if item.IsReduceItem:
                    prod = item.production
                    if prod.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in follows[prod.Left]:
                          self._register(self.action, (idx, symbol), (self.REDUCE, prod))  
                else:
                    symbol = item.NextSymbol
                    sidx = node.get(symbol.Name).idx # goto(Ii, <t>) = Ij
                    if symbol.IsTerminal:
                        self._register(self.action, (idx, symbol), (self.SHIFT, sidx))
                    else:
                        self._register(self.goto, (idx, symbol), sidx)
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value
    
    @staticmethod
    def build_LR0_automaton(G: Grammar) -> State:
        """
        ### Construcción del autómata LR(0)
        Implementemos el algoritmo para construir la versión no determinista del autómata LR(0). Recordemos de conferencia que:
        - Cada item representa un estado.
        - El estado inicial es representado por el item $S' \to .S$
        - Todos los estados son finales: _Todo prefijo de un prefijo viable es un prefijo viable_.
            - Una cadena no es un prefijo viable si el autómata se traba.
        - Función de transición:
            - $(X \to \alpha . c \beta) \longrightarrow^{c} (X \to \alpha c . \beta)$, con $c \in V_T$
            - $(X \to \alpha . Y \beta) \longrightarrow^{Y} (X \to \alpha Y . \beta)$, con $Y \in V_N$
            - $(X \to \alpha . Y \beta) \longrightarrow^{\epsilon} (Y \to .\delta)$, con $Y \in V_N$

            Args:
                G (_type_): _description_

            Returns:
                _type_: _description_
        """
            
        assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

        start_production = G.startSymbol.productions[0]
        start_item = Item(start_production, 0)
        automaton = State(start_item, True)

        pending = [ start_item ]
        visited = { start_item: automaton }

        while pending:
            current_item = pending.pop()
            current_state = visited[current_item]
            if current_item.IsReduceItem:
                continue
            
            next_item = current_item.NextItem()
            next_symbol = current_item.NextSymbol
            
            # include next_item state in the visited set
            try:
                visited[next_item]
            except Exception:
                visited[next_item] = State(next_item, True)
                pending.append(next_item)
            
            next_state = visited[next_item]
            # base transition to the next item
            current_state.add_transition(next_symbol.Name, next_state)
            
            if next_symbol.IsNonTerminal:
                # add extra transitions (epsilons)
                for production in G.Productions:
                    if production.Left == next_symbol: # only productions of type next_symbol -> .w
                        item = Item(production, 0)
                        try:
                            visited[item]
                            current_state.add_epsilon_transition(visited[item])
                        except Exception:
                            nstate = State(item, True)
                            visited[item] = nstate
                            current_state.add_epsilon_transition(nstate)
                            pending.append(item)
            
            # current_state = visited[current_item]
            # Your code here!!! (Add the decided transitions)
        return automaton

