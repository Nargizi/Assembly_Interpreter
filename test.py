from typing import NamedTuple
import re

class Token(NamedTuple):
    def __init__(self, type, value):
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
<statement> ::= <load_statement> | <call_statement> | <store_statement> | <jump_statement> | <allocate_statement>

<load_statement> ::= (REGISTER | RV_REG) EQ_OP (<alu_expr> | <mem_expr>)

<allocate_statement> ::= SP_REG EQ_OP (<alu_expr> | <mem_expr>)

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
    def __init__(self, lexer: Tokenizer):
        self.lexer = lexer
        self.lookahead = lexer.get_next_token()

    def eat(self, token_type):
        if token_type == self.lookahead:
            self.lookahead = self.lexer.get_next_token()
        else:
            raise RuntimeError("Something's sus")


    def Program(self):
        while self.lookahead.type != 'EOF':
            self.statement()

    #  < statement >: := < load_statement > | < call_statement > | < store_statement > | < jump_statement >

    def statement(self):

        # R1 = M[R2]

        # <load_statement>

        # < load_statement >: := < all_reg > EQ_OP( < alu_expr > | < mem_expr >)
        #
        # < call_statement >: := CALL_OP(LT_OP IDENTIFIER RT_OP | REGISTER)
        #
        # < store_statement >: := MEM LB < alu_expr > RB EQ_OP < numeric_val >
        #


        cur_token = self.lookahead

        if cur_token.type == 'CALL_OP':
            self.call_statement()
        elif cur_token.type == 'JUMP_OP':
            self.jump_statement()
        elif cur_token.type == 'MEM':
            self.store_statement()
        else:
            self.load_statement()


    def call_statement(self):
        self.eat('CALL_OP')
        if self.lookahead.type == 'LT_OP':
            self.eat('LT_OP')
            self.eat('IDENTIFIER')
            self.eat('RT_OP')
        else:
            self.eat('REGISTER')

    # < jump_statement >: := JUMP_OP < alu_expr >

    def jump_statement(self):
        self.eat('JUMP_OP')
        self.alu_expr()


    def store_statement(self):
        pass

    def load_statement(self):
        pass


    def alu_expr(self):
        self.numeric_val()



    def numeric_val(self):
        if self.lookahead.type in ('PLUS', 'MINUS'):
            self.additive_operator()
        if self.lookahead.type in ('REGISTER', 'PC_REG', 'SP_REG', 'RV_REG'):
            self.all_reg()
        else:
            self.eat('NUMERIC_LITERAL')


     #   < numeric_val >: := < additive_operator >?(< all_reg > | NUMERIC_LITERAL)

    def additive_operator(self):
        if self.lookahead.type == 'PLUS':
            self.eat('PLUS')
        else:
            self.eat('MINUS')

    # <all_reg> ::= REGISTER | PC_REG | SP_REG | RV_REG

    def all_reg(self):
        if self.lookahead.type == 'REGISTER':
            self.eat('REGISTER')
        self.eat(self.lookahead.type)





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


