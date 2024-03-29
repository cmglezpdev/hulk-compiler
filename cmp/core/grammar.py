from cmp.pycompiler import Grammar
from cmp.tools.ast import *

G = Grammar()
program = G.NonTerminal('<program>', True)

#non terminals
instr_list = G.NonTerminal('<inst-list>')
instr = G.NonTerminal('<inst>')
var_dec = G.NonTerminal('<var-dec>')
expression = G.NonTerminal('<expression>')
flux_control = G.NonTerminal('<flux-control>')
scope = G.NonTerminal('<scope>')
function_declaration = G.NonTerminal('<function-declaration>')
function_call = G.NonTerminal('<function-call>')
type_declaration = G.NonTerminal('<type-declaration>')
id_list = G.NonTerminal('<id-list>')
type_instanciation = G.NonTerminal('<type-instanciation>')
var_asignation = G.NonTerminal('<var-asign>')
aritmetic_operation = G.NonTerminal('<aritmetic-operation>')
factor = G.NonTerminal('<factor>')
atom = G.NonTerminal('<atom>')
var_initialization = G.NonTerminal('<var-init>')
var_inicialization_list = G.NonTerminal('<vat-init-list>')
string_operation =G.NonTerminal('<string-operation>')
string_atom = G.NonTerminal('<string-atom>')
function_full_declaration = G.NonTerminal('<function-full-declaration>')
function_inline_declaration = G.NonTerminal('<function-inline-declaration>')
var_decl_expression = G.NonTerminal('<var-decl-expr>')
conditional = G.NonTerminal('<conditional>')
inline_conditional = G.NonTerminal('<inline-conditional>')
full_conditional = G.NonTerminal('<full-conditional>')
else_statement = G.NonTerminal('<else-statement>')
inline_else = G.NonTerminal('<inline-else>')
full_else = G.NonTerminal('<full-else>')
loop = G.NonTerminal('<loop>')
while_loop = G.NonTerminal('<while-loop>')
for_loop = G.NonTerminal('<for-loop>')
iterable_expression = G.NonTerminal('<iterable-expression>')
conditional_expression = G.NonTerminal('<conditional-expresssion>')
condition = G.NonTerminal('<condition>')
boolean_value = G.NonTerminal('<boolean-value>') 
comparation = G.NonTerminal('<comparation>')
decl_body = G.NonTerminal('<decl-body>')
decl_list = G.NonTerminal('<decl-list>')
declaration = G.NonTerminal('<decl>')
atribute_declaration = G.NonTerminal('<atribute-declaration>')
method_declaration = G.NonTerminal('<method-declaration>')
function_call = G.NonTerminal('<function-call>')
param_list = G.NonTerminal('<param-list>')
variable_atribute = G.NonTerminal('<var-attr>')
variable_method = G.NonTerminal('<var-method>')
identifier = G.NonTerminal('<identifier>')
type_anotation = G.NonTerminal('<type-anotation>')

#terminals
semicolon = G.Terminal(';')
while_ = G.Terminal('while')
for_ = G.Terminal('for')
open_bracket = G.Terminal('{')
closed_bracket = G.Terminal('}')
let = G.Terminal('let')
ID = G.Terminal('ID')
asignation = G.Terminal(':=')
inicialization = G.Terminal('=')
in_ = G.Terminal('in')
comma = G.Terminal(',')
number = G.Terminal('number')
open_curly_braket = G.Terminal('(')
closed_curly_braket = G.Terminal(')')
plus_operator = G.Terminal('+')
minus_operator = G.Terminal('-')
multiplication = G.Terminal('*')
division = G.Terminal('/')
module_operation = G.Terminal('%')
string = G.Terminal('string')
string_operator = G.Terminal('@')
string_operator_space = G.Terminal('@@')
function = G.Terminal('function')
func_arrow = G.Terminal('=>')
if_ = G.Terminal('if')
else_ = G.Terminal('else')
and_ = G.Terminal('&')
or_ = G.Terminal('|')
not_ = G.Terminal('!')

true = G.Terminal('true')
false = G.Terminal('false')

gt = G.Terminal('>')
lt = G.Terminal('<')
gte = G.Terminal('>=')
lte = G.Terminal('=<')
eq = G.Terminal('==')
neq = G.Terminal('!=')

new = G.Terminal('new')
type = G.Terminal('type')
dot = G.Terminal('.')

number_type = G.Terminal('Number')
type_asignator = G.Terminal(':')
#productions

#entry point
#<program> -> <instr-list>
program %= instr_list, lambda h,s: ProgramNode(s[1])
#program %= number

#intruction list
#<instr-list> -> <instr>; | <instr>; <instr-list>
instr_list %=  instr + semicolon, lambda h,s: [s[1]]
instr_list %= instr + semicolon + instr_list, lambda h,s: [s[1]] + s[3]
# instr_list %= instr + instr_list
# instr_list %= instr

#instruction
#<instr> -> <var-dec> | <func-call> | <func-dec> | <type-dec> | <scope> | <flux-control> | <var-asign> | <expression>

