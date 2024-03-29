from cmp.evaluation import evaluate_reverse_parse
from cmp.tools.parsing.lr1 import LR1Parser
from cmp.utils import Token
from cmp.core.grammar import G

def parse(tokens: list[Token]):
    print('>>> Parsing...')
    parse = LR1Parser(G)
    result = parse(tokens, get_shift_reduce=True)

    right_parse, operations = result

    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    return ast