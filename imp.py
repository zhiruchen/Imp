# -*- coding: utf-8 -*-

import sys

from imp_lexer import *
from imp_parser import *


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        tokens = imp_lex(f.read())
        parse_result = imp_parser(tokens)
        if not parse_result:
            sys.stderr.write("Parse Error\n")
            sys.exit(1)

        ast = parse_result.value
        env = dict()
        ast.eval(env)

        sys.stdout.write("Final variable values: \n")
        for name in env:
            sys.stdout.write("{}: {}\n".format(name, env[name]))
