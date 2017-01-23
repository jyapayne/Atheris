import pytest
from atheris.lexer import Lexer
from atheris.token import TokenType

from .config import TEST_PATH

def test_large_file():
    lexer = Lexer(open(TEST_PATH+'/example.ath'))
    tokens = list(lexer.tokens())

def test_idents():
    lexer = Lexer('junk flop')
    tokens = list(lexer.tokens())
    assert tokens[0].token_type == TokenType.IDENT

def test_comments():
    lexer = Lexer('# balls and stuff')
    tokens = list(lexer.tokens())
    assert tokens[0].token_type == TokenType.COMMENT
    assert tokens[0].content == ' balls and stuff'

def test_keywords():
    lexer = Lexer('def let var int float for in class')
    tokens = list(lexer.tokens())

    assert tokens[0].token_type == TokenType.DEF
    assert tokens[1].token_type == TokenType.LET
    assert tokens[2].token_type == TokenType.VAR
    assert tokens[3].token_type == TokenType.INT
    assert tokens[4].token_type == TokenType.FLOAT
    assert tokens[5].token_type == TokenType.FOR
    assert tokens[6].token_type == TokenType.IN
    assert tokens[7].token_type == TokenType.CLASS

def test_simple_codeblock():
    lexer = Lexer('def stuff():\n    pass')
    tokens = list(lexer.tokens())

    assert tokens[5].token_type == TokenType.INDENT
    assert tokens[5].content == 4
    assert tokens[7].token_type == TokenType.DEDENT
    assert tokens[7].content == 4

def test_hanging_indents():
    lexer = Lexer('x\n    \n        \n')
    tokens = list(lexer.tokens())

    assert tokens[0].token_type == TokenType.IDENT
    assert tokens[0].content == 'x'
    assert tokens[0].line == 1
    assert tokens[0].col == 1

    assert tokens[1].token_type == TokenType.INDENT
    assert tokens[1].content == 4
    assert tokens[1].line == 2
    assert tokens[1].col == 1

    assert tokens[2].token_type == TokenType.INDENT
    assert tokens[2].content == 4
    assert tokens[2].line == 3
    assert tokens[2].col == 4

    assert tokens[3].token_type == TokenType.DEDENT
    assert tokens[3].content == 4
    assert tokens[3].line == 4
    assert tokens[3].col == 1

    assert tokens[4].token_type == TokenType.DEDENT
    assert tokens[4].content == 4
    assert tokens[4].line == 4
    assert tokens[4].col == 1

    assert tokens[5].token_type == TokenType.EOF
    assert tokens[5].content == ''
    assert tokens[5].line == 4
    assert tokens[5].col == 1
