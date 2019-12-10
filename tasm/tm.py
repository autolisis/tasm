#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import json

from copy import deepcopy
from itertools import groupby
blah = 0


class TM:
    initState = 'init'
    acceptState = 'accept'
    keys = set(['letters', 'states', 'transitions', 'initialState'])

    def __init__(self,
                 *,
                 initialState=initState,
                 letters=['#'],
                 states=[initState, acceptState],
                 transitions=[]):
        self.letters = letters
        self.initialState = initialState
        self.states = list(sorted(set(states)))
        self.transitions = [
            k for k, g in groupby(
                sorted(transitions, key=lambda i: json.dumps(i)))
        ]

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

    def toDict(self):
        d = json.loads(self.toJson())
        return {k: d[k] for k in self.keys}

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def addState(self, state: str):
        if state in self.states:
            if state != 'accept':
                __import__('pdb').set_trace()
                raise ValueError
        s = set(self.states)
        s.add(state)
        self.states = list(sorted(s))

    def addTransition(self, trans):
        trans['oldState'] = trans.get('oldState', self.states[-1])
        trans['newLetter'] = trans.get('newLetter', '*')
        trans['readLetter'] = trans.get('readLetter', '*')
        self.transitions.append(trans)
        self.transitions = [
            k for k, g in groupby(
                sorted(transitions, key=lambda i: json.dumps(i)))
        ]
