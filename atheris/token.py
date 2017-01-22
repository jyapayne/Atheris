from enum import Enum

class TokenType(Enum):
    EOF = 1
    WS = 2

    IDENT = 3

    LET = 4
    VAR = 5

    INT = 6
    FLOAT = 7
    STRING = 8
    CHAR = 9

    LEFT_BRACKET = 10
    RIGHT_BRACKET = 11
    EQUALS = 12
    COLON = 13

    DEF = 14
    CLASS = 15

    INDENT = 16
    DEDENT = 17

    FOR = 18
    IN = 19

    NUMBER = 20
    QUOTE = 21
    DB_QUOTE = 22


class Token(object):

    keyword_map = {
        'def': TokenType.DEF,
        'var': TokenType.VAR,
        'class': TokenType.CLASS,
        'let': TokenType.LET,
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'string': TokenType.STRING,
        'char': TokenType.CHAR,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        '(': TokenType.LEFT_BRACKET,
        ')': TokenType.RIGHT_BRACKET,
        '=': TokenType.EQUALS,
        ':': TokenType.COLON,
        '\'': TokenType.QUOTE,
        '"': TokenType.DB_QUOTE
    }

    def __init__(self, token_type=None, content=None, line=0, col=0):
        self.token_type = token_type
        self.content = content

        self.line = line
        self.col = col

    def __str__(self):
        return ('Token(type: {}, content: {}, '
                'line: {}, col: {})'.format(self.token_type, self.content,
                                            self.line, self.col))
