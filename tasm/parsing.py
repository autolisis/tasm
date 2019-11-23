#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tasm.lexing
from pprint import pprint
from tasm.lexing import lexer, tokens
from tasm.stmt import stmt

savedLexer = lexer.clone()
labels = {}
statements = []
instructions = {}


def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 3:
        p[0] = {'statements': statements, 'labels': labels}
    else:
        p[0] = {'statements': statements, 'labels': labels}


def p_statement(p):
    '''statement : labelledStatement
                 | unlabelledStatement'''
    p[0] = p[1]
    statements.append(p[1])


def p_labelledStatement(p):
    'labelledStatement : label unlabelledStatement'
    if not labels.get(p[1]):
        labels[p[1]] = p.lineno(2)
    else:
        print(f'Reusing label {p[1]} on line {p.lineno(2)}')

    p[0] = p[2]


def p_unlabelledStatement(p):
    '''unlabelledStatement : acceptStatement
                           | rejectStatement
                           | writeStatement
                           | moveStatement
                           | jumpStatement
                           | ifrStatement'''
    p[1]['stmt'] = p[1]['stmt'].lower()
    p[0] = stmt.new(**p[1])


def p_acceptStatement(p):
    'acceptStatement : accept'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1)}


def p_reject(p):
    'rejectStatement : reject'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1)}


def p_writeStatement(p):
    'writeStatement : wr symbol'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1), 'sym': p[2]}


def p_right(p):
    'moveStatement : right'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1)}


def p_left(p):
    'moveStatement : left'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1)}


def p_jumpStatement(p):
    'jumpStatement : goto destlabel'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(1), 'destlabel': p[2]}


def p_ifrStatement(p):
    'ifrStatement : ifr symbol destlabel'
    p[0] = {'stmt': p[1], 'lineno': p.lineno(
        1), 'sym': p[2], 'destlabel': p[3]}


def p_error(p):
    try:
        print(f'Syntax error at {p.value} on {p.lineno}')
    except AttributeError:
        print(f'Syntax error at {p}')


yacc = __import__('ply.yacc').yacc
parser = yacc.yacc()


def getLexer():
    return tasm.lexing.getLexer()


def getParser():
    return parser


def reset():
    statements.clear()
    labels.clear()
    try:
        parser.restart()
    except AttributeError:
        pass
