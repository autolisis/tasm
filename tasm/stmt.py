#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from enum import Enum, auto


class stmt:
    class Statement:
        def __init__(self, **kwargs):
            self.lineno = kwargs['lineno']

        def __repr__(self):
            items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
            return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

        def __eq__(self, other):
            if type(other) is type(self):
                return self.__dict__ == other.__dict__
            return False

    class Accept(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Reject(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Write(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sym = kwargs['sym']

    # class Direction(Enum):
    #     left = auto()
    #     right = auto()
    # class Move(Statement):
    #     def __init__(self, direction):
    #         self.direction = direction

    class Left(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Right(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Jump(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.destlabel = kwargs['destlabel']

    class IFR(Statement):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sym = kwargs['sym']
            self.destlabel = kwargs['destlabel']

    statements = {
        'acc': Accept,
        'rej': Reject,
        'wr': Write,
        'goto': Jump,
        'left': Left,
        'right': Right,
        'ifr': IFR
    }

    def new(**kwargs):
        return stmt.statements.get(kwargs['stmt'])(**kwargs)