# instr %= function_declaration
# instr %= type_declaration
instr %= var_dec, lambda h,s: s[1]
instr %= scope, lambda h,s: s[1]
instr %= flux_control, lambda h,s: s[1]
instr %= var_asignation, lambda h,s: s[1]
instr %= expression, lambda h,s: s[1]

# #var declaration <var-dec> -> let <var-init-list> in <var-decl-expression> 
var_dec %= let + var_inicialization_list + in_ + var_decl_expression, lambda h,s: VarsDeclarationsListNode(s[2], s[4])

#var declaration expression <var-decl-expression> -> <scope> | <flux-control> | <var-decl> | <expression> | (<var-dec>)
var_decl_expression %= scope, lambda h,s: s[1]
var_decl_expression %= flux_control, lambda h,s: s[1]
var_decl_expression %= expression, lambda h,s: s[1]
var_decl_expression %= var_dec, lambda h,s: s[1]
# var_decl_expression %= open_curly_braket + var_dec + closed_curly_braket

# #var-inicialization-list <var-init-list> -> <var-init> | <var-init> , <var-init-list>
var_inicialization_list %= var_initialization, lambda h,s: [s[1]]
var_inicialization_list %= var_initialization + comma + var_inicialization_list, lambda h,s: [s[1]] + s[3]

#var initialization <var-init> -> ID = <expression> | ID = <var-asign>
var_initialization %= identifier + inicialization + expression, lambda h,s: VarDeclarationNode(s[1], s[3])
var_initialization %= identifier + inicialization + var_asignation, lambda h,s: VarDeclarationNode(s[1], s[3]) 
#TODO desambiguar let a = b=c = 4 y let a = c := 4

# #id list <id-list> -> <identifier> | <identifier>, <id-list>
# id_list %= identifier
# id_list %= identifier + comma + id_list

# #identifier <identifier> -> ID | ID <type-anotation>
identifier %= ID, lambda h,s: s[1]
# identifier %= ID + type_anotation

# #type anotation <type-anotation> -> : Number
# type_anotation %= type_asignator + number_type

# #scopes <scope> -> { <inst-list> } | {}
scope%=open_bracket+instr_list+closed_bracket, lambda h,s: BlockNode(s[2])
scope%=open_bracket+closed_bracket, lambda h,s: BlockNode([])

#expressions <expresion> -> <aritmetic-op> | <type-instanciation> | <string-operation>
expression %= aritmetic_operation, lambda h,s: s[1]
# expression %= type_instanciation
# expression %= string_operation

#artimetic expresssion <aritmetic-expresion> -> <factor> + <aritmetic-expression> | <factor> - <aritmetic-expression> | <factor>

aritmetic_operation %= aritmetic_operation + plus_operator + factor, lambda h,s: PlusNode(s[1], s[3])
aritmetic_operation %= aritmetic_operation + minus_operator + factor, lambda h,s: MinusNode(s[1], s[3])
aritmetic_operation %= factor, lambda h,s: s[1]

#factor <factor> -> <atom> * <factor> | <atom> / <factor> | <atom>

factor %= atom + multiplication + factor, lambda h,s: StarNode(s[1], s[3])
factor %= atom + division + factor, lambda h,s: DivNode(s[1], s[3])
factor %= atom, lambda h,s: s[1]

# #atom <atom> -> (<expression>) | number | <function-call> | id
atom %= open_curly_braket + aritmetic_operation + closed_curly_braket, lambda h,s: s[2]
atom %= number, lambda h,s: ConstantNode(s[1])
atom %= function_call, lambda h,s: s[1]
atom %= ID, lambda h,s: VariableNode(s[1])
# atom %= variable_atribute
# atom %= variable_method

# #string operation <string-operation> -> <string-atom> @ <string-operation> | <string-atom>
# string_operation %= string_atom
# # string_operation %= string_atom + string_operator + string_operation
# string_operation %= string_atom + string_operator_space + string_operation

# #string atom <string-atom> -> string | <function-call> | ID
# string_atom %= string
# # string_atom %= function_call
# # string_atom %= ID
# # string_atom %= variable_atribute
# # # string_atom %= variable_method
# # string_atom %= open_curly_braket + string_operation + closed_curly_braket

#variable asignation <var-asignation> -> let id
var_asignation %= ID + asignation + expression, lambda h,s: VarAssignation(s[1], s[3])

# #function declaration <function-declaration> -> <func-inline-declaration> | <func-full-dec>
# function_declaration %= function_inline_declaration, lambda h,s: s[1]
# function_declaration %= function_full_declaration, lambda h,s: s[1]

#function full declaration <function-full-declaration> -> function ID(<id-list>)<scope> | function ID()<scope>
function_full_declaration %= function + ID + open_curly_braket + id_list + closed_curly_braket + scope, lambda h,s: FuncFullDeclarationNode(s[2], s[4], s[6])
function_full_declaration %= function + ID + open_curly_braket + closed_curly_braket + scope, lambda h,s: FuncFullDeclarationNode(s[2], [], s[5])
#function inline declaration <function-inline-declaration> -> function ID (<id-list> ) => <expression> | function ID () => <expression>
function_inline_declaration %= function + ID + open_curly_braket + id_list + closed_curly_braket + func_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[2], s[4], s[7])
function_inline_declaration %= function + ID + open_curly_braket + closed_curly_braket + func_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[2], [], s[6])

