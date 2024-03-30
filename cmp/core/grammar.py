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
extend_definer = G.NonTerminal('<extend-definer>')
virtual_method_list = G.NonTerminal('<virtual-method-list>')
virtual_method = G.NonTerminal('<virtual-method>')
fully_typed_params = G.NonTerminal('<fully-typed-params>')
fully_typed_param = G.NonTerminal('<fully-typed-param>')
vector = G.NonTerminal('<vector>')
vector_decl = G.NonTerminal('<vector-decl>')
generation_pattern = G.NonTerminal('<generation-pattern>')
function_declaration_id = G.NonTerminal('<func-decl-id>')
inherits_type = G.NonTerminal('<inherits-type>')

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
elif_ = G.Terminal('elif')
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
program %= program_level_decl_list, lambda h,s: ProgramNode(s[1])
# program %= G.Epsilon

program_level_decl_list%= instr_wrapper, lambda h,s: [s[1]]
program_level_decl_list %= program_level_decl + program_level_decl_list, lambda h,s: [s[1]] + s[2]
program_level_decl_list %= G.Epsilon, lambda h,s: []

program_level_decl %= type_declaration, lambda h,s: s[1]
program_level_decl %= function_declaration, lambda h,s: s[1]
program_level_decl %= protocol_declaration, lambda h,s: s[1]

#intruction list
#<instr-list> -> <instr>; | <instr>; <instr-list>
instr_list %= instr + semicolon, lambda h,s: [s[1]]
instr_list %= instr + semicolon + instr_list, lambda h,s: [s[1]] + s[3]

instr_wrapper %= instr, lambda h,s: s[1]
instr_wrapper %= instr + semicolon, lambda h,s: s[1]
#instruction
#<instr> -> <var-dec> | <func-call> | <func-dec> | <type-dec> | <scope> | <flux-control> | <var-asign> | <expression>

# instr %= function_declaration
# instr %= type_declaration
instr %= scope, lambda h,s: s[1]
instr %= flux_control, lambda h,s: s[1]
# instr %= var_asignation
instr %= expression, lambda h,s: s[1]
instr %= var_dec, lambda h,s: s[1]

#var declaration <var-dec> -> let <var-init-list> in <var-decl-expression> 
var_dec %= let + var_inicialization_list+ in_ + var_decl_expression, lambda h,s: VarsDeclarationsListNode(s[2], s[4])

#var declaration expression <var-decl-expression> -> <scope> | <flux-control> | <var-decl> | <expression> | (<var-dec>)
var_decl_expression %= scope, lambda h,s: s[1]
var_decl_expression %= flux_control, lambda h,s: s[1]
var_decl_expression %= expression, lambda h,s: s[1]
var_decl_expression %= open_curly_braket + var_dec + closed_curly_braket, lambda h,s: ParenthesisExpr(s[2])
var_decl_expression %= var_dec, lambda h,s: s[1]

#var-inicialization-list <var-init-list> -> <var-init> | <var-init> , <var-init-list>
var_inicialization_list %= var_initialization, lambda h,s: [s[1]]
var_inicialization_list %= var_initialization + comma + var_inicialization_list, lambda h,s: [s[1]] + s[3]

#var initialization <var-init> -> ID = <expression> | ID = <var-asign>
var_initialization %= identifier + inicialization + expression, lambda h,s: lambda h,s: VarDeclarationNode(s[1], s[3])
# var_initialization %= identifier + inicialization  + var_asignation 

# #id list <id-list> -> <identifier> | <identifier>, <id-list>
id_list %= identifier, lambda h,s: [s[1]]
id_list %= identifier + comma + id_list, lambda h,s: [s[1]] + s[3]

#identifier <identifier> -> ID | ID <type-anotation>
identifier %= ID, lambda h,s: s[1]
identifier %= fully_typed_param, lambda h,s: s[1]

#fullt typed param 
fully_typed_param %= ID + type_anotation, lambda h,s: s[1] #TODO: this has type

# #type anotation <type-anotation> -> : Number
type_anotation %= type_asignator + ID, lambda h,s: TypeAnotationNode(s[2]) #TODO: this has type

#scopes <scope> -> { <inst-list> }
scope%=open_bracket+instr_list+closed_bracket, lambda h,s: BlockNode(s[2])

