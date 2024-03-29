#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pytest

from tasm.stmt import stmt
from tasm.compiling import Compiler
import json

import os
from contextlib import contextmanager


@contextmanager
def getFile(filename, *args, **kwargs):
    rootPath = os.popen('git rev-parse --show-toplevel').read().strip()
    path = os.path.join(rootPath, 'tests', 'data', filename)
    f = open(path, *args, **kwargs)
    yield f
    f.close()


class TestCompiler:
    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def setup_method(self):
        self.compiler = Compiler()

    def test_empty(self):
        op = self.compiler.compile('')
        exp = None
        assert op == exp

    @pytest.mark.parametrize('ipFile,expFile', [
        ('acc.tasm', 'acc.tout'),
        ('rej.tasm', 'rej.tout'),
        ('wr.tasm', 'wr.tout'),
        ('left.tasm', 'left.tout'),
        ('right.tasm', 'right.tout'),
        ('goto.tasm', 'goto.tout'),
        ('ifr.tasm', 'ifr.tout'),
    ])
    def test_basic_statements(self, ipFile, expFile):
        self.compiler = Compiler()
        with getFile(ipFile) as ip:
            compiled = self.compiler.compile(ip.read())
            with getFile(expFile) as exp:
                expected = json.load(exp)
        assert compiled.toDict() == expected
