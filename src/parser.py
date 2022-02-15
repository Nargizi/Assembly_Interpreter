from ast import *
from tokenizer import Tokenizer


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

    def statement(self):

        token = self.lookahead

        if token.type == 'CALL_OP':
            return self.call_statement()
        elif token.type == 'JUMP_OP':
            return self.jump_statement()
        elif token.type == 'MEM':
            return self.store_statement()
        elif token.type == 'SP_REG':
            return self.allocate_statement()
        elif token.type == 'BRANCH_OP':
            return self.branch_statement()
        elif token.type == 'RETURN':
            return self.return_statement()
        else:
            return self.load_statement()


    # <call_statement> ::= CALL_OP (LT IDENTIFIER GT | REGISTER)

    def call_statement(self):
        self.eat('CALL_OP')
        if self.lookahead.type == 'LT':
            self.eat('LT')
            token = self.lookahead
            self.eat('IDENTIFIER')
            self.eat('GT')
        else:
            token = self.lookahead
            self.eat('REGISTER')
            node = Register(token)
            return Call(node)

        return Call(token)

    # <jump_statement> ::= JUMP_OP <alu_expr>
    def jump_statement(self):
        self.eat('JUMP_OP')
        dest = self.alu_expr() # dest is either a BinaryOP or UnaryOp, not sure if this is correct
        return Jump(dest)

    # <store_statement> ::= <numeric_val> EQ BYTE_SIZE? <numeric_val>
    def store_statement(self):
        address = self.numeric_val()
        self.eat('EQ')
        prc = None
        if self.lookahead.type == 'BYTE_SIZE':
            prc = self.lookahead
            self.eat('BYTE_SIZE')

        value = self.numeric_val() # UnaryOP
        node = Store(address, value, prc) # here address is a BinaryOP, where value is
        return node

    # <allocate_statement> ::= SP_REG EQ <expr>
    def allocate_statement(self):
        self.eat("SP_REG")
        self.eat("EQ")
        node = self.expr()
        return Allocate(node)

    # <branch_statement> ::=  BRANCH_OP <numeric_val> COMMA <numeric_val> COMMA <alu_expr>
    def branch_statement(self):
        token = self.lookahead # branch token
        self.eat('BRANCH_OP')
        left = self.numeric_val()
        self.eat('COMMA')
        right = self.numeric_val()
        self.eat('COMMA')
        dest = self.alu_expr()
        return Branch(token, left, right, dest)


    # <return_statement> ::= RETURN
    def return_statement(self):
        token = self.lookahead
        self.eat('RETURN')
        return Return(token)


    # <load_statement> ::= (REGISTER | RV_REG) EQ BYTE_SIZE? (<expr> | <function>)
    def load_statement(self):
        token = self.lookahead
        if token.type in ('REGISTER', 'RV_REG'):
            var = self.all_reg()
        self.eat('EQ')
        prc = None
        if self.lookahead.type == 'BYTE_SIZE':
            prc = self.lookahead
            self.eat('BYTE_SIZE')

        if self.lookahead.type == 'LT':
            value = self.function()
        else:
            value = self.expr()
        return Assignment(var, value, prc)


    # <function> ::= LT IDENTIFIER GT
    def function(self):
        self.eat('LT')
        token = self.lookahead
        self.eat('IDENTIFIER')
        self.eat('GT')
        return Function(token)


    # <alu_expr> ::= <numeric_val> (<alu> <numeric_val>)?
    def alu_expr(self):
        node = self.numeric_val() #
        if self.lookahead.type in ('PLUS', 'MINUS', 'MUL', 'DIV'):
            op = self.alu()
            right = self.numeric_val()
            return BinaryOP(node, op, right)
        return node

    # <mem_expr> ::= MEM LB <alu_expr> RB
    def mem_expr(self):
        self.eat('MEM')
        self.eat('LB')
        node = self.alu_expr()
        self.eat('RB')
        return Load(node)

    # <expr> ::= <alu_expr> | <mem_expr>
    def expr(self):
        if self.lookahead.type == "MEM":
            return self.mem_expr()
        else:
            return self.alu_expr()


    # <numeric_val> ::= (PLUS | MINUS)? (< all_reg > | NUMERIC_LITERAL)
    def numeric_val(self):
        op = None
        if self.lookahead.type in ('PLUS', 'MINUS'):
            op = self.alu()

        token = self.lookahead
        if token.type in ('REGISTER', 'PC_REG', 'SP_REG', 'RV_REG'):
            node = self.all_reg()
        else:
            node = Num(self.lookahead)
            self.eat('NUMERIC_LITERAL')

        return UnaryOP(op, node)


    # <alu> ::= PLUS | MINUS | MUL | DIV
    def alu(self):
        token = self.lookahead
        self.eat(token.type)
        return token.type

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


