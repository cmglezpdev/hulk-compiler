from cmp.pycompiler import Grammar
from cmp.tools.ast import *

G = Grammar()
program = G.NonTerminal('<program>', True)

#non terminals
instr_list = G.NonTerminal('<inst-list>')
param = G.NonTerminal('<param>')
program_level_decl_list = G.NonTerminal('<program-decl-list>')
program_level_decl = G.NonTerminal('<program-level-decl>')
instr_wrapper = G.NonTerminal('<inst-wrapper>')
instr = G.NonTerminal('<inst>')
var_dec = G.NonTerminal('<var-dec>')
expression = G.NonTerminal('<expression>')
flux_control = G.NonTerminal('<flux-control>')
base_exponent = G.NonTerminal('<base-exponent>')
scope = G.NonTerminal('<scope>')
function_declaration = G.NonTerminal('<function-declaration>')
function_call = G.NonTerminal('<function-call>')
type_declaration = G.NonTerminal('<type-declaration>')
id_list = G.NonTerminal('<id-list>')
type_instanciation = G.NonTerminal('<type-instanciation>')
var_asignation = G.NonTerminal('<var-asign>')
aritmetic_operation = G.NonTerminal('<aritmetic-operation>')
factor = G.NonTerminal('<factor>')
term = G.NonTerminal('<term>')
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
constructor = G.NonTerminal('<constructor>')
atribute_declaration = G.NonTerminal('<atribute-declaration>')
method_declaration = G.NonTerminal('<method-declaration>')
function_call = G.NonTerminal('<function-call>')
param_list = G.NonTerminal('<param-list>')
variable_atribute = G.NonTerminal('<var-attr>')
variable_method = G.NonTerminal('<var-method>')
identifier = G.NonTerminal('<identifier>')
type_anotation = G.NonTerminal('<type-anotation>')
protocol_declaration =G.NonTerminal('<protocol-declaration>')
var_use = G.NonTerminal('<var-use>')
protocol_body = G.NonTerminal('<protocol-body>')
protocol_definer = G.NonTerminal('<protocol-definer>')
virtual_method_list = G.NonTerminal('<virtual-method-list>')
virtual_method = G.NonTerminal('<virtual-method>')
fully_typed_params = G.NonTerminal('<fully-typed-params>')
fully_typed_param = G.NonTerminal('<fully-typed-param>')
vector = G.NonTerminal('<vector>')
vector_decl = G.NonTerminal('<vector-decl>')
generation_pattern = G.NonTerminal('<generation-pattern>')
function_declaration_id = G.NonTerminal('<func-decl-id>')

#terminals
semicolon = G.Terminal(';')
gen_pattern_symbol = G.Terminal('||')
while_ = G.Terminal('while')
for_ = G.Terminal('for')
open_bracket = G.Terminal('{')
closed_bracket = G.Terminal('}')
let = G.Terminal('let')
ID = G.Terminal('ID')
asignation = G.Terminal(':=')
inicialization = G.Terminal('=')
in_ = G.Terminal('in')
inherits = G.Terminal('inherits')
comma = G.Terminal(',')
number = G.Terminal('number')
open_curly_braket = G.Terminal('(')
closed_curly_braket = G.Terminal(')')
plus_operator = G.Terminal('+')
minus_operator = G.Terminal('-')
multiplication = G.Terminal('*')
division = G.Terminal('/')
module_operation = G.Terminal('%')
string_= G.Terminal('string')
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
lte = G.Terminal('<=')
eq = G.Terminal('==')
neq = G.Terminal('!=')

new = G.Terminal('new')
type = G.Terminal('type')
dot = G.Terminal('.')

type_asignator = G.Terminal(':')
exponentiation = G.Terminal('^')

protocol = G.Terminal('protocol')
extends = G.Terminal('extends')

open_square_braket = G.Terminal('[')
close_square_braket = G.Terminal(']')
#productions

#entry point
#<program> -> <instr-list>
# program %= instr_wrapper   
# program %=  instr_wrapper
program %= program_level_decl_list# + instr_wrapper
# program %= G.Epsilon

program_level_decl_list%= instr_wrapper
program_level_decl_list %= program_level_decl + program_level_decl_list
program_level_decl_list %= G.Epsilon

program_level_decl %= type_declaration
program_level_decl %= function_declaration
program_level_decl %= protocol_declaration

#intruction list
#<instr-list> -> <instr>; | <instr>; <instr-list>
instr_list %= instr + semicolon
instr_list %= instr + semicolon + instr_list

instr_wrapper %= instr
instr_wrapper %= instr + semicolon
#instruction
#<instr> -> <var-dec> | <func-call> | <func-dec> | <type-dec> | <scope> | <flux-control> | <var-asign> | <expression>

# instr %= function_declaration
# instr %= type_declaration
instr %= scope
instr %= flux_control
# instr %= var_asignation
instr %= expression
instr %= var_dec

