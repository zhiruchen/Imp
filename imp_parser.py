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
    return (num ^ (lambda i: IntAexp(i))) | (id ^ (lambda v: VarAexp(v)))

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

def any_operator_in_list(ops):
    """
    ops: 保留字字符串列表
    return: 能匹配其中任意一个的parser
    """
    op_parsres = [key_word(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsres)
    return parser

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

def precedence(value_parser, precedence_levels, combine):
    """
    value_parser: 读取表达式基本的组成(数字，变量，组合)的parser, aexp_term
    precedence_levels: 操作符列表的列表, aexp_precedence_levels
    combine: process_binop
    """
    def op_parser(precedence_level):
        """读取precedence_level中的所有字符， 返回一个组合两个表达式的函数"""
        return any_operator_in_list(precedence_level) ^ combine
    
    # print precedence_levels[0]
    parser = value_parser * op_parser(precedence_levels[0])
    # print parser

    for precedence_level in precedence_levels[1:]:
        # print precedence_level
        parser = parser * op_parser(precedence_level)
    
    print parser
    return parser

def aexp():
    print "calling aexp"
    print aexp_precedence_levels
    return precedence(aexp_term(), aexp_precedence_levels, process_binop)

#------------------parsing boolean expression--------------------
def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def bexp_relop():
    """parse two arithmetic expression separated by relational operator"""
    relops = ["<", "<=", ">", ">=", "=", "!="]
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_not():
    return key_word('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_group():
    return key_word('(') + Lazy(bexp) + key_word(')') ^ process_group

def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group()

bexp_precedence_levels = [['and'], ['or']]

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        RuntimeError("Unknown logic operator: " + op)

def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)

# ---------------parsing statement---------------------

def assign_stmt():
    """解析赋值语句"""
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)

    return id + key_word(':=') + aexp() ^ process

def stmt_list():
    separator = key_word(";") ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)

def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None

        return IfStatement(condition, true_stmt, false_stmt)

    return key_word("if") + bexp() + \
           key_word("then") + Lazy(stmt_list) + \
           Opt(key_word("else") + Lazy(stmt_list)) + \
           key_word("end") ^ process

def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)

    return key_word("while") + bexp() + \
           key_word("do") + Lazy(stmt_list) + \
           key_word("end") + process

def stmt():
    return assign_stmt() | if_stmt() | while_stmt()

# ------------top level definitions--------------
def parser():
    return Phrase(stmt_list())

def imp_parser(tokens):
    ast = parser()(tokens, 0)
    return ast