# -*- coding: utf-8 -*-

"""
ref: http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
"""

import sys
import re


def lex(chars, token_exprs):
    """
    词法解析
    :param chars: 
    :param token_exprs: 
    :return: 
    """
    tokens = []
    pos = 0

    while pos < len(chars):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)  # 编译模式为正则对象
            match = regex.match(chars, pos)  # 从pos开始匹配

            if match:
                text = match.group(0)  # The entire match
                if tag:
                    tokens.append((text, tag))
                break

        if not match:
            sys.stderr.write("Illegal character %s\n" % chars[pos])
            sys.exit(1)
        else:
            pos = match.end(0)  # 返回匹配的子串的最后索引

    return tokens
