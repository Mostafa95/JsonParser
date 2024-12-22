import sys
from .lexer import lex
from .parser import parse

sys.path.append(".")
def from_string(input):
    tokens = lex(input)
    print('tokens ',tokens)
    ans = parse(tokens)
    print('parsed ',ans)
    return ans

