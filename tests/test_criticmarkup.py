import unittest

from context import html2md
from assertions import assertEq


class CriticMarkupTest(unittest.TestCase):
    def test_ins_inline(self):
        in_html = u'''<p>Firstly an inline insert for <ins>words that escape us</ins>.</p>'''
        out_md  = u'''Firstly an inline insert for {++words that escape us++}.'''

        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_ins_block(self):
        in_html = u'''
<blockquote>
    <p>blockquote paragraph</p>
    <ins><p>correction added</p></ins>
</blockquote>'''
        out_md  = u'''
> blockquote paragraph

> {++correction added++}
'''.strip()
        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_del_inline(self):
        in_html = u'''<p>Deleting some <del>words that escape us</del> from this paragraph.</p>'''
        out_md  = u'''Deleting some {--words that escape us--} from this paragraph.'''

        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_del_block(self):
        in_html = u'''
<blockquote>
    <p>blockquote paragraph</p>
    <del><p>deleted error</p></del>
</blockquote>'''
        out_md  = u'''
> blockquote paragraph

> {--deleted error--}
'''.strip()
        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_comments(self):
        in_html = u'''<p>This paragraph contains <!--a secret--> comment.</p>'''
        out_md  = u'''This paragraph contains {>>a secret<<} comment.'''

        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_highlight_simple(self):
        in_html = u'''<p>This paragraph contains <u>a highlighted</u> comment.</p>'''
        out_md  = u'''This paragraph contains {==a highlighted==}{>><<} comment.'''

        assertEq(out_md, html2md.html2md(in_html, critic_markup=True))

    def test_hightlight(self):
        pass

    def test_substitution_inline(self):
        pass

    def test_substitution_block(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(CriticMarkupTest('test_ins_inline'))
    suite.addTest(CriticMarkupTest('test_del_inline'))
    suite.addTest(CriticMarkupTest('test_comments'))
    suite.addTest(CriticMarkupTest('test_highlight_simple'))
    suite.addTest(CriticMarkupTest('test_ins_block'))
    suite.addTest(CriticMarkupTest('test_del_block'))
    return suite


if __name__ == '__main__':
    unittest.main()