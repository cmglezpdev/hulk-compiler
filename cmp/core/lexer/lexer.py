from cmp.utils import Token
from cmp.tools.regex import Regex
from cmp.automata import State

class Lexer:
    """
        ### Lexer
        Implementemos el generador de lexer. El lexer se construirá a partir de la tabla de expresiones regulares (una lista de tuplas con la forma: `(<token_type>, <regex_str>)`). Esta tabla se recibe como el parámetro `table` en el contructor de la clase `Lexer`. La prioridad/relevancia de cada tipo de token está marcada por el índice que ocupa en la tabla. Los tipos de tokens cuyas expresiones regulares estén registradas más cerca del inicio de la tabla tiene más prioridad.
        - **_build_regexs:** devuelve un lista con los autómatas (instancias de `State`) de cada expresión regular. Los estados finales de los respectivos autómatas deben marcarse (campo `tag`) con la prioridad y tipo de token según la expresión regular que lo originó.
        - **_build_automaton:** devuelve la versión determinista del autómata que reconoce los tokens del lenguaje.
        - **_walk:** Devuelve el último estado final visitado, y lexema consumido, durante el reconocimiento del string que se recibe como entrada.
        - **_tokenize:** Devuelve tuplas de la forma `(lex, token_type)` que resultan de tokenizar la entrada. Debe manejar el caso en que la entrada no puede ser tokenizada completamente (se detecta cuando en una iteración la cadena no avanzó).
    """
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            regx = Regex(regex)
            automaton = State.from_nfa(regx.automaton)
            # display(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (n, token_type)
            regexs.append(automaton)
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)

        return start.to_deterministic()
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            try:
                state = state[symbol][0]
                lex += symbol
                if state.final:
                    final = state if state.final else final
                    final_lex = lex
            except TypeError:
                break
        
        return final, final_lex
    
    def _tokenize(self, text):
        remaining_text = text
        while remaining_text:
            final_state, lexeme = self._walk(remaining_text)
            if final_state:
                sorted_states = [s for s in final_state.state if s.tag is not None]
                sorted_states.sort(key= lambda x: x.tag[0])
                
                yield lexeme, sorted_states[0].tag[1] # token_type
                remaining_text = remaining_text[len(lexeme):]
            else:
                yield remaining_text[0], 'ERROR'
                remaining_text = remaining_text[1:]
                
        yield '$', self.eof
    
    def __call__(self, text: str):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]