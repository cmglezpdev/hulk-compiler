from cmp.core.lexer.scanner import build_lexer, tokenizer
from cmp.core.parser.parser import parse




if __name__ == '__main__':
    lexer = build_lexer()
    code_tokens = tokenizer(
       # """
       # (5.5 + 0.5) * 2 - 34 /2;
       # let x: Number in (let y = 5 in x + y);
       # let x = 1 > 3, y = 7 < 8 in (x & y == (true | false)); 
       # """,
       "(4*5)/3+9*8;",
    lexer=lexer)

    print([t.lex for t in code_tokens])
    print([t.token_type for t in code_tokens])

    parse([t.token_type for t in code_tokens])




