class AST:
    pass


class Program(AST):
    def __init__(self, statements):
        self.statements = statements


class Call(AST):
    def __init__(self, callee):
        self.callee = callee


class Jump(AST):
    def __init__(self, dest):
        self.dest = dest


class BinaryOP(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token


class Register(AST):
    def __init__(self, token):
        self.token = token


class RVRegister(AST):
    def __init__(self, token):
        self.token = token


class PCRegister(AST):
    def __init__(self, token):
        self.token = token


class SPRegister(AST):
    def __init__(self, token):
        self.token = token


class Allocate(AST):
    def __init__(self, value):
        self.value = value


class UnaryOP(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Store(AST):
    def __init__(self, address, value):
        self.address = address
        self.value = value


class Load(AST):
    def __init__(self, address):
        self.address = address


class Assignment(AST):
    def __init__(self, var, value):
        self.var = var
        self.value = value


class Branch(AST):
    def __init__(self, type_, left, right, dest):
        self.type = type_
        self.left = left
        self.right = right
        self.dest = dest


class NodeVisitor:
    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass
