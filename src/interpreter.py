from ast import *

REGISTER_SIZE = 4
LINE_SIZE = 4


class JumpError(Exception):
    def __init__(self, dest):
        self.dest = dest


class Memory(bytearray):
    def change_size(self, size):
        length = len(self)
        if length > size:
            del self[size:]
        elif length < size:
            self.extend(bytearray(size-length))

    @staticmethod
    def __byte_length(i):
        return (i.bit_length() + 7) // 8

    def store_value(self, value: int, start=0, size=4):
        binary_rep = value.to_bytes(max(self.__byte_length(value), size), byteorder='little', signed=True)
        binary_rep = binary_rep[:size]
        self[start: start + size] = binary_rep

    def get_bytes(self, start=0, size=4):
        if start >= len(self):
            raise Exception
        return self[start: start + size]

    def get_value(self, start=0, size=4):
        if start >= len(self):
            raise Exception
        fragment = self[start: start + size]
        print(fragment)
        return int.from_bytes(fragment, byteorder='little', signed=True)


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.registers = {'SP': Memory(REGISTER_SIZE), 'PC': Memory(REGISTER_SIZE)}
        self.stack = Memory()
        self.function_def = [FunctionBuiltIn(print, 4)]
        self.function_decl = {'print', 0}
        self.parser = parser

    def __error(self, msg=''):
        raise Exception(msg)

    def __create_register(self, name, mem=4):
        self.registers[name] = Memory(mem)

    def __get_value_from_register(self, name, prc=4):
        try:
            register: Memory = self.registers[name]
            return register.get_value(0, prc)
        except KeyError:
            self.__error()

    def __store_value_in_registers(self, name, value, prc=4):
        register: Memory = self.registers.setdefault(name, Memory(REGISTER_SIZE))
        register.store_value(value, 0, prc)

    def visit_FunctionBuiltIn(self, node: FunctionBuiltIn):
        arg = self.stack.get_value(self.__get_value_from_register('SP') - node.args_length, node.args_length)
        rv = node.func(arg)
        if rv is not None:
            self.__store_value_in_registers('RV', rv)

    def visit_Num(self, node: Num):
        try:
            return int(node.token.value)
        except ValueError:
            self.__error()

    def visit_Register(self, node: Register):
        register_name = node.token.value
        return self.__get_value_from_register(register_name)

    def visit_RVRegister(self, node: RVRegister):
        register_name = node.token.value
        return self.__get_value_from_register(register_name)

    def visit_SPRegister(self, node: SPRegister):
        register_name = node.token.value
        return self.__get_value_from_register(register_name)

    def visit_PCRegister(self, node: PCRegister):
        register_name = node.token.value
        return self.__get_value_from_register(register_name)

    def visit_Function(self, node: Function):
        try:
            return self.function_decl[node.token.value]
        except KeyError:
            self.__error()

    def visit_Return(self, node: Return):
        pass

    def visit_Allocate(self, node: Allocate):
        size = self.visit(node.size)
        self.__store_value_in_registers('SP', size)
        self.stack.change_size(size)

    def visit_Store(self, node: Store):
        address = self.visit(node.address)
        value = self.visit(node.value)
        if node.prc is None:
            prc = 4
        else:
            prc = self.visit(node.prc)
        self.stack.store_value(value, address, prc)

    def visit_Load(self, node: Load):
        address = self.visit(node.address)
        return self.stack.get_value(address)

    def visit_Assignment(self, node: Assignment):
        register = node.var.token.value
        value = self.visit(node.value)
        if node.prc is None:
            prc = 4
        else:
            prc = self.visit(node.prc)
        self.__store_value_in_registers(register, value, prc)

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

    def visit_Call(self, node: Call):
        address = self.visit(node.callee)
        try:
            self.visit(self.function_def[address])
        except ValueError:
            self.__error()

    def visit_Jump(self, node: Jump):
        dest = self.visit(node.dest) // LINE_SIZE  # convert byte value to line num
        raise JumpError(dest)

    def visit_Branch(self, node: Branch):
        left = self.visit(node.left)
        right = self.visit(node.right)
        dest = self.visit(node.dest) // LINE_SIZE
        type_ = node.type.type
        if type_ == 'BEQ':
            cond = left == right
        elif type_ == 'BGT':
            cond = left > right
        elif type_ == 'BLT':
            cond = left < right
        elif type_ == 'BGE':
            cond = left >= right
        elif type_ == 'BLE':
            cond = left <= right
        if cond:
            raise JumpError(dest)

    def visit_Program(self, node: Program):
        i = 0
        while i != len(node.statements):
            self.registers['PC'].store_value(i * LINE_SIZE)
            statement = node.statements[i]
            try:
                self.visit(statement)
                i += 1
            except JumpError as j:
                i = j.dest

    def interpret(self):
        ast_ = self.parser.parse()
        self.visit(ast_)


if __name__ == '__main__':
    pass
    # ast = BinaryOP(Num(Token('NUMERIC_LITERAL', '2', 0, 0)), Token('PLUS', '+', 0, 0),
    #                Num(Token('NUMERIC_LITERAL', '1', 0, 0)))
    # ast = BinaryOP(ast, Token('MUL', '*', 0, 0), ast)
    # translator = LispTranslator()
    # print(translator.visit(ast))


