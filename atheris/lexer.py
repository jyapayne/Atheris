from io import StringIO
from atheris.token import TokenType, Token


class Scanner(object):
    def __init__(self, obj):
        buf = None
        if isinstance(obj, str):
            buf = StringIO(obj)
        else:
            buf = obj

        self.buf = buf

    def readline(self):
        return self.buf.readline()

    def read(self):
        return self.buf.read(1)

    def unread(self):
        self.buf.seek(self.buf.tell()-1)


class Lexer(object):
    def __init__(self, obj):
        self.scanner = Scanner(obj)
        self.pos = 0
        self.col = 0
        self.line = 0
        self.line_buf = ''
        self.cur_char = ''
        self.indent_stack = []
        self.advance()

    def fill_buffer(self):
        self.line_buf = self.scanner.readline().rstrip('\n').rstrip('\r\n')

    def advance(self, return_on_newline=False):
        self.pos += 1
        self.col += 1

        end_of_line = False

        if self.pos < len(self.line_buf):
            self.cur_char = self.line_buf[self.pos]
        else:
            end_of_line = True
            if return_on_newline:
                return end_of_line
            # if we've reached the end of the line, fill er up again
            self.fill_buffer()
            if self.line_buf:
                self.pos = 0
                self.line += 1
                self.col = 1
                self.cur_char = self.line_buf[self.pos]
            else:
                # no more characters
                self.cur_char = ''
        return end_of_line

    def get_indent(self):
        indent = 0

        end_of_line = False
        while self.cur_char.isspace() and self.cur_char and not end_of_line:
            indent += 1
            end_of_line = self.advance(True)

        token = None

        if self.indent_stack:

            last_indent = self.indent_stack[-1]
            if indent < last_indent:
                self.indent_stack.pop()
                size = last_indent - indent
                self.col -= 1
                token = Token(TokenType.DEDENT, size, self.line, self.col)
                self.advance()
            elif indent > last_indent:
                self.indent_stack.append(indent)
                size = indent - last_indent
                self.col -= 1
                token = Token(TokenType.INDENT, size, self.line, self.col-size)
                self.advance()

        elif indent > 0:
            self.indent_stack.append(indent)
            self.col -= 1
            token = Token(TokenType.INDENT, indent, self.line, 1)
            self.advance()

        return token

    def next_token(self):
        cur_col = self.col
        cur_line = self.line

        if self.cur_char:
            if self.pos == 0:
                indent = self.get_indent()
                if indent is not None:
                    return indent

            while self.cur_char.isspace():
                self.advance()

            if self.cur_char.isdigit() or self.cur_char == '.':
                num_str = ''

                while self.cur_char.isdigit() or self.cur_char == '.':
                    num_str += self.cur_char
                    self.advance()

                return Token(TokenType.NUMBER, num_str, cur_line, cur_col)

            elif self.cur_char == '#':
                self.advance()

                while self.cur_char and self.cur_char not in set(['\n', '\r']):
                    self.advance()

                return self.next_token()

            elif self.cur_char in Token.keyword_map:
                last = self.cur_char
                self.advance()
                return Token(Token.keyword_map[last], last,
                             cur_line, cur_col)

            elif not self.cur_char.isspace():
                id_str = ''

                while not self.cur_char.isspace() and not self.cur_char in Token.keyword_map:
                    id_str += self.cur_char
                    self.advance()

                if self.cur_char in Token.keyword_map and not id_str:
                    token = Token(Token.keyword_map[self.cur_char],
                                  self.cur_char,
                                  cur_line, cur_col)
                    self.advance()
                    return token

                if id_str in Token.keyword_map:
                    return Token(Token.keyword_map[id_str], id_str,
                                 cur_line, cur_col)
                else:
                    return Token(TokenType.IDENT, id_str, cur_line, cur_col)


        if self.indent_stack:
            # Extra indents that have not been taken care of (ie: at the
            # end of an indented file)
            indent = self.indent_stack.pop()

            content = indent

            if self.indent_stack:
                previous_indent = self.indent_stack[-1]
                content = indent - previous_indent

            return Token(TokenType.DEDENT, content, cur_line+1, 1)

        return Token(TokenType.EOF, '', cur_line+1, 1)

    def tokens(self):
        token = self.next_token()
        while token.token_type != TokenType.EOF:
            yield token
            token = self.next_token()
        yield token

if __name__ == '__main__':
    import sys
    lexer = Lexer(open(sys.argv[1]))

    for token in lexer.tokens():
        print(token)
