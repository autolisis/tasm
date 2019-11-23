#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pytest
import mock
from pytest_mock import mocker
from functional import seq
from fn import _

from tasm import parsing
from tasm.stmt import stmt
import ply.lex
from os import path


class TestParsing:
    @classmethod
    def setup_class(self):
        self.lexer = parsing.getLexer()
        self.parser = parsing.getParser()

    @classmethod
    def setup_method(self):
        self.lexer = parsing.getLexer()
        parsing.reset()

    def helpParse(self, code):
        return self.parser.parse(code, tracking=True, lexer=self.lexer)

    def test_empty(self):
        result = self.helpParse('')
        assert result is None

    def test_invalidLabel(self):
        with pytest.raises(Exception):
            result = self.helpParse('ab:\nright\ngoto aa')
            assert result is None

    def test_ifr_validLabel(self):
        result = self.helpParse("ad:\nifr '0' ad")
        assert len(result['statements']) == 1
        assert result['statements'][0] == stmt.new(
            stmt='ifr', lineno=2, sym='0', destlabel='ad')

    def test_ifr_reusedLabel(self):
        result = self.helpParse("ad:\nifr '0' ad\nad:\nright")
        assert len(result['statements']) == 2
        assert result['statements'][0] == stmt.new(
            stmt='ifr', lineno=2, sym='0', destlabel='ad')

    def test_ifr_invalidLabel(self):
        result = self.helpParse("ifr '0' ad")
        assert result
        assert not result['labels']
        assert result['statements']
        assert len(result['statements']) == 1
        assert result['statements'][0] == stmt.new(
            stmt='ifr', lineno=1, sym='0', destlabel='ad')

    def test_program(self):
        p = path.relpath('./data/evenPalindrome.tasm')
        with open(p) as f:
            result = self.helpParse(f.read())

        def getReferencedLabel(st):
            try:
                return st.destlabel
            except AttributeError:
                pass
        referencedLabels = set()
        for st in result['statements']:
            try:
                referencedLabels.add(st.destlabel)
            except AttributeError:
                pass

        assert len(result['statements']) == 23
        assert len(result['labels']) == 7
        assert set(result['labels']) == referencedLabels
