# -*- coding: utf-8 -*-

import lexer

# TOKEN TYPES
RESERVED = "RESERVED"  # 保留字或操作符
INT = "INT"  # int
ID = "ID"  # 标识符


token_exprs = [
    (r'[ \n\t]+',              None),  # 空白
    (r'#[^\n]*',               None),  # 注释
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'=',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'do',                    RESERVED),
    (r'end',                   RESERVED),
    (r'[0-9]+',                INT),
    (r'[a-zA-Z][_a-zA-Z0-9]*', ID)
]


def imp_lex(chars):
    return lexer.lex(chars, token_exprs)

