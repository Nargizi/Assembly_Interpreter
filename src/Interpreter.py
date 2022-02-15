from ast import *
import struct

class Stack(bytearray):
    def change_size(self, size):
        length = len(self)
        if length > size:
            del self[size:]
        elif length < size:
            self.extend(bytearray(size-length))

    def store_value(self, start, value: int, size=4):
        self[start: start + size] = value.to_bytes(size ,byteorder='little')

    def get_value(self, start, size=4):
        return

class Interpreter(NodeVisitor):
    def __init__(self):
        self.registers = {'SP': 0, 'PC': 0}

    def __error(self, msg=''):
        raise Exception(msg)

    def visit_Num(self, node: Num):
        try:
            return int(node.token.value)
        except ValueError:
            self.__error()

    def visit_Register(self, node: Register):
        register_name = node.token.value
        try:
            return self.registers[register_name]
        except KeyError:
            self.__error()

    def visit_RVRegister(self, node: RVRegister):
        try:
            return self.registers[node.token.value]
        except KeyError:
            self.__error()

    def visit_SPRegister(self, node: SPRegister):
        return self.registers[node.token.value]

    def visit_PCRegister(self, node: PCRegister):
        return self.registers[node.token.value]

    def visit_Allocate(self, node: Allocate):
        self.registers['SP'] = self.visit(node.size)


    def visit_UnaryOP(self, node: UnaryOP):
        operand = self.visit(node.operand)
        if node.op is None:
            return operand
        if node.op.type == 'MINUS':
            return -operand
        if node.op.type == 'PLUS':
            return operand
        self.__error()

    def visit_BinaryOP(self, node: BinaryOP):
        left = self.visit(node.left)
        right = self.visit(node.right)
        try:
            if node.op.type == 'PLUS':
                return left + right
            if node.op.type == 'MINUS':
                return left - right
            if node.op.type == 'MUL':
                return left * right
            if node.op.type == 'DIV':
                return left / right
        except ValueError:
            self.__error()
        self.__error()


