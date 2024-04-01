import os
import sys
from cmp.core.lexer.scanner import build_lexer, semantic_checker, tokenizer
from cmp.core.parser.parser import parse, build_parser
from cmp.core.semantics  import SemanticCheckerVisitor
from cmp.core.type_check import TypeCheckingVisitor



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
    sem_checker = SemanticCheckerVisitor()
    type_checker = TypeCheckingVisitor()

    for file, content in tests:
        print(f'Parsing code: {file}\n\n')
        
        code_tokens = tokenizer(content, lexer=lexer)
        ast = parse(code_tokens)
        serrors = semantic_checker(ast, sem_checker)
        
        if len(serrors) == 0:
            terrors = type_checker.visit(ast)
            print(terrors)

        print(serrors)
        sem_checker.errors =[]




