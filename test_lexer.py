# -*- coding: utf-8 -*-

import sys
from imp_lexer import imp_lex


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        chars = f.read()

        tokens = imp_lex(chars)
        for token in tokens:
            print token