# #conditional  <conditional> -> <inline-conditional> | <full-conditional>
# conditional %= inline_conditional
# conditional %= full_conditional

# #inline conditional <inline-conditional> -> if (<conditional-expression>) expression <else-staement> | if (<conditional-expression>) expression
# inline_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + expression + else_statement
# inline_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + expression

# #full conditional <full-conditional> -> if (<conditional>) { <instruction> } <else-statement> | if (<conditional>) { <instruction> } 
# full_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + open_bracket + instr_list + closed_bracket
# full_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + open_bracket + instr_list + closed_bracket + else_statement

# #else statement <else-statement> -> <inline-else> | <full-else>
# else_statement %= else_ + inline_else
# else_statement %= else_ + full_else

# #while instruction <while-loop> -> while (<condition-expression>) <scope>
# while_loop %= while_ + open_curly_braket + conditional_expression + closed_curly_braket + scope

# #for instruction <for-loop> -> for ( Id in <iterable-expression>) <scope> 
# for_loop %= for_ + open_curly_braket + ID + iterable_expression + closed_curly_braket + scope

# #conditional expression <conditional-expression> -> <condition> & <conditiona-expression> | <condition> '|' <conditiona-expression> | !<condition> | <condition>
# conditional_expression %= condition + and_ + conditional_expression
# conditional_expression %= condition + or_ + conditional_expression
# conditional_expression %= not_ + condition
# conditional_expression %= condition

# #condition <condition> -> <boolean-value> | <comparation> | (<conditional_expression>) 
# condition %= boolean_value
# condition %= comparation
# condition %= open_curly_braket + conditional_expression + closed_curly_braket 
# #comparation <comparation> -> <expression> '>' <expression> | <expression> '<' <expression> | <expression> =< <expression> | <expression> >= <expression> | 
# #<expression> == <expression> | <expression> != <expression>
# comparation %= expression + gt + expression
# comparation %= expression + lt + expression
# comparation %= expression + gte + expression
# comparation %= expression + lte + expression
# comparation %= expression + eq + expression
# comparation %= expression + neq + expression

#boolean value <boolean-value> -> true | false
boolean_value %= true, lambda h,s: BooleanNode(s[1])
boolean_value %= false, lambda h,s: BooleanNode(s[1])

# #type declaration <type-declaration> -> type ID <decl-body> | type ID () <decl-body> | type ID (<id-list>) <declaration-body>
# type_declaration %= type + ID + decl_body
# type_declaration %= type + ID +open_curly_braket+closed_curly_braket+ decl_body
# type_declaration %= type + ID +open_curly_braket+id_list+closed_curly_braket+ decl_body

# #declaration body <decl-body> -> {<decl-list>} | {}
# decl_body %= open_bracket+closed_bracket
# decl_body %= open_bracket+ decl_list + closed_bracket

# #declaration statement list <decl-list> -> <declaration>; | <declaration>;<decl-list> 
# decl_list %= declaration + semicolon
# decl_list %= declaration + semicolon+decl_list

# #declaration <declaration> -> <atribute-declaration> | <method-declaration>
# declaration %= atribute_declaration
# declaration %= method_declaration

# #atribute declaration <atribute-declaration> -> ID = <expression>
# atribute_declaration %= ID + expression

# #method declaration <method-declaration>-> ID (<params>) => <expression> | ID (<params>) => { <inst-list> } 
# method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + func_arrow + expression 
# method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + open_bracket + instr_list +closed_bracket

#function call <func-call> -> ID(<param-list>) | ID()
function_call %= ID + open_curly_braket + param_list + closed_curly_braket, lambda h,s: CallNode(s[1], s[3])
function_call %= ID + open_curly_braket + closed_curly_braket, lambda h,s: CallNode(s[1], [])

# #type instanciation <type-instanciation -> new ID (<param-list>) | new ID()
# type_instanciation %= new + ID + open_curly_braket + param_list + closed_curly_braket
# type_instanciation %= new + ID + open_curly_braket + closed_curly_braket

#param list <param-list> -> <expression> | <expression> , <param-list>
param_list %= expression, lambda h,s: s[1]
param_list %= expression + comma + param_list, lambda h,s: [s[1]] + s[3]

#variable atribute use <var-atrr>-> ID.ID
# variable_atribute %= ID + dot + ID

#variable method use <var-method> -> ID.ID(param_list) | ID.ID()
# variable_method %= ID + dot + ID + open_curly_braket + param_list+ closed_curly_braket
# variable_method %= ID + dot + ID + open_curly_braket + closed_curly_braket

#flux controllers <flux-control> -> <while> | if | for

# flux_control %= while_loop, lambda h,s: s[1]
# flux_control %= conditional, lambda h,s: s[1]
# flux_control %= for_loop, lambda h,s: s[1]