#var declaration <var-dec> -> let <var-init-list> in <var-decl-expression> 
var_dec %= let + var_inicialization_list+ in_ + var_decl_expression

#var declaration expression <var-decl-expression> -> <scope> | <flux-control> | <var-decl> | <expression> | (<var-dec>)
var_decl_expression %= scope
var_decl_expression %= flux_control
var_decl_expression %= expression
var_decl_expression %= open_curly_braket + var_dec + closed_curly_braket
var_decl_expression %= var_dec

#var-inicialization-list <var-init-list> -> <var-init> | <var-init> , <var-init-list>
var_inicialization_list %= var_initialization
var_inicialization_list %= var_initialization + comma + var_inicialization_list

#var initialization <var-init> -> ID = <expression> | ID = <var-asign>
var_initialization %= identifier + inicialization + expression
# var_initialization %= identifier + inicialization  + var_asignation 

# #id list <id-list> -> <identifier> | <identifier>, <id-list>
id_list %= identifier
id_list %= identifier + comma + id_list

#identifier <identifier> -> ID | ID <type-anotation>
identifier %= ID
identifier %= fully_typed_param

#fullt typed param 
fully_typed_param %= ID + type_anotation

# #type anotation <type-anotation> -> : Number
type_anotation %= type_asignator + ID

#scopes <scope> -> { <inst-list> }
scope%=open_bracket+instr_list+closed_bracket

#expressions <expresion> -> <aritmetic-op> | <type-instanciation> | <string-operation>
expression %= aritmetic_operation
# expression %= type_instanciation
expression %= atom + string_operator + expression
expression %= atom + string_operator_space + expression
expression %= var_asignation
#expression %= string_operation

#artimetic expresssion <aritmetic-expresion> -> <factor> + <aritmetic-expression> | <factor> - <aritmetic-expression> | <factor>

aritmetic_operation %= term +plus_operator+ aritmetic_operation
aritmetic_operation %= term + minus_operator + aritmetic_operation
aritmetic_operation %= term

#factor <factor> -> <atom> * <factor> | <atom> / <factor> | <atom>
term %= factor + multiplication + term
term %= factor + division + term
term %= factor

factor %= factor + exponentiation + base_exponent
factor %= base_exponent

base_exponent %= atom
base_exponent %= open_curly_braket + aritmetic_operation + closed_curly_braket

#base exponent <base exponent>

#atom <atom> -> (<expression>) | number | <function-call> | id
atom %= number
atom %= function_call
atom %= var_use
atom %= vector
atom %= variable_method
atom %= string_
atom %= type_instanciation
atom %= boolean_value

#string_operation <string-operation> -> <string-atom> @ <string-operation> | <string-atom>
# string_operation %= string_atom
# string_operation %= string_atom + string_operator + string_operation
# string_operation %= string_atom + string_operator_space + string_operation

# #string_atom <string-atom> -> string_| <function-call> | ID
# string_atom %= string_
# string_atom %= function_call
# string_atom %= ID
# string_atom %= variable_atribute
# string_atom %= variable_method
# string_atom %= open_curly_braket + string_operation + closed_curly_braket

#variable asignation <var-asignation> ->  <var-use> := <expression>
var_asignation %= var_use + asignation + expression
# var_asignation %= var_use + asignation + var_asignation

#function declaration <function-declaration> -> <func-inline-declaration> | <func-full-dec>

function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_full_declaration
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_full_declaration
function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_full_declaration + semicolon
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_full_declaration + semicolon

function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_inline_declaration
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_inline_declaration

function_declaration_id %= function + ID 

#function full declaration <function-full-declaration> -> function ID(<id-list>)<scope> | function ID()<scope>
function_full_declaration %= scope
function_full_declaration %= type_anotation + scope
#function inline declaration <function-inline-declaration> -> function ID (<id-list> ) => <expression> | function ID () => <expression>
function_inline_declaration %= func_arrow + expression +semicolon
function_inline_declaration %= type_anotation+  func_arrow + expression + semicolon

#conditional  <conditional> -> <inline-conditional> | <full-conditional>
conditional %= inline_conditional 
conditional %= full_conditional

#inline conditional <inline-conditional> -> if (<conditional-expression>) expression <else-staement> | if (<conditional-expression>) expression
inline_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + expression + else_statement
inline_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + expression

#full conditional <full-conditional> -> if (<conditional>) { <instruction> } <else-statement> | if (<conditional>) { <instruction> } 
full_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + scope
full_conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + scope+ else_statement

#else statement <else-statement> -> <inline-else> | <full-else>
else_statement %= else_ + inline_else
else_statement %= else_ + full_else

#while instruction <while-loop> -> while (<condition-expression>) <scope>
while_loop %= while_ + open_curly_braket + conditional_expression + closed_curly_braket + scope

#for instruction <for-loop> -> for ( Id in <iterable-expression>) <scope> 
for_loop %= for_ + open_curly_braket + identifier + in_ + expression + closed_curly_braket + scope

