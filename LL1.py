# from cmp.pycompiler import Symbol
# from cmp.pycompiler import NonTerminal
# from cmp.pycompiler import Terminal
# from cmp.pycompiler import EOF
# from cmp.pycompiler import Sentence, SentenceList
# from cmp.pycompiler import Epsilon
# from cmp.pycompiler import Production
# from cmp.pycompiler import Grammar
# from cmp.utils import pprint, inspect
from cmp.utils import ContainerSet

# Computes First(alpha), given First(Vt) and First(Vn) 
# alpha in (Vt U Vn)*
def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:  # noqa: E722
        alpha_is_epsilon = False
    
    ###################################################
    # alpha == epsilon ? First(alpha) = { epsilon }
    ###################################################
    if alpha_is_epsilon:
        first_alpha.set_epsilon()
        return first_alpha
        
    ###################################################
    # alpha = X1 ... XN
    # First(Xi) subconjunto First(alpha)
    # epsilon pertenece a First(X1)...First(Xi) ? First(Xi+1) subconjunto de First(X) y First(alpha)
    # epsilon pertenece a First(X1)...First(XN) ? epsilon pertence a First(X) y al First(alpha)
    ###################################################
    for symbol in alpha:
        first_alpha.hard_update(firsts[symbol])
        if symbol.IsTerminal or  not firsts[symbol].contains_epsilon:
            return first_alpha

    return first_alpha


# Computes First(Vt) U First(Vn) U First(alpha)
# P: X -> alpha
def compute_firsts(G):
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


def compute_follows(G, firsts):
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
            
            ###################################################
            # X -> zeta Y beta
            # First(beta) - { epsilon } subset of Follow(Y)
            # beta ->* epsilon or X -> zeta Y ? Follow(X) subset of Follow(Y)
            ###################################################
            for i, symbol in enumerate(alpha):
                if symbol.IsNonTerminal:
                    local_firsts = compute_local_first(firsts, alpha[i + 1:])
                    change |= follows[symbol].update(local_firsts)
                    if local_firsts.contains_epsilon or i == len(alpha) - 1:
                        change |= follows[symbol].update(follow_X)

    # Follow(Vn)
    return follows  


def build_parsing_table(G, firsts, follows):
    # init parsing table
    M = {}
    
    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
        
        ###################################################
        # working with symbols on First(alpha) ...
        ###################################################
        if not alpha.IsEpsilon:
            for first in firsts[alpha]:
                if (X, first) in M:
                    raise Exception(f'The grammar is not LL(1) because the pair({X}, {first}) has already asociated the production {M[X, first]} and want assign the production {production}')
                M[X, first] = [production]
        
        ###################################################
        # working with epsilon...
        ###################################################
        else:
            for follow in follows[X]:
                if (X, follow) in M:
                    raise Exception('La gramatica no es LL(1)')
                M[X, follow] = [production]
    
    # parsing table is ready!!!
    return M

