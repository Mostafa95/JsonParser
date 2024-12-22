# parser.py

from ..lexer.constants import *

class BaseParser:
    def __init__(self, tokens, ind):
        self.tokens = tokens
        self.ind = ind

    def validate_value(self, value):
        if isinstance(value,(int,float,str,bool,list,type(None))):
            return value
        raise ValueError(f"Unexpected value: {value}")
    
    def parse(self):
        raise NotImplementedError


class ObjectParser(BaseParser):
    def parse(self):
        ans = {}

        if self.tokens[self.ind] == JSON_RIGHTBRACE:
            return ans

        while True:
            
            if self.tokens[self.ind] in JSON_BLACKLIST:
                raise ValueError(f"Unexpected token in object: {self.tokens[self.ind]}")
            key = self.tokens[self.ind]
            self.ind += 1

            if self.tokens[self.ind] != JSON_COLON:
                raise ValueError(f"Expected colon after key, got: {self.tokens[self.ind]}")
            self.ind += 1

            value = self._parse_value()
            ans[key] = value

            if self.tokens[self.ind] == JSON_RIGHTBRACE:
                break
            if self.tokens[self.ind] == JSON_COMMA:
                self.ind += 1
                continue

            raise ValueError(f"Expected comma or closing brace, got: {self.tokens[self.ind]}")
        
        return ans

    def _parse_value(self):
        value = self.tokens[self.ind]
        if isinstance(value, list) and value[0] == JSON_LEFTBRACKET:
            value = ArrayParser(value, 1).parse()
        elif isinstance(value, list) and value[0] == JSON_LEFTBRACE:
            value = ObjectParser(value, 1).parse()
        else:
            value = self.validate_value(value)
        self.ind += 1
        return value


class ArrayParser(BaseParser):
    def parse(self):
        ans = []
        if self.tokens[self.ind] == JSON_RIGHTBRACKET:
            return ans
        
        while True:
            value = self._parse_value()
            ans.append(value)

            if self.tokens[self.ind] == JSON_COMMA:
                self.ind += 1
                continue
            elif self.tokens[self.ind] == JSON_RIGHTBRACKET:
                break
            else:
                raise ValueError(f"Unexpected token in array: {self.tokens[self.ind]}")

        return ans

    def _parse_value(self):
        value = self.tokens[self.ind]
        if isinstance(value, list) and value[0] == JSON_LEFTBRACKET:
            value = ArrayParser(value, 1).parse()
        elif isinstance(value, list) and value[0] == JSON_LEFTBRACE:
            value = ObjectParser(value, 1).parse()
        else:
            value = self.validate_value(value)
        self.ind += 1
        return value


class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ind = 1

    def parse(self):
        if not self.validate_form():
            raise Exception("Invalid token structure.")

        return ObjectParser(self.tokens, self.ind).parse()

    def validate_form(self):
        if self.tokens is None or len(self.tokens)==0:
            return False

        tokenStack = []
        for self.token in self.tokens:
            if self.token ==  JSON_LEFTBRACKET or self.token == JSON_LEFTBRACE:
                tokenStack.append(self.token)            
            if self.token == JSON_RIGHTBRACKET and tokenStack[-1] == JSON_LEFTBRACKET:
                tokenStack.pop()
            if self.token == JSON_RIGHTBRACE and tokenStack[-1] == JSON_LEFTBRACE:                
                tokenStack.pop()
        return len(tokenStack)==0
