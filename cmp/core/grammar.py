from cmp.pycompiler import Grammar
from cmp.tools.ast import ConstantNode, DivNode, MinusNode, PlusNode, StarNode, VariableNode

G = Grammar()
program = G.NonTerminal('<program>', True)

expr_def, arith_expr, term, factor, atom, const, idx = G.NonTerminals('<expr-def> <arith-expr> <term> <factor> <atom> <const> <idx>')

plus, minus, star, div, equal = G.Terminals('+ - * / =')
opar, cpar, ocur, ccur, comma, semmicolon = G.Terminals('( ) { } , ;')

# Expression definition
arith_expr %= arith_expr + plus + term, lambda h,s: PlusNode(s[1], s[3])
arith_expr %= arith_expr + minus + term, lambda h,s: MinusNode(s[1], s[3])
arith_expr %= term, lambda h,s: s[1]

term %= term + star + factor, lambda h,s: StarNode(s[1], s[3])
term %= term + div + factor, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1]

factor %= atom, lambda h,s: s[1]
factor %= opar + arith_expr + cpar, lambda h,s: s[2]

atom %= const, lambda h,s: ConstantNode(s[1])
atom %= idx, lambda h,s: VariableNode(s[1])
