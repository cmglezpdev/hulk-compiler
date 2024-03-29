from cmp.tools.regex import EPSILON
from cmp.utils import Token
from .lexer import Lexer
from cmp.core.grammar import *
import string
from cmp.core.grammar import G, plus_operator, minus_operator, multiplication, division, open_curly_braket, closed_curly_braket, number

digits = '|'.join(str(i) for i in range(0, 10))
nonzerodigits = '|'.join(str(i) for i  in range(1, 10))
lowers = '|'.join(chr(i) for i in range(ord('a'), ord('z') + 1))
uppers = '|'.join(chr(i) for i in range(ord('A'), ord('Z') + 1))
# SYMBOLS = [
#     '&', '!', r'\|', # logics 
#     '+', '-', r'\*', '/', '%', # arithmetics 
#     '<', '>', '>=', '<=', '==', '!=', # comparations
#     '@', r'\(', r'\)', '{', '}', '=', '.', ':', ';', ',', '?', # others 
# ]
SYMBOLS = {
    '+': plus_operator,
    '-': minus_operator,
    r'\*': multiplication,
    '/': division,
    r'\(': open_curly_braket,
    r'\)': closed_curly_braket
    
}

symbols = '|'.join([digits, lowers, uppers,
    '|'.join(SYMBOLS)                   
])
def mapping(string):
    if string == '|':
        return r'\|'
    if string == '*':
        return r'\*'
    if string == '(':
        return r'\('
    if string == ')':
        return r'\)'           
    else:
        return string
printables = '|'.join([printable for printable in list(map(mapping,string.printable))])
STRINGS_VALUES = f'(\")({printables})*(\")'
INTEGER = f'({digits})(.|{EPSILON})({digits})*'
SPACE = '(\n|\t|\f|\r|\v| )(\n|\t|\f|\r|\v| )*'
KEYWORDS = [
    'type', 'inherit', 
    'if','else', 
    'function', 'while', 'for', 
    'let', 'in','is','new','Number'
]

TYPE_ANOTATIONS =":( )*Number"

TRUE = 'true'
FALSE = 'false'
identifier = f'({uppers}|{lowers}|_)({uppers}|{lowers}|{digits}|_)*'


# COMMENT = f'[--[{symbol}|\\|"|\t]^\n]|[(*[{symbol}|\\|"|{SPACE}]^*)]'  # TODO: Check nested comments


def build_lexer():
    
    table = []

    table.append(('space',SPACE))

    table.append((multiplication,r'\*'))
    table.append((plus_operator,'+'))
    table.append((open_curly_braket,r'\('))
    table.append((closed_curly_braket,r'\)'))
    table.append((semicolon,';'))
    table.append((minus_operator,'-'))
    table.append((division,'/'))
    table.append((open_bracket,'{'))
    table.append((closed_bracket,'}'))
    table.append((and_,'&'))
    table.append((or_,r'\|'))
    table.append((not_,'!'))
    table.append((gt,'>'))
    table.append((lt,'<'))
    table.append((lte,'<='))
    table.append((gte,'>='))
    table.append((eq,'=='))
    table.append((neq,'!='))
    table.append((exponentiation,'^'))
    table.append((open_square_braket,'['))
    table.append((close_square_braket,']'))
    table.append((gen_pattern_symbol,r'\|\|'))
    table.append((string_operator_space,'@@'))
    table.append((string_operator,'@'))
    table.append((asignation,':='))
    table.append((inicialization,'='))
    table.append((comma,','))
    table.append((module_operation,'%'))
    table.append((func_arrow,'=>'))
    table.append((type_asignator,':'))
    table.append((dot,'.'))

    table.append((number, INTEGER))

    table.append((while_,'while'))
    table.append((protocol,'protocol'))
    table.append((extends,'extends'))
    table.append((for_,'for'))
    table.append((let,'let'))
    table.append((in_,'in'))
    table.append((function,'function'))
    table.append((if_,'if'))
    table.append((else_,'else'))
    table.append((true,'true'))
    table.append((false,'false'))
    table.append((new,'new'))
    table.append((type,'type'))
    table.append((inherits,'inherits'))
    table.append((string_,STRINGS_VALUES))
    table.append((ID,identifier))

    print('>>> Building Lexer...')
    return Lexer(table,G.EOF)


def cleaner(tokens: list[Token]):
    i = 0
    while i < len(tokens):
        if tokens[i].token_type == 'space':
            tokens.remove(tokens[i])
        else:
            i += 1

def tokenizer(code: str, lexer: Lexer = None):
    if lexer is None:
        lexer = build_lexer()
    
    print('>>> Tokenizing..')
    try:
        tokens = lexer(code)
    except Exception as e:
        print(e)
    else:
        print('>>> Cleaning tokens...')
        cleaner(tokens)
        
        print('>>> Done !')
        return tokens



