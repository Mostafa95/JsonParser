from .constants import *

class TokenParser:
    def can_parse(self, lexer):
        raise NotImplementedError

    def parse(self,lexer):
        raise NotImplementedError

class NullParser(TokenParser):
    def __init__(self):
        self.nullStr = 'null'
        self.nullLen = len(self.nullStr)

    def can_parse(self, lexer):
        return lexer.peek(self.nullLen) == self.nullStr
    
    def parse(self, lexer, tokens):
        tokens.append(None)
        lexer.advance(self.nullLen)

class WhiteSpaceParser(TokenParser):
    def __init__(self):
        pass

    def can_parse(self, lexer):
        return lexer.peek() == JSON_WHITESPACE or lexer.peek() == JSON_NEWLINE
    
    def parse(self, lexer, tokens):
        lexer.advance(1)

class ObjectParser(TokenParser):
    def __init__(self):
        pass

    def can_parse(self, lexer):
        return lexer.peek() == JSON_LEFTBRACE
    
    def parse(self, lexer, tokens):
        lexer.advance(1)  # Skip '{'
        object_tokens = [JSON_LEFTBRACE]
        while lexer.has_more():
            parser = lexer.factory.get_parser(lexer)
            if lexer.peek() == JSON_RIGHTBRACE:
                object_tokens.append(JSON_RIGHTBRACE)
                lexer.advance(1)
                break
            if parser:
                parser.parse(lexer, object_tokens)
            else:
                raise ValueError(f"Invalid character at ind {lexer.ind} , {lexer.inputStr[lexer.ind]}")

        tokens.append(object_tokens)

class StringParser(TokenParser):
    def can_parse(self, lexer):
        return lexer.peek() == JSON_QUOTE

    def parse(self, lexer, tokens):
        lexer.advance(1)  # Skip opening quote
        start = lexer.ind
        while lexer.has_more() and lexer.peek() != JSON_QUOTE:
            lexer.advance(1)
        if lexer.peek() != JSON_QUOTE:
            raise ValueError("Unterminated string")
        tokens.append(lexer.inputStr[start:lexer.ind])
        lexer.advance(1)  # Skip closing quote

class SyntaxParser(TokenParser):
    def can_parse(self, lexer):
        return lexer.peek() in JSON_SYNTAX

    def parse(self, lexer, tokens):
        tokens.append(lexer.peek())
        lexer.advance(1)

class NumberParser(TokenParser):
    def can_parse(self, lexer) :
        return lexer.peek().isdigit() or lexer.peek() == '-'

    def parse(self, lexer, tokens):
        start = lexer.ind
        while lexer.has_more() and (lexer.peek().isdigit() or lexer.peek() in {'.', 'e', 'E', '-', '+'}):
            lexer.advance(1)
        tokens.append(float(lexer.inputStr[start:lexer.ind]))

class ArrayParser(TokenParser):
    def can_parse(self, lexer) :
        return lexer.peek() == JSON_LEFTBRACKET

    def parse(self, lexer, tokens):
        lexer.advance(1)  # Skip '['
        array_tokens = [JSON_LEFTBRACKET]
        while lexer.has_more():
            parser = lexer.factory.get_parser(lexer)
            if lexer.peek() == JSON_RIGHTBRACKET:
                array_tokens.append(JSON_RIGHTBRACKET)
                lexer.advance(1)
                break
            if parser:
                parser.parse(lexer, array_tokens)
            else:
                raise ValueError(f"Invalid character at ind {lexer.ind} , {lexer.inputStr[lexer.ind]}")
        tokens.append(array_tokens)

class BooleanParser(TokenParser):
    def can_parse(self, lexer) :
        return lexer.peek(4) == "true" or lexer.peek(5) == "false"

    def parse(self, lexer, tokens):
        if lexer.peek(4) == "true":
            tokens.append(True)
            lexer.advance(4)
        else:
            tokens.append(False)
            lexer.advance(5)