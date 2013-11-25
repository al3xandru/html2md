import unittest

from context import html2md
from assertions import assertEq


class SpaceTests(unittest.TestCase):
    def test_multispace_in_paragraph(self):
        in_html = u'''
            <blockquote>
                <p>Now this is a blockquote having the same trick at the end.
              It is a single paragraph.</p>
            </blockquote>'''
        out_md = u"""
> Now this is a blockquote having the same trick at the end.
> It is a single paragraph.""".lstrip('\n')

        assertEq(out_md, html2md.html2md(in_html))

    def test_div_space(self):
        in_html = u'''
<div>
    And an image directly inside a div:

    <img src="http://yahoo.com" alt="alt text" width="500" height="200" />
</div>'''
        out_md = u'''
And an image directly inside a div:

    ![alt text](http://yahoo.com "{{width=500 height=200}}")'''.lstrip()
        assertEq(out_md, html2md.html2md(in_html))


    def test_initial_p_space(self):
        in_html = u'''
<p>
    A paragraph in a formatted form.

    And another sentence 2 lines below.
</p>'''
        out_md = u'''
A paragraph in a formatted form.
And another sentence 2 lines below.'''.lstrip()
        assertEq(out_md, html2md.html2md(in_html))

    def test_initial_li_space(self):
        in_html = u'''
<ul>
    <li>   item 1</li>
    <li>
        item 2</li>
    <li>
        item 3
    </li>
    <li>  item 4
        <p>
            With a paragraph
        </p>
    </li>
</ul>'''
        out_md = u'''
*   item 1
*   item 2
*   item 3
*   item 4

    With a paragraph'''.lstrip()
        assertEq(out_md, html2md.html2md(in_html))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(SpaceTests)


if __name__ == '__main__':
    unittest.main()