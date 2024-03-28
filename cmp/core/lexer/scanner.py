from cmp.tools.regex import EPSILON
from cmp.utils import Token
from .lexer import Lexer
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
printables = '|'.join([printable for printable in string.printable])
STRINGS_VALUES = f'{symbols}*'
INTEGER = f'({digits})*(.|{EPSILON})({digits})*'
SPACE = '(\n|\t|\f|\r|\v| )(\n|\t|\f|\r|\v| )*'
KEYWORDS = [
    'type', 'inherit', 
    'if','else', 
    'function', 'while', 'for', 
    'let', 'in','new','Number'
]

TYPE_ANOTATIONS =":( )*Number"

TRUE = 'true'
FALSE = 'false'
# STRING = f'"[{symbols}|{escaped_symbol}|\\"|\\\n]^"'
ID = f'({uppers}|{lowers}|_)({uppers}|{lowers}|{digits}|_)*'

# COMMENT = f'[--[{symbol}|\\|"|\t]^\n]|[(*[{symbol}|\\|"|{SPACE}]^*)]'  # TODO: Check nested comments

def build_lexer():
    
    table = []
    #table.append(('string',STRINGS_VALUES))
    table.append(('space', SPACE))
    for sb in SYMBOLS.keys():
        table.append((SYMBOLS[sb], sb))
        # table.append((sb.replace("\\",""), sb))
    table.append((number, INTEGER))
    # table.append(('type-anotation', TYPE_ANOTATIONS))
    # for kw in KEYWORDS:
    #     table.append((kw, kw))


    
    # table.append(('string',STRINGS_VALUES))
    # table.append(('true', TRUE))
    # table.append(('false', FALSE))

    # table.append(('ID', ID))

    print('>>> Building Lexer...')
    return Lexer(table, G.EOF)


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



