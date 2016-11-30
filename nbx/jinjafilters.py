# -*- coding: utf-8 -*-

from nbx.utils.format import moneyfmt, timeago

def dateformat_filter(date, format='%d/%m/%Y'):
    if date:
        return date.strftime(format)
    return ''

def timeago_filter(date):
    if date:
        return timeago(date)
    return ''

def moneyfmt_filter(value, places=2, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg=''):
    return moneyfmt(value, places, curr, sep, dp, pos, neg, trailneg)

def cuitfmt_filter(value):
    return value[:2] + '-' + value[2:11] + '-' + value[-1]
