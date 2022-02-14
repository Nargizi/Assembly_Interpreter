from typing import NamedTuple
import re
from ast import *

class Token(NamedTuple):
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

<mem_expr> ::= SP_REG <additive_operator> NUMERIC_LITERAL

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
        statement_list = []
        while self.lookahead.type != 'EOF':
            statement_list.append(self.statement())
        return Program(statement_list)

    #  < statement >: := < load_statement > | < call_statement > | < store_statement > | < jump_statement >

    def statement(self):

        # <load_statement>
        # < load_statement >: := < all_reg > EQ_OP( < alu_expr > | < mem_expr >)
        #
        # < call_statement >: := CALL_OP(LT_OP IDENTIFIER RT_OP | REGISTER)
        #
        # < store_statement >: := MEM LB < alu_expr > RB EQ_OP < numeric_val >
        #
        # < allocate_statement >: := SP_REG EQ_OP( < alu_expr > | < mem_expr >)

        cur_token = self.lookahead

        if cur_token.type == 'CALL_OP':
            self.call_statement()
        elif cur_token.type == 'JUMP_OP':
            self.jump_statement()
        elif cur_token.type == 'MEM':
            self.store_statement()
        elif cur_token.type == 'SP_REG':
            self.allocate_statement()
        else:
            self.load_statement()


    # <call_statement> ::= CALL_OP (LT_OP IDENTIFIER RT_OP | REGISTER)
    def call_statement(self):
        self.eat('CALL_OP')
        if self.lookahead.type == 'LT_OP':
            self.eat('LT_OP')
            token = self.lookahead
            self.eat('IDENTIFIER')
            self.eat('RT_OP')
        else:
            token = self.lookahead
            self.eat('REGISTER')

        return Call(token)

    # < jump_statement >: := JUMP_OP < alu_expr >
    def jump_statement(self):
        self.eat('JUMP_OP')
        dest = self.alu_expr() # dest is either a BinaryOP or UnaryOp, not sure if this is correct
        return Jump(dest)

    # < store_statement >: := MEM LB < alu_expr > RB EQ_OP < numeric_val >

    def store_statement(self):
        self.eat('MEM')
        self.eat('LB')
        address = self.alu_expr()
        self.eat('RB')
        self.eat('EQ_OP')
        value = self.numeric_val()
        node = Store(address, value) # here address is a BinaryOP, where value is
        return node

    # < allocate_statement >: := SP_REG EQ_OP( < alu_expr > | < mem_expr >)

    def allocate_statement(self):
        self.eat("SP_REG")
        self.eat("EQ_OP")
        if self.lookahead.type == "MEM":
            value = self.mem_expr()
            return Allocate(value)
        else:
            return self.alu_expr()

    # <load_statement> ::= (REGISTER | RV_REG) EQ_OP (<alu_expr> | <mem_expr>)

    def load_statement(self):
        token = self.lookahead
        if token.type == 'RV_REG':
            self.eat('RV_REG')
        else:
            self.eat('REGISTER')


    # <alu_expr> ::= <numeric_val> (<alu> <numeric_val>)?

    def alu_expr(self):
        node = self.numeric_val()
        if self.lookahead.type in ('PLUS', 'MINUS', 'MUL', 'DIV'):
            op = self.alu()
            right = self.numeric_val()
            return BinaryOP(node, op, right)
        return node

    # <mem_expr> ::= SP_REG <additive_operator> NUMERIC_LITERAL

    def mem_expr(self):
        self.eat('SP_REG')
        self.additive_operator()
        token = self.lookahead
        self.eat('NUMERIC_LITERAL')
        return token


    # <alu> ::= <additive_operator> | <multiplicative_operator>

    # <numeric_val> ::= < additive_operator >?(< all_reg > | NUMERIC_LITERAL)

    def numeric_val(self):
        op = None
        if self.lookahead.type in ('PLUS', 'MINUS'):
            op = self.lookahead
            self.additive_operator()

        operand = self.lookahead

        if operand.type in ('REGISTER', 'PC_REG', 'SP_REG', 'RV_REG'):
            self.all_reg()
        else:
            self.eat('NUMERIC_LITERAL')

        return UnaryOP(op, operand)



    # <alu> ::= <additive_operator> | <multiplicative_operator>
    def alu(self):
        token = self.lookahead
        self.eat(token.type)
        return token.type

        # if token.type in ('PLUS', 'MINUS'):
        #     self.additive_operator()
        # elif token.type in ('MUL', 'DIV'):
        #     self.multiplicative_operator()

    def additive_operator(self):
        # not sure whether this code is needed, commenting for now.
        # if self.lookahead.type == 'PLUS':
        #     self.eat('PLUS')
        # else:
        #     self.eat('MINUS')

        self.eat(self.lookahead.type)

    def multiplicative_operator(self):
        self.eat(self.lookahead.type)

    # <all_reg> ::= REGISTER | PC_REG | SP_REG | RV_REG

    def all_reg(self):
        token = self.lookahead

        if token.type == 'REGISTER':
            self.eat('REGISTER')
            return Register(token)
        if token.type == 'PC_REG':
            self.eat('PC_REG')
            return PCRegister(token)
        if token.type == 'SP_REG':
            self.eat('SP_REG')
            return SPRegister(token)
        if token.type == 'RV_REG':
            self.eat('RV_REG')
            return RVRegister(token)



# test = '''R123 = 12
#         Mem[R2] = 12
#         R3 = R2
#     ENDIF;
# '''

test = "M[R1 + 4] =.1 R2"

if __name__ == '__main__':
    tokenizer = Tokenizer(test)
    while True:
        token_cur = tokenizer.get_next_token()
        if token_cur.type == "EOF":
            break
        else:
            print("shemovida",  token_cur.type, token_cur.value)


