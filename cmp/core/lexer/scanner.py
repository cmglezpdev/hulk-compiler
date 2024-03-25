from cmp.tools.regex import EPSILON
from cmp.utils import Token
from .lexer import Lexer

digits = '|'.join(str(i) for i in range(0, 10))
nonzerodigits = '|'.join(str(i) for i  in range(1, 10))
lowers = '|'.join(chr(i) for i in range(ord('a'), ord('z') + 1))
uppers = '|'.join(chr(i) for i in range(ord('A'), ord('Z') + 1))
SYMBOLS = [
    '&', '!', '|', # logics 
    '+', '-', '*', '/', '%', # arithmetics 
    '<', '>', '>=', '<=', '==', '!=', # comparations
    '@', '(', ')', '{', '}', '=', '.', ':', ';', ',', '?', # others 
]
symbols = '|'.join([digits, lowers, uppers,
    '|'.join(SYMBOLS)                   
])

INTEGER = f'[{digits}]^[.|{EPSILON}][{digits}]^'
SPACE = '[ |\n|\t|\f|\r|\v][ |\n|\t|\f|\r|\v]^'
KEYWORDS = [
    'class', 'inherit', 
    'if', 'elif', 'else', 
    'function', 'with', 'as', 
    'let', 'in', 
    'while', 'case', 
    'of', 'new'
]

TRUE = 'True'
FALSE = 'False'
# STRING = f'"[{symbols}|{escaped_symbol}|\\"|\\\n]^"'
TYPE_ID = f'[{uppers}][{lowers}|{digits}|_]^'
OBJECT_ID = f'[[{lowers}][{uppers}|{digits}|_]^]|[self]'
# COMMENT = f'[--[{symbol}|\\|"|\t]^\n]|[(*[{symbol}|\\|"|{SPACE}]^*)]'  # TODO: Check nested comments

def build_lexer():
    table = [('number', INTEGER)]
    
    for kw in KEYWORDS:
        table.append((kw, kw))
    
    table.append(('true', TRUE))
    table.append(('false', FALSE))
    
    for sb in SYMBOLS:
        table.append((sb, sb))
    
    table.append(('space', SPACE))
    table.append(('type', TYPE_ID))
    table.append(('id', OBJECT_ID))

    print('>>> Building Lexer...')
    return Lexer(table, '$')


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



