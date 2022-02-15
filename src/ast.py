class AST:
    pass


class Program(AST):
    def __init__(self, statements):
        self.statements = statements


class Call(AST):
    """
    callee - function to be called
    Example:
        CALL <print> (print == callee)
    """
    def __init__(self, callee: 'IDENTIFIER | REGISTER'):
        self.callee = callee


class Jump(AST):
    """
    dest - destination of jump
    Example:
        JMP PC - 4 (PC - 4 == dest)
    """
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
    """
    size - size of stack
    Example:
        SP = SP - 4  (SP - 4 == size)
    """
    def __init__(self, size):
        self.size = size


class UnaryOP(AST):
    """
    op - unary operator token
    operand - operand token
    """
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class Store(AST):
    """
    address - address of memory block where value is to be stored
    value - value
    prc - (optional) number of bytes to be copied
    Example:
        (M[R4] = 12) - (R4 == address, 12 == value)
        (M[12] =.2 R1) - (12 == address, R1 == value, .2 == prc)
    """
    def __init__(self, address, value, prc=None):
        self.address = address
        self.value = value
        self.prc = prc


class Load(AST):
    """
    address - address of memory block to be loaded
    Example:
        M[12] (12 == address)
        M[R3 + 4] (R3 + 4 == address)
    """
    def __init__(self, address):
        self.address = address


class Assignment(AST):
    """
    var - left-hand side variable
    value - value
    prc - (optional) number of bytes to be stored
    Example:
        (R2 = R3 + 4) - (var = value)
        (R1 =.2 10) - (var =prc value)
    """
    def __init__(self, var, value, prc):
        self.var = var
        self.value = value
        self.prc = prc


class Branch(AST):
    """
    type_ - type of branch
    left - left operand
    right - right operand
    dest - destination of jump
    Example:
        (BGT, 12, R2, PC + 15) - (type_ left, right, dest)
    """
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
