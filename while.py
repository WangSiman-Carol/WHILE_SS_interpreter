#!/usr/bin/env python3
# Reference: Lark, an open source parser.
# https://github.com/lark-parser/lark

import sys
from lark import Lark
from interpreter import *

def main():
    try:
        text = "x := 1\n"
        text = "while x = 0 do x := 3\n"
        text = "x := 1 * 9 ; if 5 < x then x := 2 - 2 else y := 9\n"
        text = "if x = 0 ∧ 4 < 4 then x := 1 else x := 3\n"
        text = "if 0 < x ∧ 4 = 4 then x := 1 else x := 3\n"
        text = "while ¬ true do x := 1\n"
        text = "z := 26 ; { a := 1 ; b := 2 ; c := 3 }\n"
        text = "x := 1 * 9 ; if 5 < x then x := 2 - 2 else y := 9\n"
        # text = "if true then x := 1 else x := 0\n"
        # text = "if ( 1 - 1 ) < 0 then z8 := 09 else z3 := 90\n"
        while_parser = Lark.open('WHILE.lark', parser='lalr')
        # print(while_parser.parse(text))
        interpreter = Interpreter(while_parser)
        result = interpreter.interpret(text)
        # print(result, flush=True) 
        # for text in sys.stdin:
        #         while_parser = Lark.open('WHILE.lark', parser='lalr')
        #         print(while_parser.parse(text))
        #         interpreter = Interpreter(while_parser)
        #         result = interpreter.interpret(text)
        #         print(result, flush=True)              
    except OSError as err:
        print("OS error: {0}".format(err))
    except EOFError:
        print("EOF error.")
        raise

if __name__ == '__main__':
    main()