#conditional expression <conditional-expression> -> <condition> & <conditiona-expression> | <condition> '|' <conditiona-expression> | !<condition> | <condition>
conditional_expression %= condition + and_ + conditional_expression
conditional_expression %= condition + or_ + conditional_expression
conditional_expression %= not_ + condition
conditional_expression %= condition

#condition <condition> -> <boolean-value> | <comparation> | (<conditional_expression>) 
# condition %= boolean_value
condition %= comparation
condition %= open_curly_braket + conditional_expression + closed_curly_braket 
#comparation <comparation> -> <expression> '>' <expression> | <expression> '<' <expression> | <expression> =< <expression> | <expression> >= <expression> | 
#<expression> == <expression> | <expression> != <expression>
comparation %= expression + gt + expression
comparation %= expression + lt + expression
comparation %= expression + gte + expression
comparation %= expression + lte + expression
comparation %= expression + eq + expression
comparation %= expression + neq + expression

#boolean value <boolean-value> -> true | false
boolean_value %= true
boolean_value %= false

#type declaration <type-declaration> -> <type-declaration> -> type + <constructor> + <decl-body> | type<constructor>inherits <constructor><decl-body>
type_declaration %= type + constructor + decl_body
type_declaration %= type + constructor +inherits+ constructor + decl_body
type_declaration %= type + constructor + decl_body + semicolon
type_declaration %= type + constructor +inherits+ constructor + decl_body + semicolon
#constructor <constructor> -> ID | ID()
constructor %= ID
constructor %= function_call


#declaration body <decl-body> -> {<decl-list>} | {}
decl_body %= open_bracket+closed_bracket
decl_body %= open_bracket+ decl_list + closed_bracket

#declaration statement list <decl-list> -> <declaration>; | <declaration>;<decl-list> 
decl_list %= declaration + semicolon
decl_list %= declaration + semicolon+decl_list

#declaration <declaration> -> <atribute-declaration> | <method-declaration>
declaration %= atribute_declaration
declaration %= method_declaration

#atribute declaration <atribute-declaration> -> ID = <expression>
atribute_declaration %= identifier +inicialization+ expression

#method declaration <method-declaration>-> ID (<params>) => <expression> | ID (<params>) => { <inst-list> } 
method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + func_arrow + expression
method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + function_full_declaration

method_declaration %= ID + open_curly_braket + closed_curly_braket + func_arrow + expression
method_declaration %= ID + open_curly_braket + closed_curly_braket + function_full_declaration



#function call <func-call> -> ID(<param-list>) | ID()
function_call %= ID + open_curly_braket + param_list + closed_curly_braket
function_call %= ID + open_curly_braket + closed_curly_braket

#type instanciation <type-instanciation -> new ID (<param-list>) | new ID()
type_instanciation %= new + ID + open_curly_braket + param_list + closed_curly_braket
type_instanciation %= new + ID + open_curly_braket + closed_curly_braket

#param list <param-list> -> <expression> | <expression> , <param-list>
param_list %= param
param_list %= param + comma + param_list

param%=expression
# param%=string_operation

#var use <var-use> -> Id | <variable-atribute>
var_use %= ID
var_use %= atom+open_square_braket+atom+close_square_braket
var_use %= variable_atribute
#variable atribute use <var-atrr>-> ID.ID
variable_atribute %= ID + dot + ID


#variable method use <var-method> -> ID.ID(param_list) | ID.ID()
variable_method %= ID + dot + function_call

#flux controllers <flux-control> -> <while> | if | for

flux_control %= while_loop
flux_control %= conditional
flux_control %= for_loop

#protocol declaration <protocol-declaration> -> protocol <protocol-definer> <protocol-body>

protocol_declaration  %= protocol + protocol_definer + protocol_body
protocol_declaration  %= protocol + protocol_definer + protocol_body + semicolon

#protocol definer <protocol-definer> -> ID | ID extends

protocol_definer %= ID
protocol_definer %= ID + extends + protocol_definer

#protocol body (type decl body with full typing) <protocol-body> -> {<virtual-method-list>}
protocol_body %= open_bracket+virtual_method_list+closed_bracket

#virtual method list <virtual-method-list> -> <virtual-method>;|<virtual-method>;<virtual-method-list>
virtual_method_list %= virtual_method + semicolon
virtual_method_list %= virtual_method + semicolon + virtual_method_list

#virtual method <virtual-method> -> ID():ID | ID(param_list_typed):ID
virtual_method %= ID + open_curly_braket+closed_curly_braket + type_anotation
virtual_method %= ID + open_curly_braket+fully_typed_params+closed_curly_braket + type_anotation

#param_list_typed <param-list-typed> -> <typed-param> | <typed-param> , <param-list-typed>
fully_typed_params %= fully_typed_param
fully_typed_params %= fully_typed_param + comma + fully_typed_params

#vectors
vector %= open_square_braket + vector_decl + close_square_braket

#vector declaration
vector_decl %= param_list 
vector_decl %= expression + gen_pattern_symbol + identifier + in_ + expression









