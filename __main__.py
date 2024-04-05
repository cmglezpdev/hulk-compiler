import os
import sys
import argparse
from cmp.core.lexer.scanner import build_lexer, semantic_checker, tokenizer, type_checker
from cmp.core.parser.parser import build_parser
from cmp.core.semantics  import SemanticCheckerVisitor
from cmp.core.type_check import TypeCheckingVisitor


def load_tests(left_test, right_test):
    files = os.listdir('./tests/')
    files = [file for file in files if file.endswith('.hulk')]

    if left_test is None:
        left_test = 1
    
    if right_test is None:
        right_test = len(files)

    print('>>> Execute tests between [%d, %d]'%(left_test, right_test))

    tests = []
    for file in files:
        try:
            test_id  = int(file.split('.')[1])
            if left_test <= test_id and test_id <= right_test:
                with open(f'./tests/{file}' , 'r') as test:
                    tests.append((file, test.read()))
        except:
            print('Test with id %d not exists.' %(test_id))
            continue
    return tests

def load_args():
    
    arg_parser = argparse.ArgumentParser("Execute compiler")
    arg_parser.add_argument('--test-id', type=int, help="Execute a specific test")
    arg_parser.add_argument('--test-range', type=int, nargs=2, metavar=('start', 'end'), help="Execute test in the range especified")
    
    args = arg_parser.parse_args()
    test_id = args.test_id
    test_range = args.test_range
    
    if test_id is None and test_range is None:
        return [None, None]
    
    if test_id is not None and test_range is not None:
        raise Exception('You must provide just a test_id or a range, not both')
    
    if test_id is not None:
        return [test_id, test_id]
    
    return test_range
        

if __name__ == '__main__':
    [left_test, right_test] = load_args()
    tests = load_tests(left_test, right_test)
    lexer = build_lexer()
    parser = build_parser()
    sem_checker = SemanticCheckerVisitor()
    t_checker = TypeCheckingVisitor()

    for file, content in tests:
        print(f'\n\n\nParsing code: {file}')
        
        code_tokens = tokenizer(content, lexer=lexer)
        ast = parser(code_tokens)
        serrors = semantic_checker(ast, sem_checker)
        terrors = type_checker(ast, t_checker)
        
        print(serrors, terrors)
        if(len(serrors) > 0):
            print(">>> %d errors founded:" %(len(serrors)))
            for e in serrors:
                print('* %s' %(e))
        
        if(len(terrors) > 0):
            print(">>> %d errors founded:" %(len(terrors)))
            for e in terrors:
                print('* %s' %(e))
        
        
        
        sem_checker.errors = []




