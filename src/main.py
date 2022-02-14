import argparse
from utils import read_file
from tokenizer import Tokenizer
parser = argparse.ArgumentParser(description='Interpret *name of the programming language* src code')
parser.add_argument('-f', '--file', required=True, help='path to the src code')
args = parser.parse_args()


def main():
    tokenizer = Tokenizer(read_file(args.file))


if __name__ == '__main__':
    main()

