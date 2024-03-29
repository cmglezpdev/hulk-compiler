from cmp.core.lexer.scanner import build_lexer, tokenizer
from cmp.core.parser.parser import parse

tests = [
    "42;",
    "print(42);",
    "print((((1 + 2) * 3) * 4) / 5);",
    "print(sin(2 * PI) * 2 + cos(3 * PI / log(4, 64)));",
    """ let a = 0, c = 2 in
        let b = 1 , x =2+5-(3*9) in {
            print(a);
            print(b);
        };
    """,
    # """
    # (5.5 + 0.5) * 2 - 34 /2;
    # let x: Number in (let y = 5 in x + y);
    # let x = 1 > 3, y = 7 < 8 in (x & y == (true | false)); 
    # """
]


if __name__ == '__main__':
    lexer = build_lexer()
    
    for t in tests:
        print(f'Parsing:\n{t}\n\n')
        
        code_tokens = tokenizer(t, lexer=lexer)
        print([t.lex for t in code_tokens])
        print([t.token_type for t in code_tokens])
        parse(code_tokens)
        
        print(f'Code {t} parsed successfully!!\n\n\n')




