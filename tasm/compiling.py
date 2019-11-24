#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import tasm.parsing
from tasm.parsing import getLexer, getParser


def helpParse(code):
    return p.parse(code, tracking=True, lexer=self.lexer)


class Compiler:
    def __init__(self):
        self.parser = getParser()
        tasm.parsing.reset()
        self.lexer = getLexer()

    def compile(self, code):
        pass