#expressions <expresion> -> <aritmetic-op> | <type-instanciation> | <string-operation>
expression %= aritmetic_operation, lambda h,s: s[1]
# expression %= type_instanciation
expression %= atom + string_operator + expression, lambda h,s: StringSimpleConcatNode(s[1], s[3])
expression %= atom + string_operator_space + expression, lambda h,s: StringSpaceConcatNode(s[1], s[3])
expression %= var_asignation, lambda h,s: s[1]
#expression %= string_operation

#artimetic expresssion <aritmetic-expresion> -> <factor> + <aritmetic-expression> | <factor> - <aritmetic-expression> | <factor>

aritmetic_operation %= term +plus_operator+ aritmetic_operation, lambda h,s: PlusNode(s[1], s[3])
aritmetic_operation %= term + minus_operator + aritmetic_operation, lambda h,s: MinusNode(s[1], s[3])
aritmetic_operation %= term, lambda h,s: s[1]

#factor <factor> -> <atom> * <factor> | <atom> / <factor> | <atom>
term %= factor + multiplication + term, lambda h,s: StarNode(s[1], s[3])
term %= factor + division + term, lambda h,s: DivNode(s[1], s[3])
term %= factor, lambda h,s: s[1]

factor %= factor + exponentiation + base_exponent, lambda h,s: PowNode(s[1], s[3])
factor %= base_exponent, lambda h,s: s[1]

base_exponent %= atom, lambda h,s: s[1]
base_exponent %= open_curly_braket + aritmetic_operation + closed_curly_braket, lambda h,s: ParenthesisExpr(s[2])

#base exponent <base exponent>

#atom <atom> -> (<expression>) | number | <function-call> | id
atom %= number, lambda h,s: NumberNode(s[1])
atom %= function_call, lambda h,s: s[1]
atom %= var_use, lambda h,s: s[1]
atom %= vector, lambda h,s: s[1]
atom %= variable_method, lambda h,s: s[1]
atom %= string_, lambda h,s: StringNode(s[1])
atom %= type_instanciation, lambda h,s: s[1]
atom %= boolean_value, lambda h,s: s[1]

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
var_asignation %= var_use + asignation + expression, lambda h,s: VarAssignation(s[1], s[3])
# var_asignation %= var_use + asignation + var_asignation

#function declaration <function-declaration> -> <func-inline-declaration> | <func-full-dec>

function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])
function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_full_declaration + semicolon, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])

function_declaration %= function_declaration_id+open_curly_braket +id_list+ closed_curly_braket + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[5])
function_declaration %= function_declaration_id+open_curly_braket + closed_curly_braket + function_inline_declaration, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[4])

function_declaration_id %= function + ID, lambda h,s: s[2]

#function full declaration <function-full-declaration> -> function ID(<id-list>)<scope> | function ID()<scope>
function_full_declaration %= scope, lambda h,s: s[1]
function_full_declaration %= type_anotation + scope, lambda h,s: s[2] # TODO: this has type
#function inline declaration <function-inline-declaration> -> function ID (<id-list> ) => <expression> | function ID () => <expression>
function_inline_declaration %= func_arrow + expression +semicolon, lambda h,s: s[2]
function_inline_declaration %= type_anotation + func_arrow + expression + semicolon, lambda h,s: s[3] # TODO: this has type

#conditional  <conditional> -> <inline-conditional> | <full-conditional>
conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + expression + else_statement, lambda h,s: IfNode(s[3], s[5], s[6][0], s[6][1])
conditional %= if_ + open_curly_braket + conditional_expression + closed_curly_braket + scope + else_statement, lambda h,s: IfNode(s[3], s[5], s[6][0], s[6][1])

#inline conditional <inline-conditional> -> if (<conditional-expression>) expression <else-staement>


#full conditional <full-conditional> -> if (<conditional>) { <instruction> } <else-statement>

#else statement <else-statement> -> <inline-else> | <full-else>
else_statement %= elif_ + expression + else_statement, lambda h,s: [s[2]] + s[3]
else_statement %= elif_ + scope + else_statement, lambda h,s: [s[2]] + s[3]
else_statement %= else_ + inline_else, lambda h,s: s[2]
else_statement %= else_ + full_else, lambda h,s: s[2]

