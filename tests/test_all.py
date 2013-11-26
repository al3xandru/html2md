import unittest

import test_attributes
import test_basic
import test_blockquote
import test_breaks
import test_lists
import test_nestedelements
import test_purelists
import test_unknownelements
import test_spacing
import test_frag
import test_pre
import test_criticmarkup
import test_definitionlist

def suite():
    return unittest.TestSuite([
        test_attributes.suite(),
        test_basic.suite(),
        test_blockquote.suite(),
        test_breaks.suite(),
        test_purelists.suite(),
        test_lists.suite(),
        test_unknownelements.suite(),
        test_nestedelements.suite(),
        test_spacing.suite(),
        test_frag.suite(),
        test_pre.suite(),
        test_criticmarkup.suite(),
        test_definitionlist.suite()])


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run (test_suite)
