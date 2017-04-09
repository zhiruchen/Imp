# -*- coding: utf-8 -*-

import sys

from imp_parser import *

def test_imp_parser(chars):
    tokens = imp_lex(chars)
    print tokens
    parser = aexp()
    result = parser(tokens, 0)
    print result


if __name__ == '__main__':
    # file_name = sys.argv[1]
    # with open(file_name, 'r') as f:
    #     test_imp_parser(f.read())
    test_imp_parser('1+2*3')
