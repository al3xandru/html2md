import unittest

from context import html2md
from assertions import assertEq


class FragTests(unittest.TestCase):
    def test_div_p(self):
        in_html = u'''
<div>
    And an image directly inside a div:

    <img src="http://yahoo.com" alt="alt text" width="500" height="200" />
</div>

<p id="pid" class="andpclass">And now two advanced examples</p>'''
        out_md = u'''
And an image directly inside a div:

    ![alt text](http://yahoo.com "{{width=500 height=200}}")

And now two advanced examples [..]("{{p:#pid andpclass}}")'''.lstrip()

        assertEq(out_md, html2md.html2md(in_html, attrs=True))

    def test_complex_div_p(self):
        in_html = u'''
<div style="margin-bottom:5px"> <strong> <a href="https://www.slideshare.net/subagini/effective-presentation-skills-28512891" title="Effective presentation skills" target="_blank">Effective presentation skills</a> </strong> from <strong><a href="http://www.slideshare.net/subagini" target="_blank">Subagini Manivannan</a></strong> </div>

<p>Vimeo:</p>
'''
        out_md = u'''
**[Effective presentation skills](https://www.slideshare.net/subagini/effective-presentation-skills-28512891 "Effective presentation skills {{target=_blank}}")** from **[Subagini Manivannan](http://www.slideshare.net/subagini "{{target=_blank}}")**

Vimeo:'''
        assertEq(out_md, html2md.html2md(in_html))


    def test_div_hr(self):
        in_html = u'''
<div>
    Also DIVs even if they're wrong, they should still work.
</div>

<hr>'''
        out_md = u'''
Also DIVs even if they're wrong, they should still work.

-----'''
        assertEq(out_md, html2md.html2md(in_html))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(FragTests)


if __name__ == '__main__':
    unittest.main()