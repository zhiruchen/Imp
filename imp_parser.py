# -*- coding: utf-8 -*-


class Result:
    """
    Result represent the parse result
    """
    def __init__(self, value, pos):
        """
        
        :param value: part of ast
        :param pos: the index of next token in the token stream
        """
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)


class Parser:
    def __call__(self, tokens, pos):
        return None


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] == self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None
