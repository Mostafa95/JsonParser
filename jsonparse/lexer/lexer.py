from .parser_factory import TokenParserFactory

class JSONLexer:
    def __init__(self, inputStr):
        self.inputStr = inputStr
        self.ind = 0
        self.factory = TokenParserFactory()

    def has_more(self):
        return self.ind < len(self.inputStr)
    
    def peek(self, length=1):
        return self.inputStr[self.ind:self.ind+length]
    
    def advance(self, steps=1):
        self.ind += steps

    def tokenize(self):
        tokens = []
        while self.has_more():
            parser = self.factory.get_parser(self)
            if parser:
                parser.parse(self, tokens)
            else:
                raise ValueError(f"Invalid character at index {self.ind}")
        
        return tokens
