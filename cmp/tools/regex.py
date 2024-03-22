# import zlib, base64
# exec(zlib.decompress(base64.b64decode('eJytVsFu2zgQvesreFhDVE0IdY8BCNTZtVRg2yyaOKgdwxAYiYrZSKRK0qnttp+1v7HftCQlWbLWTXPYgwzyzXDem9Fw5FyKEqRlFRKlASsrITWYalGy9EpkFF0yTuTeLW/blZe3Z6p9KsqKFVS2R2NJypLIzkULUaiQbE1IoknjBv+IpujKPC2epIVQW0l7gOAp0ZQTzQTv4JJxVrLDAN1yu+U5SbRIspwEQ376RIqtO9QKbRCaVEQqOvS3IOMPrXNJtchEUkmasVSzJ5FwkUiabo3Xk+gObzUrVHtoLh4p975gk6uXFkQpMKsUKwS3NYRdjYMLD2Q0PyqCiha5BYGkeis5+AKVNrjCE5Sb11EovHq9RloSrphNSeFvPwJP4l74hvBmX96L4sV8CttlWNDdGfI3R/LJgBy+Riq4mBgNKe4YGwm/1y/WaTh2kGV7a+Oy1JR2I7JakaiotIKsMNqvwLBNGg/vI+6FbwhvbS84uq53f8FXuHBI/pzXNdjAz7vGR642Wde0/zf5yVUYiogi3LF6NrCkD3RnLoLpPnagEmq60yhG6pFVydcNM++yIql5oXNZ823wau2BOMbfdheuZ+EOxavdOsiFBDvA+Mr/7iP/lXmgeQLz/PO3v/7hAetwMA7AUljlLAdDGkB4Bg4hU24LXYLAZKQZ31Kz1nLvoM84jlcHIwTQXUorDf6k+5mUQjbWWtnBKPOV6zF/HRiL68miDrEJSVVRnsHPxnLc1Af933wUh7O/osDYmgJvXLnut6zIkod6bjl9MY7bnQdmOA6vBJ9TWVoq6M985CrngTmK0BQt0BLdnTop6M9BBKZgAZbgzjeuFfqAbtAlIujWuPb8voNXAIIA1DkBU1jLOcLz8QIVpLzPCNggdaFWb9bIMNBTcGLqtRjhajzr49dwYweEPRM4u0m8Hg19L+tjchjhaLx8IdXS6OqjUdQyTSzT8lmmaISn47sXMt2N8Ic++tERBc7wDMd0hEkfTWEjzRhu+wbZM9yMZ+PLoa5jk8RejAct4r3Hz38QYBw0A+Ha3sVm3iaJ+XbpJHHzFrlb+t9LGZmuqKfAJzeM7SJ0vtj9un0zGQTHn8Ja2xGBzitoGVNzOVpGe0lPIzcp9gIaqlQ82LnhxkZwdnKdpXwulQ0ezqT6yJmhVB+yFxu/hxu7mOPTTzXMkcPf4Xl4/IRZYIG7PwDwnUUe8dn/DXARdMk/ev8C0IsPHg==')))
# # Created by pyminifier (https://github.com/liftoff/pyminifier)


from cmp.pycompiler import Grammar
from cmp.tools.automata import NFA, nfa_to_dfa
from cmp.tools.automata import automata_union, automata_concatenation, automata_closure, automata_minimization
from cmp.ast import get_printer, AtomicNode, UnaryNode, BinaryNode
from cmp.utils import Token
from cmp.tools.parsing.ll1 import LL1Parser
from cmp.tools.evaluation import evaluate_parse

printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)

# AST Nodes
EPSILON = 'ε'
class EpsilonNode(AtomicNode):
    def evaluate(self):
        states = 1
        finals = [0]
        transitions = {}
        return NFA(states, finals, transitions)
# EpsilonNode(EPSILON).evaluate()

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        states = 2
        finals = [1]
        transitions = {(0, s): [1]}
        return NFA(states, finals, transitions)
# SymbolNode('a').evaluate()

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)
# ClosureNode(SymbolNode('a')).evaluate()

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)
# UnionNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)
# ConcatNode(SymbolNode('a'), SymbolNode('b')).evaluate()



G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# > PRODUCTIONS
E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2])
X %= G.Epsilon, lambda h,s: h[0]

T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]

Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0], s[1])
Y %= G.Epsilon, lambda h,s: h[0]

F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]

Z %= star + Z, lambda h,s: s[2], None, lambda h,s: ClosureNode(h[0])
Z %= G.Epsilon, lambda h,s: h[0]

A %= symbol, lambda h,s: SymbolNode(s[1]), None
A %= opar + E + cpar, lambda h,s: s[2], None, None, None
A %= epsilon, lambda h,s: EpsilonNode(s[1]), None



def regex_tokenizer(text, G, skip_whitespaces=True) -> list[Token]:
    tokens = []
    fixed_tokens = {
        '|': Token('|', pipe),
        '*': Token('*', star),
        'ε': Token('ε', epsilon),
        '(': Token('(', opar),
        ')': Token(')', cpar),
    }

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        try:
            tokens.append(fixed_tokens[char])
        except KeyError:
            tokens.append(Token(char, symbol))

    tokens.append(Token('$', G.EOF))
    return tokens

class Regex:
    def __init__(self, regex: str, skip_whitespaces=False) -> None:
        self.regex = regex
        self.automaton = self.build_automaton(regex, skip_whitespaces)
        
    def __call__(self, text: str):
        return self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex: str, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, G, skip_whitespaces)
     
        parser = LL1Parser(G)
        left_parse = parser([t.token_type for t in tokens])
        
        ast = evaluate_parse(left_parse, tokens)
        print(printer(ast))
        # Automaton
        nfa = ast.evaluate()
        # display(nfa)
        dfa = nfa_to_dfa(nfa)
        # display(dfa)
        mini = automata_minimization(dfa)
        # display(mini)
        return mini
