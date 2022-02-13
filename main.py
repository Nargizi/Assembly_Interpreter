import re
from typing import NamedTuple


class Token(NamedTuple):  # not sure what this does tbh
    def __init(self, type, value):
        self.type = type
        self.value = value

    type: str
    value: str
    # line: int
    # column: int

class Tokenizer:
    def __init__(self, text):
        self.code = text
        self.pos = 0
        # self.current_char = self.text[self.pos]

    def get_next_token(self):

        token_specification = [
            ('REGISTER', 'R\d+(?!\w)'),
            ('NUMERIC_LITERAL', '\d+'),  # Integer or decimal number
            ('PC_REG', '^PC(?!\w)'),  #
            ('SP_REG', '^SP(?!\w)'),  #
            ('RV_REG', '^RV(?!\w)'),  #
            ('MEM', 'M(?=\[)'),  #
            ('LB', '\['),  #
            ('RB', '\]'),  #
            ('COMMA', ','),
            ('INT_CAST', '\.\d'),  # change the name to something better, matches .1, .2 ...
            ('ARITHM_OP', '[\-\+\*\/]'),
            ('BRANCH_OP', 'B(LT|LE|GT|GE|EQ|NE)'),  # matches branch operators: BLT, BLE, BGT, BGE, BEQ, BNE
            ('JUMP_OP', '^JMP\b'),  # not sure if this is correct
            ('CALL_OP', '^CALL\b'),
            ('LT', '<'),
            ('GT', '>'),
            ('EQ', '='),
            ('NEWLINE', '\n'),
            ('IGNORED', '\s+'),
            ('IDENTIFIER', '[a-zA-Z]+'),
            ('OTHER', '.')  # everything else
        ]
        if self.pos > len(self.code) - 1:
            self.pos += 1
            return Token('EOF', None)

        for token_type, token_regex in token_specification:
            match = re.match(token_regex, self.code[self.pos:])
            if not match:
                continue
            if token_type == 'IGNORED':
                self.pos += match.end()
                return self.get_next_token()
            if token_type == 'OTHER':
                raise RuntimeError("Error: unexpected symbol: '" + match.group() + "' on line {self.pos}")
            self.pos += match.end()
            return Token(token_type, match.group())

# test = '''R123 = 12
#         Mem[R2] = 12
#         R3 = R2
#     ENDIF;
# '''


test = "M[R1 + 4] =.1 R2"

if __name__ == '__main__':
    tokenizer = Tokenizer(test)
    while True:
        token = tokenizer.get_next_token()
        if token.type == "EOF":
            break
        else:
            print("shemovida",  token.type, token.value)