inline_else %= expression, lambda h,s: s[1]
full_else %= scope, lambda h,s: s[1]

#while instruction <while-loop> -> while (<condition-expression>) <scope>
while_loop %= while_ + open_curly_braket + conditional_expression + closed_curly_braket + scope, lambda h,s: WhileLoopNode(s[3], s[5])

#for instruction <for-loop> -> for ( Id in <iterable-expression>) <scope> 
for_loop %= for_ + open_curly_braket + identifier + in_ + expression + closed_curly_braket + scope, lambda h,s: ForLoopNode(s[3], s[5], s[7])

#conditional expression <conditional-expression> -> <condition> & <conditiona-expression> | <condition> '|' <conditiona-expression> | !<condition> | <condition>
conditional_expression %= condition + and_ + conditional_expression, lambda h,s: AndNode(s[1], s[3])
conditional_expression %= condition + or_ + conditional_expression, lambda h,s: OrNode(s[1], s[3])
conditional_expression %= not_ + condition, lambda h,s: NotNode(s[2])
conditional_expression %= condition, lambda h,s: s[1]

#condition <condition> -> <boolean-value> | <comparation> | (<conditional_expression>) 
# condition %= boolean_value
condition %= comparation, lambda h,s: s[1]
condition %= open_curly_braket + conditional_expression + closed_curly_braket, lambda h,s: ParenthesisExpr(s[2])
#comparation <comparation> -> <expression> '>' <expression> | <expression> '<' <expression> | <expression> =< <expression> | <expression> >= <expression> | 
#<expression> == <expression> | <expression> != <expression>
comparation %= expression + gt + expression, lambda h,s: GreaterThatNode(s[1], s[3])
comparation %= expression + lt + expression, lambda h,s: LessThatNode(s[1], s[3])
comparation %= expression + gte + expression, lambda h,s: GreaterOrEqualThatNode(s[1], s[3])
comparation %= expression + lte + expression, lambda h,s: LessOrEqualThatNode(s[1], s[3])
comparation %= expression + eq + expression, lambda h,s: EqualNode(s[1], s[3])
# comparation %= expression + neq + expression 

#boolean value <boolean-value> -> true | false
boolean_value %= true, lambda h,s: BooleanNode(s[1])
boolean_value %= false, lambda h,s: BooleanNode(s[1])

#type declaration <type-declaration> -> <type-declaration> -> type + <constructor> + <decl-body> | type<constructor>inherits <constructor><decl-body>
type_declaration %= type + ID + constructor + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[4])

type_declaration %= type + ID + constructor + inherits_type + decl_body, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])
type_declaration %= type + ID + constructor + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], [])
type_declaration %= type + ID + constructor + inherits_type + decl_body + semicolon, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5], s[4])

#constructor <constructor> -> ID | ID()
constructor %= open_curly_braket + param_list + closed_curly_braket, lambda h,s: s[2]
constructor %= open_curly_braket + closed_curly_braket, lambda h,s: []
constructor %= G.Epsilon, lambda h,s: []

inherits_type %= inherits + ID + constructor, lambda h,s: TypeInheritNode(s[2], s[3])

#declaration body <decl-body> -> {<decl-list>} | {}
decl_body %= open_bracket+closed_bracket, lambda h,s: []
decl_body %= open_bracket+ decl_list + closed_bracket, lambda h,s: s[2]

#declaration statement list <decl-list> -> <declaration>; | <declaration>;<decl-list> 
decl_list %= declaration + semicolon, lambda h,s: [s[1]]
decl_list %= declaration + semicolon+decl_list, lambda h,s: [s[1]] + s[3]

#declaration <declaration> -> <atribute-declaration> | <method-declaration>
declaration %= atribute_declaration, lambda h,s: s[1]
declaration %= method_declaration, lambda h,s: s[1]

#atribute declaration <atribute-declaration> -> ID = <expression>
atribute_declaration %= identifier + inicialization + expression, lambda h,s: AttrDeclarationNode(s[1], None, s[3])

#method declaration <method-declaration>-> ID (<params>) => <expression> | ID (<params>) => { <inst-list> } 
method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + func_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[1], s[3], s[6])
method_declaration %= ID + open_curly_braket + id_list + closed_curly_braket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], s[3], s[5])

