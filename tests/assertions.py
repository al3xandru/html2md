# -*- coding: utf8 -*-
import os


def assertEq(expected, actual):
    if not isinstance(expected, unicode):
        expected = unicode(expected)
    expected = expected.lstrip(os.linesep)
    actual = actual.lstrip(os.linesep)
    expected = expected.replace("\t", "....").replace(" ", ".")
    actual = actual.replace("\t", "....").replace(" ", ".")
    if expected != actual:
        for idx in range(min(len(expected), len(actual))):
            if expected[idx] != actual[idx]:
                actual = actual[:idx] + (u"^%s^" % actual[idx]) + actual[idx + 1:]
                break
        msg = u"\nExpected:\n%s\nActual:\n%s" % (expected, actual)
        msg += u"\nExpected:\n%r\nActual:\n%r" % (expected, actual)
        raise AssertionError(msg)