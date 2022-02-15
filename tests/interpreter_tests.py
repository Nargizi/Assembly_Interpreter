import unittest
from src.interpreter import Interpreter, Memory
from src.ast import *
from src.tokenizer import Token


class MockParser:
    def __init__(self, ast_):
        self.ast = ast_

    def parse(self):
        return self.ast


class MyTestCase(unittest.TestCase):
    def __number(self, num):
        return Num(Token('NUMERIC_LITERAL', str(num), 0, 0))

    def __register(self, name):
        return Register(Token('REGISTER', name, 0, 0))

    def __binary_op(self, left, op, right):
        return BinaryOP(left, op, right)

    def __unary_op(self, op, operand):
        return UnaryOP(op, operand)

    def __branch(self, type_, left, right, jump):
        return Branch(Token('BRANCH_OP', type_, 0, 0), left, right, jump)

    def test_memory(self):
        mem = Memory()
        mem.change_size(10)
        self.assertEqual(bytes(10), mem)
        mem.change_size(5)
        self.assertEqual(bytes(5), mem)
        mem.store_value(8, 4, 1)
        self.assertEqual(bytes([0, 0, 0, 0, 8]), mem)
        mem.change_size(4)
        self.assertEqual(bytes(4), mem)
        mem.store_value(256, 0)
        self.assertEqual(bytes([0, 1, 0, 0]), mem)
        self.assertEqual(256, mem.get_value(0))

    def test_memory_negative(self):
        mem = Memory()
        mem.change_size(20)
        mem.store_value(-1, 1, 1)
        self.assertEqual(mem.get_value(1, 1), -1)
        mem.store_value(-250)
        self.assertEqual(mem.get_value(0), -250)

    def test_store_in_memory(self):
        asts = Program([Allocate(self.__number(10)), Store(self.__number(2), self.__number(8))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        answ = Memory(10)
        answ.store_value(8, 2)
        self.assertEqual(interpreter.registers['SP'].get_value(), 10)
        self.assertEqual(answ, interpreter.stack)

    def test_store_in_register(self):
        asts = Program([Assignment(self.__register('R1'), self.__number(4)),
                        Assignment(self.__register('R2'), self.__register('R1'))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(4, interpreter.registers['R1'].get_value(0))
        self.assertEqual(4, interpreter.registers['R2'].get_value(0))

    def test_unary_operators(self):
        asts = Assignment(self.__register('R1'), self.__unary_op(Token('MINUS', '-', 0, 0), self.__number(1)))
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(-1, interpreter.registers['R1'].get_value(0))

    def test_bin_op(self):
        asts = Program([Assignment(self.__register('R1'), self.__binary_op(self.__number(4), Token('PLUS', '+', 0, 0), self.__number(8)))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(12, interpreter.registers['R1'].get_value(0))
        asts = Program([Assignment(self.__register('R1'), self.__number(200)),
                        Assignment(self.__register('R2'), self.__number(8)),
                        Assignment(self.__register('R1'),
                                   self.__binary_op(self.__register('R1'), Token('MUL', '*', 0, 0), self.__register('R2')))])

        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(1600, interpreter.registers['R1'].get_value(0))

    def test_jump(self):
        asts = Program([Assignment(self.__register('R1'), self.__number(200)),
                        Assignment(self.__register('R2'), self.__number(8)),
                        Jump(self.__binary_op(PCRegister(Token('PC_REG', 'PC', 0, 0)), Token('PLUS', '+', 0, 0), self.__number(8))),
                        Assignment(self.__register('R1'),
                                   self.__binary_op(self.__register('R1'), Token('MUL', '*', 0, 0),
                                                    self.__register('R2'))),
                        Assignment(self.__register('R2'), self.__number(16))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(200, interpreter.registers['R1'].get_value(0))
        self.assertEqual(16, interpreter.registers['R2'].get_value(0))

    def test_call(self):
        asts = Program([Allocate(self.__number(10)),
                        Store(self.__number(6), self.__number(8)),
                        Call(Function(Token('IDENTIFIER', 'print', 0, 0)))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.asser

    def test_branch(self):
        asts = Program([Assignment(self.__register('R1'), self.__number(200)),
                        Assignment(self.__register('R2'), self.__number(8)),
                        self.__branch('BGT', self.__register('R2'), self.__register('R1'),
                        self.__binary_op(PCRegister(Token('PC_REG', 'PC', 0, 0)), Token('PLUS', '+', 0, 0), self.__number(8))),
                        Assignment(self.__register('R1'),
                                   self.__binary_op(self.__register('R1'), Token('MUL', '*', 0, 0),
                                                    self.__register('R2'))),
                        Assignment(self.__register('R2'), self.__number(16))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(1600, interpreter.registers['R1'].get_value(0))
        self.assertEqual(16, interpreter.registers['R2'].get_value(0))
        asts = Program([Assignment(self.__register('R1'), self.__number(200)),
                        Assignment(self.__register('R2'), self.__number(8)),
                        self.__branch('BLT', self.__register('R2'), self.__register('R1'),
                                      self.__binary_op(PCRegister(Token('PC_REG', 'PC', 0, 0)),
                                                       Token('PLUS', '+', 0, 0), self.__number(8))),
                        Assignment(self.__register('R1'),
                                   self.__binary_op(self.__register('R1'), Token('MUL', '*', 0, 0),
                                                    self.__register('R2'))),
                        Assignment(self.__register('R2'), self.__number(16))])
        interpreter = Interpreter(MockParser(asts))
        interpreter.interpret()
        self.assertEqual(200, interpreter.registers['R1'].get_value(0))
        self.assertEqual(16, interpreter.registers['R2'].get_value(0))


if __name__ == '__main__':
    unittest.main()
