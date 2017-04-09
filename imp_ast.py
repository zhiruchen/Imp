# -*- coding: utf-8 -*-

"""
classes represent syntactic element of Imp
ref: http://jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3
"""

from equality import Equality


class Aexp(Equality):
    """算术表达式基础类"""
    pass


class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return self.i

    def __repr__(self):
        return 'IntAexp({})'.format(self.i)


class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env.get(self.name, 0)

    def __repr__(self):
        return 'VarExp({})'.format(self.name)


class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            return left_value + right_value
        elif self.op == '-':
            return left_value - right_value
        elif self.op == '*':
            return left_value * right_value
        elif self.op == '/':
            return left_value / right_value
        else:
            raise RuntimeError("unsupported operator: {}".format(self.op))

    def __repr__(self):
        return "BinopExp({0}, {1}, {2})".format(self.op, self.left, self.right)


class Bexp(Equality):
    """布尔表达式"""
    pass

class RelopBexp(Bexp):
    """关系表达式"""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)

        if self.op == '<':
            return left_value < right_value
        elif self.op == '<=':
            return left_value <= right_value
        elif self.op == '>':
            return left_value > right_value
        elif self.op == '>=':
            return left_value >= right_value
        elif self.op == '=':
            return left_value == right_value
        elif self.op == '!=':
            return left_value != right_value
        else:
            raise RuntimeError("unsupported operator: {}".format(self.op))

    def __repr__(self):
        return "BinopExp({0}, {1}, {2})".format(self.op, self.left, self.right)


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)

    def __repr__(self):
        return "AndBexp({0}, {1})".format(self.left, self.right)


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)

    def __repr__(self):
        return "OrBexp({0}, {1})".format(self.left, self.right)


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp
    
    def eval(self, env):
        return not self.exp.eval(env)

    def __repr__(self):
        return 'NotBexp({})'.format(self.exp)


class Statement(Equality):
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp
    
    def eval(self, env):
        env[self.name] = self.aexp.eval(env)

    def __repr__(self):
        return 'AssignStatement({},{})'.format(self.name, self.aexp)


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

    def __repr__(self):
        return 'CompoundStatement({},{})'.format(self.first, self.second)


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)

    def __repr__(self):
        return 'IfStatement({},{},{})'.format(self.condition, self.true_stmt, self.false_stmt)


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)

    def __repr__(self):
        return 'WhileStatement({},{})'.format(self.condition, self.body)