method_declaration %= ID + open_curly_braket + closed_curly_braket + func_arrow + expression, lambda h,s: FuncInlineDeclarationNode(s[1], [], s[5])
method_declaration %= ID + open_curly_braket + closed_curly_braket + function_full_declaration, lambda h,s: FuncFullDeclarationNode(s[1], [], s[4])



#function call <func-call> -> ID(<param-list>) | ID()
function_call %= ID + open_curly_braket + param_list + closed_curly_braket, lambda h,s: CallNode(s[1], s[3])
function_call %= ID + open_curly_braket + closed_curly_braket, lambda h,s: CallNode(s[1], [])

#type instanciation <type-instanciation -> new ID (<param-list>) | new ID()
type_instanciation %= new + ID + open_curly_braket + param_list + closed_curly_braket, lambda h,s: InstantiateTypeNode(s[2], s[4])
type_instanciation %= new + ID + open_curly_braket + closed_curly_braket, lambda h,s: InstantiateTypeNode(s[2], [])

#param list <param-list> -> <expression> | <expression> , <param-list>
param_list %= param, lambda h,s: [s[1]]
param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]

param %= expression, lambda h,s: s[1]
# param%=string_operation

#var use <var-use> -> Id | <variable-atribute>
var_use %= ID, lambda h,s: VariableNode(s[1])
var_use %= atom+open_square_braket+atom+close_square_braket, lambda h,s: VecInstNode(s[1], s[3])
var_use %= variable_atribute, lambda h,s: s[1]
#variable atribute use <var-atrr>-> ID.ID
variable_atribute %= ID + dot + ID, lambda h,s: CallTypeAttr(s[1], s[3])


#variable method use <var-method> -> ID.ID(param_list) | ID.ID()
variable_method %= ID + dot + function_call, lambda h,s: CallTypeFunc(s[1], s[3])

#flux controllers <flux-control> -> <while> | if | for

flux_control %= while_loop, lambda h,s: s[1]
flux_control %= conditional, lambda h,s: s[1]
flux_control %= for_loop, lambda h,s: s[1]

#protocol declaration <protocol-declaration> -> protocol <protocol-definer> <protocol-body>

protocol_declaration %= protocol + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[3])
protocol_declaration %= protocol + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[3])
protocol_declaration %= protocol + ID + extends + ID + protocol_body, lambda h,s: ProtocolNode(s[2], s[5], s[4])
protocol_declaration %= protocol + ID + extends + ID + protocol_body + semicolon, lambda h,s: ProtocolNode(s[2], s[5], s[4])

# # #extend definer <extend-definer> -> extends ID | epsilon

# extend_definer %= extends + ID + extend_definer
# extend_definer %= G.Epsilon, lambda h,s: []

#protocol body (type decl body with full typing) <protocol-body> -> {<virtual-method-list>}
protocol_body %= open_bracket+virtual_method_list+closed_bracket, lambda h,s: s[2]

#virtual method list <virtual-method-list> -> <virtual-method>;|<virtual-method>;<virtual-method-list>
virtual_method_list %= virtual_method + semicolon, lambda h,s: s[1]
virtual_method_list %= virtual_method + semicolon + virtual_method_list, lambda h,s: [s[1]] + s[3]

#virtual method <virtual-method> -> ID():ID | ID(param_list_typed):ID
virtual_method %= ID + open_curly_braket+closed_curly_braket + type_anotation, lambda h,s: ProtocolMethod(s[1], s[4], [])
virtual_method %= ID + open_curly_braket+fully_typed_params+closed_curly_braket + type_anotation, lambda h,s: ProtocolMethod(s[1], s[5], s[3])

#param_list_typed <param-list-typed> -> <typed-param> | <typed-param> , <param-list-typed>
fully_typed_params %= fully_typed_param, lambda h,s: s[1]
fully_typed_params %= fully_typed_param + comma + fully_typed_params, lambda h,s: [s[1]] + s[3]

#vectors
vector %= open_square_braket + vector_decl + close_square_braket, lambda h,s: VecDecExplSyntaxNode(s[2])

#vector declaration
vector_decl %= param_list, lambda h,s: s[1]
vector_decl %= expression + gen_pattern_symbol + identifier + in_ + expression, lambda h,s: VecDecImplSyntaxNode(s[1], s[3], s[5])









