# import zlib, base64
# exec(zlib.decompress(base64.b64decode('eJxdUMFuwjAMvecrfGy3qoLrJN86YGViCO2GECrF1SLSpErcqf37OUWwsZPtZ/v5+TXetVC3Xd6NtWs7bciDbjvnGV4/FmqJmsmrE1oaWFnUQdvAla1JFbhxltQaDVm1QLJ9S75iUmdqgL4r00tx7CofKGmyMn1RoBuwjqEB56ekFAw8ce+tggaXSZMqKCWWEge8kSQnaWSRQ0EVAok2K1iZ5uwuZI88dpSJWmlfyWB4EJF03p37mrWzkSXT9ou8/HU+xgHCImrbZAZ/5xSMf6q8Yvb61DMFBYz74vCUrBOTPs/l5OV/vZ8d8N8J+U5e1tkOtIVFYrJ5PBn92OVv4ZN8q21lInR78LLXBx2giBBLjtO/hgYByASaZld4miy7b+0QV/k7NRyxLY6yGDO5swVhi54X0+bEj9vkknF6P3H3azXZFEekGWlmh7u1150HxkmQSP0BhJm25Q==')))
# # Created by pyminifier (https://github.com/liftoff/pyminifier)

from cmp.pycompiler import EOF

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return
    
    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)
    
    assert isinstance(next(tokens).token_type, EOF)
    return result
    

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes
    
    synteticed = [None] * (len(body) + 1) 
    inherited = [None] * (len(body) + 1)
    inherited[0] = inherited_value # value inherited by the head
    
    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            
            lambda_inherit = attributes[i] # func that compute inherited value to the next prod
            if lambda_inherit is not None:
                inherited[i] = lambda_inherit(inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])
    
    lambda_synt = attributes[0] # func that compute the synteticed value of the head
    if lambda_synt is None:
        return None
    else:
        return lambda_synt(inherited, synteticed)