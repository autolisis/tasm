#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import pytest

from tasm.stmt import stmt
from tasm.compiler import compile
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
        pass

    @pytest.mark.parametrize(
        'ipFile,expFile',
        [('acc.tasm', 'acc.tout')]
    )
    def test_basic_statements(self, ipFile, expFile):
        with getFile(ipFile) as ip:
            with getFile(expFile) as exp:
                assert compile(ip.read()) == json.load(exp)
