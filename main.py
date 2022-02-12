import re

# class TokenType(Enum):
#     NUMERIC_LITERAL,
#     REGISTER,
#     PC_REG,
#     SP_REG,
#     RV_REG,
#     MEM,
#     LB,
#     RB,
#     OP,
#     COMMA,
#     BRANCH_OP,
#     JUMP_OP,
#     CALL_OP,
#     LT_OP,
#     GT_OP,
#     EQ_OP,
#     IDENTIFIER

class Token(object):
    type: str
    value: int


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        pass

    def get_next_token(self):
        token_specification = [
            ('NUMERIC_LITERAL', '\d+'),  # Integer or decimal number
            ('REGISTER', 'R\d+'),  #
            ('PC_REG', '^PC$'),  #
            ('SP_REG', '^SP$'),  #
            ('RV_REG', '^RV$'),  #
            ('MEM', '^MEM$'),  #
            ('LB', '\['),  #
            ('RB', '\]'),  #
            ('COMMA', ','),
            ('ARITHM_OP', r'[-+*\]'),
            ('BRANCH_OP', 'B((LT)|(LE)|(GT)|(GE)|(EQ)|(NE))'), # matches branch operators: BLT, BLE, BGT, BGE, BEQ, BNE
            ('JUMP_OP', '^JMP$'),
            ('CALL_OP', '^CALL$'),
            ('LT', '<'),
            ('GT', '>'),
            ('EQ', '='),
            ('IDENTIFIER', '[a-zA-Z]+'),
            ('OTHER', '.') # everything else
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)



    pass








def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

