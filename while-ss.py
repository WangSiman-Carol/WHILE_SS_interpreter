#!/usr/bin/env python3
# Reference: Lark, an open source parser.
# https://github.com/lark-parser/lark

import sys
from lark import Lark
from interpreter import *

def main():
    try:
        mode = 'dev' # test or dev

        if mode == 'dev':
            text = "i := 5 ; fact := 1 ; while 0 < i do { fact := fact * i ; i := i - 1 }\n"
            while_parser = Lark.open('WHILE.lark', parser='lalr')
            interpreter = Interpreter(while_parser)
            result = interpreter.interpret(text)

        elif mode == 'test':
            for text in sys.stdin:
                    while_parser = Lark.open('WHILE.lark', parser='lalr')
                    interpreter = Interpreter(while_parser)
                    result = interpreter.interpret(text)

    except OSError as err:
        print("OS error: {0}".format(err))
    except EOFError:
        print("EOF error.")
        raise

if __name__ == '__main__':
    main()
