import re
from typing import NamedTuple, Generator


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


class Tokenizer:
    def __init__(self, code: Generator[str, str, str]):
        self.code = code
        self.col = 0
        self.line = 0
        self.fragment = next(code, None)

    def __get_fragment(self):
        if self.fragment is None:
            return self.fragment
        if self.col >= len(self.fragment):
            self.fragment = next(self.code, None)
            self.col = 0
            return self.__get_fragment()
        return self.fragment[self.col:]

    def __get_token(self, type_, value):
        return Token(type_, value, self.line, self.col)

    def __error(self, msg=''):
        raise Exception(msg)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        token_specification = [
            ('NEWLINE', '\n'),
            ('IGNORED', r'\s+'),
            ('REGISTER', r'R\d+(?!\w)'),
            ('NUMERIC_LITERAL', r'\d+'),  # Integer or decimal number
            ('PC_REG', r'^PC(?!\w)'),  #
            ('SP_REG', r'^SP(?!\w)'),  #
            ('RV_REG', r'^RV(?!\w)'),  #
            ('MEM', r'M(?=\[)'),  #
            ('LB', r'\['),  #
            ('RB', r'\]'),  #
            ('COMMA', ','),
            ('INT_CAST', r'\.\d'),  # change the name to something better, matches .1, .2 ...
            ('PLUS', r'\+'),
            ('MINUS', '-'),
            ('MUL', r'\*'),
            ('DIV', '/'),
            ('BRANCH_OP', 'B(LT|LE|GT|GE|EQ|NE)'),  # matches branch operators: BLT, BLE, BGT, BGE, BEQ, BNE
            ('JUMP_OP', r'JMP\b'),  # not sure if this is correct
            ('CALL_OP', r'CALL\b'),
            ('LT', '<'),
            ('GT', '>'),
            ('EQ', '='),
            ('IDENTIFIER', '[a-zA-Z]+'),
            ('OTHER', '.')  # everything else
        ]
        fragment = self.__get_fragment()
        if fragment is None:
            return self.__get_token('EOF', None)
        for token_type, token_regex in token_specification:
            match = re.match(token_regex, fragment)
            if not match:
                continue
            if token_type == 'NEWLINE':
                self.line += 1
                self.col += match.end()
                return self.get_next_token()
            if token_type == 'IGNORED':
                self.col += match.end()
                return self.get_next_token()
            if token_type == 'OTHER':
                self.__error("Error: unexpected symbol: '" + match.group() + "' on line {self.pos}")
            self.col += match.end()
            return self.__get_token(token_type, match.group())
