#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import tasm.parsing
from tasm.parsing import getLexer, getParser

from tasm.tm import TM
from functools import reduce
import operator

b = 0


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

    def addStatement(self, tm, stmt, parsed):
        newTM = stmt.getTM(parsed=parsed)
        for state in newTM.states:
            tm.addState(state)
        for trans in newTM.transitions:
            tm.addTransition(trans)

    def compile(self, code):
        parsed = self.parse(code)
        if not parsed:
            return
        parsed = self.getSymbols(parsed)
        parsed = self.resolveLabels(parsed)
        parsed = self.getLines(parsed)
        if not parsed['lines']:
            return
        self.parsed = parsed
        prevTM = TM()
        tms = [prevTM]
        for (lineno, statement) in sorted(parsed['lines'].items()):
            currentTM = statement.getTM(parsed=self.parsed)
            # prevTM.addTransition(
            # prevTM.initialState + '$'
            tms.append(currentTM)
            self.prevTM = currentTM
            self.addStatement(currentTM, statement, parsed)
        return currentTM
