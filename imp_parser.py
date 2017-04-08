# -*- coding: utf-8 -*-

"""
imp parser
ref: http://jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3
"""

from comb import *
from imp_ast import *
from imp_lexer import *


# Primitive Parser
def key_word(kw):
    """关键字parser"""
    return Reserved(kw, RESERVED)

# id parser: 匹配变量名
id = Tag(ID)

# num: 匹配整数
num = Tag(INT) ^ (lambda i: int(i))

# parser arithmetic expressions
# convert values returned by num and id into actual expressions
# first try to parse an integer expression, if fails, then to parse a var expression
def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | (id ^ (lambda v: VarExp(v)))

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def aexp_group():
    return key_word('(') + Lazy(aexp) + key_word(')') ^ process_group

def aexp_term():
    return aexp_value() | aexp_group()

# 操作符优先级
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

