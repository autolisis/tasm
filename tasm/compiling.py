#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import tasm.parsing
from tasm.parsing import getLexer, getParser

from tasm.tm import TM
from functools import reduce
import operator

def helpParse(code):
    return p.parse(code, tracking=True, lexer=self.lexer)


class Compiler:
    def __init__(self):
        self.parser = getParser()
        tasm.parsing.reset()
        self.lexer = getLexer()

    def parse(self, code):
        return self.parser.parse(code, tracking=True, lexer=self.lexer)

    def getSymbols(self, parsed):
        syms = set()
        for st in parsed['statements']:
            try:
                syms.add(st.sym)
            except AttributeError:
                pass
        parsed['symbols'] = list(syms)
        return parsed

    def resolveLabels(self, parsed):
        for st in parsed['statements']:
            try:
                destlineno = parsed['labels'][st.destlabel]
                st.destlineno = destlineno
            except AttributeError:
                pass
            except KeyError:
                parsed['error'] = True
        return parsed

    def getLines(self, parsed):
        parsed['lines'] = {}
        l = parsed['lines']
        for st in parsed['statements']:
            l[st.lineno] = st
        return parsed

    def compile(self, code):
        parsed = self.parse(code)
        parsed = self.getSymbols(parsed)
        parsed = self.resolveLabels(parsed)
        parsed = self.getLines(parsed)
        # reduce(operator.add, parsed['lines'].values(), TM())
        t = TM()
        for (lineno, statement) in parsed['lines'].items():
            __import__('pdb').set_trace()
            t += statement
            global b
            b = b + 1 if b < 100 else breakpoint()
        return t
