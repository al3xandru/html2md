import unittest

from context import html2md
from assertions import assertEq


class DefinitioListTests(unittest.TestCase):
    def test_basic(self):
        in_html = u'''
<dl>
<dt>Apple</dt>
<dd>Pomaceous fruit of plants of the genus Malus in
the family Rosaceae.</dd>

<dt>Orange</dt>
<dd>The fruit of an evergreen tree of the genus Citrus.</dd>
</dl>'''
        out_md = u'''
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.
'''.strip()

        assertEq(out_md, html2md.html2md(in_html, def_list=True))

    def test_multi_dd(self):
        in_html = u'''
<dl>
<dt>Apple</dt>
<dd>Pomaceous fruit of plants of the genus Malus in
the family Rosaceae.</dd>
<dd>An American computer company.</dd>

<dt>Orange</dt>
<dd>The fruit of an evergreen tree of the genus Citrus.</dd>
</dl>'''
        out_md = u'''
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.
:   An American computer company.

Orange
:   The fruit of an evergreen tree of the genus Citrus.'''

        assertEq(out_md, html2md.html2md(in_html, def_list=True))

    def test_multi_dt(self):
        in_html = u'''
<dl>
<dt>Term 1</dt>
<dt>Term 2</dt>
<dd>Definition a</dd>

<dt>Term 3</dt>
<dd>Definition b</dd>
</dl>'''
        out_md = u'''
Term 1
Term 2
:   Definition a

Term 3
:   Definition b
'''.strip()

        assertEq(out_md, html2md.html2md(in_html, def_list=True))

    def not_supported_test_paragraph_dd(self):
        in_html = u'''
<dl>
<dt>Apple</dt>
<dd><p>Pomaceous fruit of plants of the genus Malus in
the family Rosaceae.</p></dd>

<dt>Orange</dt>
<dd><p>The fruit of an evergreen tree of the genus Citrus.</p></dd>
</dl>'''
        out_md = u'''
Apple

:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange

:    The fruit of an evergreen tree of the genus Citrus.
'''

        assertEq(out_md, html2md.html2md(in_html, def_list=True))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(DefinitioListTests)


if __name__ == '__main__':
    unittest.main()