#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import mock
from pytest_mock import mocker

from tasm.stmt import stmt


class TestStmt:
    def test_statement(self):
        a = stmt.Statement(lineno=43)

    def test_accept(self):
        a = stmt.Accept(lineno=43)
        assert a.lineno == 43

    def test_reject(self):
        a = stmt.Reject(lineno=43)
        assert a.lineno == 43

    def test_write(self):
        a = stmt.Write(lineno=43, sym='d')
        assert a.lineno == 43
        assert a.sym == 'd'

    def test_jump(self):
        a = stmt.Jump(lineno=43, destlabel='abc')
        assert a.lineno == 43
        assert a.destlabel == 'abc'

    def test_ifr(self):
        a = stmt.IFR(lineno=43, sym='d', destlabel='abc')
        assert a.lineno == 43
        assert a.sym == 'd'
        assert a.destlabel == 'abc'
