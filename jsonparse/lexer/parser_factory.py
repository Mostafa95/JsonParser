from .token_parser import BooleanParser,ArrayParser,NumberParser,SyntaxParser,StringParser,NullParser,ObjectParser,WhiteSpaceParser

class TokenParserFactory:
    def __init__(self):
        self.parsers = [NullParser(),
                        ObjectParser(),
                        WhiteSpaceParser(),
                        StringParser(),
                        SyntaxParser(),NumberParser(),
                        ArrayParser(),BooleanParser()]
        
    def get_parser(self, lexer):
        for parser in self.parsers:
            if parser.can_parse(lexer):
                return parser
        return None