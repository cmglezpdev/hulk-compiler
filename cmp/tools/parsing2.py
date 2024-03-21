from cmp.utils import ContainerSet

def compute_local_first(firsts, alpha):
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

def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    
    
    # parser construction...
    def parser(w):
        
        ###################################################
        # w ends with $ (G.EOF)
        ###################################################
        # init:
        stack =  [G.EOF, G.startSymbol]
        cursor = 0
        output = []
        ###################################################
        
        # parsing w...
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
                production = M[top, a][0]
                output.append(production)
                production = list(production.Right)
                stack.extend(production[::-1])

        # left parse is ready!!!
        return output
    
    # parser is ready!!!
    return parser
