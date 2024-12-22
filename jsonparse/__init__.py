from .lexer import JSONLexer
from .parser import JSONParser

def from_string(input):
    lex = JSONLexer(input)
    tokens = lex.tokenize()
    if len(tokens):
        tokens=tokens[0]
    print('tokens ' + str(tokens))
    par = JSONParser(tokens)
    ans = par.parse()
    print('parsed '+str(ans))
    return ans