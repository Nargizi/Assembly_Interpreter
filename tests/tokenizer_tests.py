import unittest
from src.tokenizer import Tokenizer
from src import utils
import os
BASE_PATH = 'files/tokenizer'


def get_path(file_name):
    return os.path.join(BASE_PATH, file_name)


class TokenizerTestCase(unittest.TestCase):
    def test_all_tokens(self):
        self.__compare(get_path('test0.txt'), get_path('answ0.txt'))

    def test_simple_program(self):
        self.__compare(get_path('test1.txt'), get_path('answ1.txt'))

    def __compare(self, test, answers):
        tokenizer = Tokenizer(utils.read_file(test))
        for answer in utils.read_file(answers):
            token = tokenizer.get_next_token()
            self.assertEqual(answer.rstrip(), token.type)



if __name__ == '__main__':
    unittest.main()
