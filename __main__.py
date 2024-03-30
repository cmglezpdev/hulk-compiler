import os
from cmp.core.lexer.scanner import build_lexer, tokenizer
from cmp.core.parser.parser import parse, build_parser



def load_tests():
    files = os.listdir('./tests/')
    files = [file for file in files if file.endswith('.hulk')]

    tests = []
    for file in files:
        with open(f'./tests/{file}', 'r') as test:
            tests.append((file, test.read()))

    return tests

if __name__ == '__main__':
    tests = load_tests()
    lexer = build_lexer()
    parser = build_parser()

    for file, content in tests:
        print(f'Parsing code: {file}\n\n')
        
        code_tokens = tokenizer(content, lexer=lexer)
        print([t.lex for t in code_tokens])
        print([t.token_type for t in code_tokens])
        right_most_parse, operations = parser(code_tokens, get_shift_reduce=True)
        print(right_most_parse)
        print(f'Code parsed successfully!!\n\n\n')
        print('------------------------------------------')




