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


class Parser(object):
    def __add__(self, other):
        """parser + other"""
        return Concat(self, other)

    def __mul__(self, other):
        """parser * other"""
        return Exp(self, other)

    def __or__(self, other):
        """parser | other"""
        return Alternate(self, other)

    def __xor__(self, func):
        """parser ^ function"""
        return Process(self, func)


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

    def __repr__(self):
        return "Reserved({},{})".format(self.value, self.tag)


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

    def __repr__(self):
        return "Tag({})".format(self.tag)


class Concat(Parser):
    """the Concat combinator take two parser as input
    first apply left parser, followed by right parser.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None

    def __repr__(self):
        return "Concat({},{})".format(self.left, self.right)


class Alternate(Parser):
    """应用左边的parser, 如果失败应用右边的Parser返回它的结果
    Alternate is useful for choosing among several possible parsers
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result

    def __repr__(self):
        return "Alternate({},{})".format(self.left, self.right)


class Opt(Parser):
    """Opt is useful for optional text"""
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return Result(None, pos)


class Rep(Parser):
    """Rep applies its input parser repeatedly until it fails"""
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)

        return Result(results, pos)


class Process(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.func(result.value)
            return result
    
    def __repr__(self):
        return "Process({},{})".format(self.parser, self.func.__name__)

class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()

        return self.parser(tokens, pos)

    def __repr__(self):
        return "Lazy({})".format(self.parser_func.__name__)


class Phrase(Parser):
    """the top level parser for IMP"""
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None


class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)

        next_parser = self.separator + self.parser ^ process_next
        next_result = result

        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result
    
    def __repr__(self):
        return "Exp({},{})".format(self.parser, self.separator)
