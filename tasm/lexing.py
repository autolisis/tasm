#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import ply.lex as lex

states = (
    ('WR', 'exclusive'),
    ('GOTO', 'exclusive'),
    ('IFR', 'exclusive'),
)

tokens = (
    'label',
    'accept',
    'reject',
    'right',
    'left',
    'wr',
    'goto',
    'ifr',
    'destlabel',
    'symbol',
)


def t_label(t):
    '\w+:'
    t.value = t.value.strip(':')
    return t


def t_comment(t):
    '\#.*'
    pass


t_accept = '(?i)acc'
t_reject = '(?i)rej'
t_right = '(?i)right'
t_left = '(?i)left'


def t_wr(t):
    r'(?i)wr'
    t_begin_WR(t)
    return t


def t_begin_WR(t):
    r'begin_WR'
    t.lexer.push_state('WR')


def t_WR_symbol(t):
    r'\'.\''
    t.value = t.value.strip('\'')
    t_WR_end(t)
    return t


def t_WR_space(t):
    r'[\ \t]+'
    pass


def t_WR_end(t):
    r'end_WR'
    t.lexer.pop_state()


def t_ifr(t):
    r'(?i)ifr'
    t_begin_IFR(t)
    return t


def t_begin_IFR(t):
    r'begin_IFR'
    t.lexer.push_state('IFR')


def t_IFR_symbol(t):
    r'\'.\''
    t.value = t.value.strip('\'')
    return t


def t_IFR_space(t):
    r'[\ \t]+'
    pass


def t_IFR_destlabel(t):
    r'\w+'
    t_IFR_end(t)
    return t


def t_IFR_end(t):
    r'end_IFR'
    t.lexer.pop_state()


def t_goto(t):
    r'(?i)goto'
    t_begin_GOTO(t)
    return t


def t_begin_GOTO(t):
    r'begin_GOTO'
    t.lexer.push_state('GOTO')


def t_GOTO_space(t):
    r'[\ \t]+'
    pass


def t_GOTO_destlabel(t):
    r'\w+'
    t_GOTO_end(t)
    return t


def t_GOTO_end(t):
    r'end_GOTO'
    t.lexer.pop_state()


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore = ' \t'


def t_ANY_error(t):
    print(f"Illegal character {t.value[0]} on line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()
savedLexer = lexer.clone()


def getLexer():
    return savedLexer.clone()


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        code = f.read()
    lexer.input(code)
