#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import mock
from pytest_mock import mocker

from tasm import lexing
import ply.lex
from os import path


class TestLexing:
    # @classmethod
    # def setup_class(self):
    #     self.savedLexer = lexing.lexer.clone()

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

    def test_program(self, mocker):
        p = path.relpath('./data/evenPalindrome.tasm')
        with open(p) as f:
            self.lexer.input(f.read())
        output = [tok for tok in self.lexer]
        assert len(output) == 54 and [
            i for i in output if i is not None] == output
