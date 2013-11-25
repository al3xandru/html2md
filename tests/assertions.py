# -*- coding: utf8 -*-


def assertEq(expected, actual):
#  if len(expected) != len(actual):
#    raise AssertionError("Length differs: expected %s actual %s" % (len(expected), len(actual)))
    expected = expected.replace("\t", "....").replace(" ", ".")
    actual = actual.replace("\t", "....").replace(" ", ".")
    if expected != actual:
        for idx in range(min(len(expected), len(actual))):
            if expected[idx] != actual[idx]:
                actual = actual[:idx] + ">%s<" % actual[idx] + actual[idx + 1:]
                break
        msg = u"\nExpected:'''\n%s'''\nActual:'''\n%s'''" % (expected, actual)
        raise AssertionError(msg)