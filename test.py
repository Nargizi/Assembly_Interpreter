from typing import NamedTuple
import re



# def tokenize(code):
#     keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
#     token_specification = [
#         ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
#         ('ASSIGN',   r':='),           # Assignment operator
#         ('END',      r';'),            # Statement terminator
#         ('ID',       r'[A-Za-z]+'),    # Identifiers
#         ('OP',       r'[+\-*/]'),      # Arithmetic operators
#         ('NEWLINE',  r'\n'),           # Line endings
#         ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
#         ('MISMATCH', r'.'),            # Any other character
#     ]
#     tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
#     print("regex: ", tok_regex)
#     line_num = 1
#     line_start = 0
#     for matched_object in re.finditer(tok_regex, code):
#         print("mo: ", matched_object)
#         kind = matched_object.lastgroup
#         print("kind: ", kind)
#         value = matched_object.group()
#         print("value: ", value)
#         column = matched_object.start() - line_start
#         if kind == 'NUMBER':
#             value = float(value) if '.' in value else int(value)
#         elif kind == 'ID' and value in keywords:
#             kind = value
#         elif kind == 'NEWLINE':
#             line_start = matched_object.end()
#             line_num += 1
#             continue
#         elif kind == 'SKIP':
#             continue
#         elif kind == 'MISMATCH':
#             raise RuntimeError(f'{value!r} unexpected on line {line_num}')
#         yield Token(kind, value, line_num, column)
#
# statements = ''' 15
#     IF quantity THEN
#         total := total + price * quantity;
#         tax := price * 0.05;
#     ENDIF;
# '''

# if __name__ == '__main__':
#     for token in tokenize(statements):
#         print(token)



class Token(NamedTuple):
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
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
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
            ('INT_CAST', '\.\d'), # change the name to something better, matches .1, .2 ...
            ('ARITHM_OP', '[\-\+\*\/]'),
            ('BRANCH_OP', 'B(LT|LE|GT|GE|EQ|NE)'),  # matches branch operators: BLT, BLE, BGT, BGE, BEQ, BNE
            ('JUMP_OP', '^JMP\b'), # not sure if this is correct
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

''' Grammar Rules:

<program> ::= <statement>*

----------- Statement types -----------
<statement> ::= <load_statement> | <call_statement> | <store_statement> | <jump_statement>

<load_statement> ::= <all_reg> EQ_OP (<alu_expr> | <mem_expr>)

<call_statement> ::= CALL_OP (LT_OP IDENTIFIER RT_OP | REGISTER)

<store_statement> ::= MEM LB <alu_expr> RB EQ_OP <numeric_val>

<jump_statement> ::= JUMP_OP <alu_expr>

// Examples:
// BEQ R1, 0, 344
// BLT R2, R3, PC + 8

<BRANCH_STATEMENT> ::=  BRANCH_OP <numeric_val> COMMA <numeric_val> COMMA <alu_expr>
---------------------------------------

<all_reg> ::= REGISTER | PC_REG | SP_REG | RV_REG

<alu_expr> ::= <numeric_val> (<alu> <numeric_val>)?

<additive_operator> ::= PLUS | MINUS

<multiplicative_operator> ::= MUL | DIV

<numeric_val> ::= <additive_operator>?(<all_reg> | NUMERIC_LITERAL)

<alu> ::= <additive_operator> | <multiplicative_operator>
'''

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = l

    lexer: Tokenizer

    def eat(self, token_type):


        pass





    pass




# test = '''R123 = 12
#         Mem[R2] = 12
#         R3 = R2
#     ENDIF;
# '''

test = "M[R1 + 4] =.1 R2"

if __name__ == '__main__':
    tokenizer = Tokenizer(test)
    while(True):
        token = tokenizer.get_next_token()
        if token.type == "EOF":
            break
        else:
            print("shemovida",  token.type, token.value)


