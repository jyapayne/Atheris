import pytest
from atheris.lexer import Lexer
from atheris.token import TokenType

@pytest.fixture(scope="module")
def lexer():
    return Lexer(open('example.ath'))

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
