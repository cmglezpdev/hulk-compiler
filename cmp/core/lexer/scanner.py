from cmp.utils import Token
from .lexer import Lexer

digits = '|'.join(str(i) for i in range(0, 10))
nonzerodigits = '|'.join(str(i) for i  in range(1, 10))
lower = '|'.join(chr(i) for i in range(ord('a'), ord('z') + 1))
upper = '|'.join(chr(i) for i in range(ord('A'), ord('Z') + 1))
symbol = ['+', '-', '*', '/']

INTEGER = f'[{nonzerodigits}][.|ε][{digits}]^'
SYMBOLS = ['+', '-', '*', '/', '(', ')']
SPACE = '[ |\n|\t|\f|\r|\v][ |\n|\t|\f|\r|\v]^'

def build_lexer():
    table = [
        ('int', INTEGER),
        ('space', SPACE)
    ]
    for op in SYMBOLS:
        table.append((op, op))

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



