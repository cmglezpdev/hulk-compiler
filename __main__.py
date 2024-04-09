import os
import sys
import argparse
from cmp.core.lexer.scanner import build_lexer, semantic_checker, tokenizer, type_checker,type_collector
from cmp.core.parser.parser import build_parser,parse
from cmp.core.semantics  import SemanticCheckerVisitor
from cmp.core.type_check import TypeCheckingVisitor
from cmp.core.hulkToCIL import HULKToCIL
from cmp.cil import get_formatter


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

def load_file(file: str):
    content = ''
    with open(file, 'r') as f:
        content = f.read()

    return file, content

def load_args():
    arg_parser = argparse.ArgumentParser("Execute compiler")
    arg_parser.add_argument('--file', type=str, help="Execute a hulk file")
    arg_parser.add_argument('--test-id', type=int, help="Execute a specific test")
    arg_parser.add_argument('--test-range', type=int, nargs=2, metavar=('start', 'end'), help="Execute test in the range especified")
    
    args = arg_parser.parse_args()
    file = args.file    
    test_id = args.test_id
    test_range = args.test_range

    return {
        'file': file,
        'test_id': test_id,
        'test_range': test_range
    }


if __name__ == '__main__':
    lexer = build_lexer()
    parser = build_parser()
    sem_checker = SemanticCheckerVisitor()
    t_checker = TypeCheckingVisitor()

    args = load_args()
    if args['file'] is not None or args['test_id'] is not None:
        file, content = None, None
        if args['file'] is not None:
            file, content = load_file(args['file'])
        else:
            file, content = load_file(f'./tests/test.{args['test_id']}.hulk')        
    
        print(f'\n\n\nParsing code: {file}')
        code_tokens = tokenizer(content, lexer=lexer)
        ast = parse(code_tokens,parser=parser)
        
        context = type_collector(ast)
        scope, serrors = semantic_checker(ast, sem_checker,context)
        terrors = type_checker(ast, t_checker,context)
        
        if(len(serrors) > 0):
            print(">>> %d errors founded:" %(len(serrors)))
            for e in serrors:
                print('* %s' %(e))
        
        if(len(terrors) > 0):
            print(">>> %d errors founded:" %(len(terrors)))
            for e in terrors:
                print('* %s' %(e))
    
        sem_checker.errors = []
        
        print('--------------------------')
        print(context)
        print('--------------------------')

        hulkToCil = HULKToCIL(context)
        cil_ast = hulkToCil.visit(ast, scope)
        formatter = get_formatter()
        print(formatter(cil_ast))
        
    else:
        try:
            left_test, right_test = args['test_range']
        except:
            left_test, right_test = None, None

        tests = load_tests(left_test, right_test)
        for file, content in tests[:6]:
            print(f'\n\n\nParsing code: {file}')
            
            code_tokens = tokenizer(content, lexer=lexer)
            ast = parse(code_tokens,parser=parser)
            
            context = type_collector(ast)
            scope, serrors = semantic_checker(ast, sem_checker,context)
            terrors = type_checker(ast, t_checker,context)
            
            if(len(serrors) > 0):
                print(">>> %d errors founded:" %(len(serrors)))
                for e in serrors:
                    print('* %s' %(e))
            
            if(len(terrors) > 0):
                print(">>> %d errors founded:" %(len(terrors)))
                for e in terrors:
                    print('* %s' %(e))
            
            
            
            sem_checker.errors = []
            
            print('--------------------------')
            print(context)
            print('--------------------------')

            hulkToCil = HULKToCIL(context)
            cil_ast = hulkToCil.visit(ast, scope)
            formatter = get_formatter()
            print(formatter(cil_ast))


