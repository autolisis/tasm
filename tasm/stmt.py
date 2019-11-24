#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from enum import Enum, auto


def st():
    global TM
    from tasm.tm import TM
    TM = TM


class stmt:
    class Statement:
        def __init__(self, **kwargs):
            st()
            self.lineno = kwargs['lineno']

        def __repr__(self):
            items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
            return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

        def __eq__(self, other):
            if type(other) is type(self):
                return self.__dict__ == other.__dict__
            return False

        def tm(self, tok='init'):
            return TM(initialState=f'{tok}{self.lineno}',
                      states=['accept', f'{tok}{self.lineno}'])

    class Accept(Statement):
        tok = 'acc'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def tm(self):
            tm = super().tm(self.tok)
            tm.addTransition({'newState': 'accept', 'moveDirection': 'R'})
            return tm

    class Reject(Statement):
        tok = 'rej'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Write(Statement):
        tok = 'wr'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sym = kwargs['sym']

    class Left(Statement):
        tok = 'left'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Right(Statement):
        tok = 'right'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    class Jump(Statement):
        tok = 'goto'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.destlabel = kwargs['destlabel']

    class IFR(Statement):
        tok = 'ifr'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sym = kwargs['sym']
            self.destlabel = kwargs['destlabel']

    statements = {
        c.tok: c
        for c in [Accept, Reject, Write, Jump, Left, Right, IFR]
    }

    @classmethod
    def new(cls, **kwargs):
        return stmt.statements.get(kwargs['stmt'], cls)(**kwargs)
