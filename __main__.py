# from cmp.pycompiler import Grammar
# from cmp.tools.lexer import Lexer

# # ===================================================== START TEST DEL LEXER ========================================================

# nonzero_digits = '|'.join(str(n) for n in range(1,10))
# letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

# print('Non-zero digits:', nonzero_digits)
# print('Letters:', letters)

# G = Grammar()
# _num, _for, _foreach, _space, _id = G.Terminals('num, for, foreach, space, id')

# # En los tipos de tokens se deben usar los simbolos de la gramática
# lexer = Lexer([
#     ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
#     ('for' , 'for'),
#     ('foreach' , 'foreach'),
#     ('space', '  *'),
#     ('id', f'({letters})({letters}|0|{nonzero_digits})*')
# ], 'eof')

# text = '5465 for 45foreach fore'
# print(f'\n>>> Tokenizando: "{text}"')

# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
# assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

# text = '4forense forforeach for4foreach foreach 4for'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
# assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']

# # ===================================================== END TEST DEL LEXER ========================================================




from cmp.core.lexer.scanner import build_lexer, tokenizer




if __name__ == '__main__':
    lexer = build_lexer()
    code_tokens = tokenizer(
        """
        (5.5 + 0.5) * 2 - 34 /2;
        let x: Number in (let y = 5 in x + y);
        let x = 1 > 3, y = 7 < 8 in (x & y == (true | false)); 
        """,
    lexer=lexer)
    print([t.lex for t in code_tokens])
    print([t.token_type for t in code_tokens])




