from cmp.pycompiler import Grammar

G = Grammar()
program = G.NonTerminal('<program>', True)
class_list, function_list, expr_def = G.NonTerminals('<class-list> <function-list> <expr-def>')
classx, functionx, expr = G.NonTerminals('<class> <function> <expr>')


let_expr, if_expr, while_expr = G.NonTerminals('<let_expr> <if_expr> <while_expr>')
decls, expr_body, decl, more_decls, more_exprs = G.NonTerminals('<decls> <expr_body> <decl> <more-decls> <more-expr>')
elif_exprs, else_expr, elem_expr = G.NonTerminals('<elif-expr> <else-expr> <elem-expr>')

classx, ifx, elifx, elsex, inx, inherits, let, whilex = G.Terminals('class if elif else in inherits let while')
idx, number, typex, string = G.Terminals('id Number type String')

semicolon, colon, comma, dot, opar, cpar, ocur, ccur, assign = G.Terminals('; : , . ( ) { } :=')
plus, minus, star, div, mod = G.Terminals('+ - * / %')
and_lgc, or_lgc, neg_lgc, at, db_at = G.NonTerminals('& | ! @ @@')
less, less_eq, greater, greater_eq, equal, equal_cmp, diff = G.NonTerminals('< <= > >= = == !=')

# basic hulk program
program %= class_list + function_list + expr_def 

# these are Epsilons because are not define yet
class_list %= G.Epsilon
function_list %= G.Epsilon

# Maybe there is an expression
expr_def %= expr + semicolon
expr_def %= G.Epsilon

# <expr> := <let-expr>
# | <if-expr>
# | <while-expr>
# | <case-expr>
# | <assign-expr>
# | <array-expr>
# | <inst-expr>
# | <elem-expr>
expr %= let_expr | if_expr | while_expr

# <let-expr> := let <decls> in <expr-body>
# <decls> := <decl> [, <decl>]*
# <decl> := ID [: ID] = <expr>
# <expr-body> := <expr>
# | { [<expr> ;]+ }
let_expr %= let + decls + inx + expr_body
decls %= decl + more_decls
more_decls %= comma + decls | G.Epsilon
decl %= idx + equal + expr
expr_body %= expr | ocur + expr + more_exprs + ccur
more_exprs %= expr + semicolon + more_exprs | G.Epsilon

# <if-expr> := if ( <expr> ) <expr-body>
# [elif ( <expr> ) <expr-body>]*
# [else <expr-body>]
if_expr %= ifx + opar + expr + cpar + expr_body + elif_exprs + else_expr
elif_exprs %= elifx + opar + expr + cpar + expr_body | G.Epsilon
else_expr %= elsex + expr_body | G.Epsilon

# <while-expr> := while ( <expr> ) <expr-body>
# [else <expr-body>]
while_expr %= whilex + opar + expr + cpar + expr_body + else_expr

# <elem-expr> := <expr> == <expr> | <expr> != <expr>
# | <expr> < <expr> | <expr> > <expr>
# | <expr> <= <expr> | <expr> >= <expr>
# | <expr> & <expr> | <expr> '|' <expr> | !<expr>
# | <expr> @ <expr> | <expr> @@ <expr>
# | <expr> + <expr> | <expr> - <expr>
# | <expr> % <expr> | <expr> * <expr> | <expr> / <expr>
# | <expr> [ '[' <expr> ']' ]?
# | [<expr> .] ID [( <args> )]?
# | -<expr> | ( <expr> )
elem_expr %= expr + equal_cmp + expr
elem_expr %= expr + diff + expr
elem_expr %= expr + less + expr
elem_expr %= expr + less_eq + expr
elem_expr %= expr + greater + expr
elem_expr %= expr + greater_eq + expr
elem_expr %= expr + and_lgc + expr
elem_expr %= expr + or_lgc + expr
elem_expr %= expr + neg_lgc + expr
elem_expr %= expr + at + expr
elem_expr %= expr + db_at + expr
elem_expr %= expr + plus + expr
elem_expr %= expr + minus + expr
elem_expr %= expr + star + expr
elem_expr %= expr + div + expr
elem_expr %= expr + mod + expr
elem_expr %= minus + expr
