#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from tasm import lexing
import ply.lex

import os
from contextlib import contextmanager
@contextmanager
def getFile(filename, *args, **kwargs):
    rootPath = os.popen('git rev-parse --show-toplevel').read().strip()
    path = os.path.join(rootPath, 'tests', 'data', filename)
    f = open(path, *args, **kwargs)
    yield f
    f.close()


class TestLexing:
    def setup_method(self, method):
        self.lexer = lexing.getLexer()

    def test_comment(self):
        self.lexer.input('# This is a comment')
        output = [tok for tok in self.lexer]
        assert len(output) == 0

    def test_valid_instruction(self):
        self.lexer.input('ifr')
        output = [tok for tok in self.lexer]
        assert len(output) == 1

    def test_invalid_instruction1(self):
        self.lexer.input('xyz')
        output = [tok for tok in self.lexer]
        assert len(output) == 0

    def test_program(self):
        with getFile('evenPalindrome.tasm') as f:
            self.lexer.input(f.read())
        output = [tok for tok in self.lexer]
        assert len(output) == 54 and [
            i for i in output if i is not None] == output
