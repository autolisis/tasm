#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from enum import Enum, auto
from tasm.tm import TM


def Transition(**kwargs):
    return kwargs


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
        tok = 'acc'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def getTM(self, parsed):
            init = f'{self.tok}{self.lineno}'
            return TM(
                initialState=init,
                states=[init, 'accept'],
                transitions=[
                    Transition(
                        oldState=init,
                        readLetter='*',
                        newState='accept',
                        newLetter='*',
                        moveDirection='R',
                    ),
                ],
            )

    class Reject(Statement):
        tok = 'rej'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def getTM(self):
            init = f'{self.tok}{self.lineno}'
            return TM(
                initialState=init,
                states=[init],
                transitions=[],
            )

    class Write(Statement):
        tok = 'wr'

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sym = kwargs['sym']

        def getTM(self):
            init = f'{self.tok}{self.lineno}'
            tmp = init + '@' + '1'
            end = init + '$'
            return TM(
                initialState=init,
                states=[init, tmp, end],
                transitions=[
                    Transition(
                        oldState=init,
                        readLetter='*',
                        newState=tmp,
                        newLetter=self.sym,
                        moveDirection='R',
                    ),
                    Transition(
                        oldState=tmp,
                        readLetter='*',
                        newState=end,
                        newLetter='*',
                        moveDirection='L',
                    ),
                ],
            )

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
