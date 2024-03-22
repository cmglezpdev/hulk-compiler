from symtable import Symbol
from cmp.pycompiler import Grammar, Sentence
from cmp.utils import ContainerSet

def compute_local_first(firsts: dict[Symbol, ContainerSet], alpha: Sentence) -> ContainerSet:
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except KeyError:
        alpha_is_epsilon = False
    
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
        return first_alpha
        
    for symbol in alpha:
        first_alpha.hard_update(firsts[symbol])
        if symbol.IsTerminal or  not firsts[symbol].contains_epsilon:
            return first_alpha

    return first_alpha

def compute_firsts(G: Grammar) -> dict[Symbol, ContainerSet]:
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)

            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G: Grammar, firsts: dict[Symbol, ContainerSet]) -> dict[Symbol, ContainerSet]:
    follows = {}
    change = True
    
    local_firsts = {}
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
            
            for i, symbol in enumerate(alpha):
                if symbol.IsNonTerminal:
                    local_firsts = compute_local_first(firsts, alpha[i + 1:])
                    change |= follows[symbol].update(local_firsts)
                    if local_firsts.contains_epsilon or i == len(alpha) - 1:
                        change |= follows[symbol].update(follow_X)

    # Follow(Vn)
    return follows
