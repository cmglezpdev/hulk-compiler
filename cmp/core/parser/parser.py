from cmp.evaluation import evaluate_reverse_parse
from cmp.pycompiler import Grammar
from cmp.tools.parsing.lr1 import LR1Parser
from cmp.utils import Token

G = Grammar()
program = G.NonTerminal('<program>', True)
class_list, function_list, expr_list = G.NonTerminals('<class-list> <function-list> <expr-list>')
classx, functionx, expr = G.NonTerminals('<class> <function> <expr>')


classx, ifx, elifx, elsex, inx, inherits, let = G.Terminals('class if elif else in inherits let')
idx, number, typex, string = G.Terminals('id Number type String')

semicolon, colon, comma, dot, opar, cpar, ocur, ccur, assign, case_sign = G.Terminals('; : , . ( ) { } <- =>')
plus, minus, star, div, less, less_eq, equal, int_comp, at = G.Terminals('+ - * / < <= = ~ @')


program %= class_list + function_list + expr_list



# Expressions
expr %= idx + assign + expr
# expr %= 









# E %= T + X
# E %= num 
# E %= G.Epsilon
# T %= num + X
# X %= plus + E | -E

def parse(tokens: list[Token]):
    print('>>> Parsing...')
    parse = LR1Parser(G, verbose=True)
    
    result = parse(tokens)
    
    right_parse, operations = result
    print(right_parse)
    
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    return ast