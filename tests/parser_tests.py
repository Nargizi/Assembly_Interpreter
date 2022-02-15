from ast import *
from tokenizer import *

# import unittest


class LispTranslator(NodeVisitor):
    def visit_BinaryOP(self, node: BinaryOP):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op.value
        return f'({op} {left} {right})'


    def visit_Num(self, node: Num):
        return node.token.value

    def visit_Register(self, node: Register):
        return node.token.value

    def visit_RVRegister(self, node: RVRegister):
        return node.token.value

    def visit_PCRegister(self, node: PCRegister):
        return node.token.value

    def visit_SPRegister(self, node: SPRegister):
        return node.token.value

    def visit_Function(self, node: Function):
        return node.token.value

    def visit_Load(self, node: Load):
        address = self.visit(node.address)
        return f'([] M {address})'

    def visit_Allocate(self, node: Allocate):
        size = self.visit(node.size)
        return f'(= SP {size})'

    def visit_UnaryOP(self, node: UnaryOP):
        operand = self.visit(node.operand)
        if node.op is not None:
            op = node.op.value
            return f'({op} {operand})'
        else:
            return operand

    def visit_Store(self, node: Store):
        address = self.visit(node.address)
        value = self.visit(node.value)
        prc = node.prc
        if prc is not None:
            prc = self.visit(prc)
            return f'(=.{prc} ({address} {value}))'
        return f'(= ({address} {value}))'


    def visit_Assignment(self, node: Assignment):
        var = self.visit(node.var)
        value = self.visit(node.value)
        prc = node.prc
        if prc is not None:
            prc = self.visit(prc)
            return f'(=.{prc} ({var} {value}))'
        return f'(= ({var} {value}))'

    def visit_Branch(self, node: Branch):
        type = self.visit(node.type)
        left = self.visit(node.left)
        right = self.visit(node.right)
        dest = self.visit(node.dest)

        return f'({type.value} {left} {right} {dest})'

    def visit_Jump(self, node: Jump):
        dest = self.visit(node.dest)
        return f'(JMP {dest})'

    def visit_Call(self, node: Call):
        callee = self.visit(node.callee)
        return f'CALL {callee}'


if __name__ == '__main__':
    bop = BinaryOP(Num(Token('NUMERIC_LITERAL', '2', 0, 0)), Token('PLUS', '+', 0, 0),
                    Num(Token('NUMERIC_LITERAL', '1', 0, 0)))
    # ast = BinaryOP(ast, Token('MUL', '*', 0, 0), ast)
    register = Register(Token('REGISTER', 'R129', 0, 0))
    uop = UnaryOP(None, register)
    ast = Store(Load(uop), bop, Num(Token('NUMERIC_LITERAL', '1', 0, 0)))

    func = Function(Token('IDENTIFIER', 'gioyletardia :D'), 0, 0)




    translator = LispTranslator()
    print(translator.visit(ast))


# if __name__ == '__main__':
    # unittest.main()
