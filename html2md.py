#!/usr/bin/env python
# -*- coding: utf8 -*-


import argparse
import os
import re
import sys
import textwrap

from BeautifulSoup import ICantBelieveItsBeautifulSoup
from BeautifulSoup import Tag, NavigableString, Declaration, ProcessingInstruction, Comment

__author__ = 'alex'


def html2md(text, attrs=True, footnotes=False):
    proc = Processor(text, attrs=attrs, footnotes=footnotes)
    return proc.get_output()

_KNOWN_ELEMENTS = ('a', 'b', 'strong', 'blockquote', 'br', 'center', 'code', 'dl', 'dt', 'dd', 'div', 'em', 'i',
                   'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'img', 'li', 'ol', 'ul', 'p', 'pre', 'tt', 'sup')

_PHRASING_ELEMENTS = ('abbr', 'audio', 'b', 'bdo', 'br', 'button', 'canvas', 'cite', 'code', 'command',
                      'datalist', 'dfn', 'em', 'embed', 'i', 'iframe', 'img', 'input', 'kbd', 'keygen',
                      'label', 'mark', 'math', 'meter', 'noscript', 'object', 'output', 'progress', 'q',
                      'ruby', 'samp', 'script', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'svg',
                      'textarea', 'time', 'var', 'video', 'wbr')

_CONDITIONAL_PHRASING_ELEMENTS = ('a', 'del', 'ins')

_ALL_PHRASING_ELEMENTS = _CONDITIONAL_PHRASING_ELEMENTS + _PHRASING_ELEMENTS

_IGNORE_ELEMENTS = ('html', 'body', 'article', 'aside', 'footer', 'header', 'main', 'section', 'span')
_SKIP_ELEMENTS = ('head', 'nav', 'menu', 'menuitem')
LF = unicode(os.linesep)


class Processor(object):
    def __init__(self, html, **kwargs):
        """
        Supported options:

        attrs:

        footnotes:
        """
        self.html = html
        self.soup = ICantBelieveItsBeautifulSoup(html)
        self._processed = False
        self._options = {
            'attrs': True,
            'footnotes': False,
        }
        self._options.update(kwargs)

        self._text_buffer = []  # maintains a buffer usually used for block elements
        self._attributes_stack = []
        self._indentation_stack = []  # maintains a stack of indentation types
        self._inside_block = False
        self._inside_footnote = False
        self._list_level = 0
        self._list_item_has_block = False
        self._output = u''
        self._footnote_ref = 0
        self._elements = {
            'a': self._tag_a,
            'b': self._tag_strong,
            'strong': self._tag_strong,
            'blockquote': self._tag_blockquote,
            'br': self._tag_br,
            'code': self._tag_code,
            'tt': self._tag_code,
            'center': self._tag_center,
            'div': self._tag_div,
            'em': self._tag_em,
            'i': self._tag_em,
            'h1': self._tag_h,
            'h2': self._tag_h,
            'h3': self._tag_h,
            'h4': self._tag_h,
            'h5': self._tag_h,
            'h6': self._tag_h,
            'hr': self._tag_hr,
            'img': self._tag_img,
            'li': self._tag_li,
            'ol': self._tag_list,
            'ul': self._tag_list,
            'p': self._tag_p,
            'pre': self._tag_pre,
        }
        if self._options['footnotes']:
            self._elements['sup'] = self._tag_sup



    def get_output(self):
        if not self._processed:
            self._process(self.soup)
            if self._text_buffer:
                self._flush_buffer()
            self._processed = True

        return self._output.rstrip()

    def _process(self, element):
        if element.string and not self._is_empty(element.string):
            txt = element.string
            if not _is_inline(element):
                txt = txt.lstrip()
                txt = re.sub('\n+', '\n', txt, re.M)
                txt = re.sub(' +', ' ', txt)
                txt = re.sub('\n ', '\n', txt)
            self._text_buffer.append(txt)
            return
        for idx, t in enumerate(element.contents):
            if isinstance(t, Tag):
                self._process_tag(t)
            elif isinstance(t, NavigableString) and not self._is_empty(t):
                txt = t.strip('\n\r')
                if idx == 0 and not _is_inline(element):
                    self._text_buffer.append(txt.lstrip(' \t'))
                else:
                    self._text_buffer.append(txt)

    def _proc(self, t, is_inline=False):
        if isinstance(t, Tag):
            self._process_tag(t)
        elif isinstance(t, NavigableString) and not self._is_empty(t):
            self._text_buffer.append(t.strip('\n\r'))

    def _process_tag(self, tag):
        _tag_func = self._elements.get(tag.name)

        if _tag_func:
            _tag_func(tag)
            return

        # even if they contain information there's no way to convert it
        if tag.name in _SKIP_ELEMENTS:
            return

        # go to the children
        if tag.name in _IGNORE_ELEMENTS:
            self._process(tag)
            return

        if self._inside_block:
            self._text_buffer.append(unicode(tag))
        else:
            self._write(unicode(tag), sep=LF * 2)

    def _tag_a(self, tag):
        if tag.get('href'):
            self._text_buffer.append(u'[')
            self._process(tag)
            self._text_buffer.append(u']')
            self._text_buffer.append(u'(')
            self._text_buffer.append(tag['href'])
            attrs = dict(tag.attrs) if tag.attrs else {}
            self.removeAttrs(attrs, 'href', 'title')
            attrs_str = self.simpleAttrs(attrs)
            if attrs_str or tag.get('title'):
                self._text_buffer.append(u' "')
                if tag.get('title'):
                    self._text_buffer.append(tag['title'])
                    if attrs_str:
                        self._text_buffer.append(u' ')
                if attrs_str:
                    self._text_buffer.append(attrs_str)
                self._text_buffer.append(u'"')
            self._text_buffer.append(u')')
        else:
            self._text_buffer.append(unicode(tag))

    def _tag_strong(self, tag):
        """Process <B> and <STRONG>
        """
        self._text_buffer.append(u"**")
        self._process(tag)
        self._text_buffer.append(u"**")

    def _tag_em(self, tag):
        """Process <EM> and <I>
        """
        self._text_buffer.append(u"*")
        self._process(tag)
        self._text_buffer.append(u"*")

    def _tag_blockquote(self, tag):
        """Process a <BLOCKQUOTE>
        """
        self._push_attributes(tag=tag)
        self._inside_block = True
        self._indentation_stack.append('bq')
        self._process(tag)
        self._write_block(sep=LF * 2)
        self._indentation_stack.pop()
        self._inside_block = False

    def _tag_br(self, tag):
        """ Process <BR>
        """
        self._text_buffer.append(u"  " + LF)

    def _tag_code(self, tag):
        """Process <CODE> and <TT>
        """
        self._text_buffer.append(u"`")
        self._text_buffer.append(tag.getText())
        self._text_buffer.append(u"`")

    def _tag_center(self, tag):
        """Process <CENTER>
        """
        if self._options['attrs']:
            self._push_attributes(tagname='p', attrs={'style': 'text-align:center;'})
        self._process(tag)
        self._write_block(sep=LF * 2)

    def _tag_div(self, tag):
        """Process <DIV>
        """
        div_class = tag.get('class')
        if div_class and div_class.find('footnote') > -1:
            self._inside_footnote = True
            self._flush_buffer()
            self._process_footnotes(tag)
            self._inside_footnote = False
            return

        if self._known_div(tag):
            self._inside_block = True
            self._process(tag)
            self._write_block(sep=LF * 2)
            self._inside_block = False
        else:
            self._write(unicode(tag), sep=LF * 2)

    def _tag_dl(self, tag):

        if tag.name == 'dl':
            # FIXME
            return
        if tag.name == 'dt':
            self._process(tag)
            self._write_block(sep=LF)
            return
        if tag.name == 'dd':
            self._text_buffer.append(u':')
            self._text_buffer.append(u' ' * 4)
            self._process(tag)
            self._write_block(sep=LF * 2)
            return

    def _tag_h(self, tag):
        self._push_attributes(tag=tag)
        self._inside_block = True
        self._text_buffer.append(u'#' * int(tag.name[1]) + ' ')
        self._process(tag)
        self._write_block(sep=LF * 2)
        self._inside_block = False
        self._text_buffer = []

    def _tag_hr(self, tag):
        if not self._inside_footnote:
            self._write(LF + u'-----', sep=LF * 2)

    def _tag_img(self, tag):
        self._text_buffer.append(u'![')
        self._text_buffer.append(tag.get('alt') or tag.get('title') or '')
        self._text_buffer.append(u']')
        self._text_buffer.append(u'(')
        self._text_buffer.append(tag['src'])
        attrs = dict(tag.attrs) if tag.attrs else {}
        self.removeAttrs(attrs, 'src', 'title', 'alt')
        attrs_str = self.simpleAttrs(attrs)
        if attrs_str or tag.get('title'):
            self._text_buffer.append(u' "')
            if tag.get('title'):
                self._text_buffer.append(tag['title'])
                if attrs_str:
                    self._text_buffer.append(u' ')
            if attrs_str:
                self._text_buffer.append(attrs_str)
            self._text_buffer.append(u'"')
        self._text_buffer.append(u')')

    def _tag_li(self, tag):
        list_item_has_block = False
        last_block_name = None
        blocks_counter = 0
        self._push_attributes(tag=tag)
        if tag.string:
            if not self._is_empty(tag.string):
                self._text_buffer.append(tag.string.strip())
            self._write_block(sep=LF)
        else:
            elements = []
            for c in tag.contents:
                if isinstance(c, Tag):
                    elements.append(c)
                elif isinstance(c, NavigableString) and not self._is_empty(c):
                    elements.append(c)
            prev_was_text = False
            for c in elements:
                if isinstance(c, NavigableString):
                    self._text_buffer.append(c.strip())
                    prev_was_text = True
                    continue
                if isinstance(c, Tag):
                    if c.name in ('blockquote', 'dl', 'ol', 'p', 'pre', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):  # nopep8
                        blocks_counter += 1
                        list_item_has_block = True
                        last_block_name = c.name
                        if prev_was_text:
                            prev_was_text = False
                            self._write_block(sep=LF * 2)
                        else:
                            self._write_block(sep=LF)
                    self._process_tag(c)

        if list_item_has_block:
            trim_newlines = False
            #        if last_block_name == 'p' and blocks_counter < 3:
            #          trim_newlines = True
            if last_block_name in ('ul', 'ol') and blocks_counter < 2:
                trim_newlines = True
            if trim_newlines and self._output[-2:] == LF * 2:
                self._output = self._output[:-1]
        if self._indentation_stack[-1] in ('cul', 'col'):
            self._indentation_stack[-1] = self._indentation_stack[-1][1:]

    def _tag_list(self, tag):
        self._list_level += 1
        self._push_attributes(tag=tag)
        self._indentation_stack.append(tag.name)
        self._process(tag)
        self._indentation_stack.pop()
        self._list_level -= 1
        self._write('', sep=LF)
        if self._list_level == 0:
            self._write('', sep=LF)

    def _tag_p(self, tag):
        # must finish it by 2 * os.linesep
        self._push_attributes(tag=tag)
        self._inside_block = True
        self._process(tag)
        self._write_block(sep=LF * 2)
        self._inside_block = False

    def _tag_pre(self, tag):
        self._push_attributes(tag=tag)
        self._inside_block = True
        self._indentation_stack.append('pre')
        # FIXME
        pre_text = unicode(tag)
        pre_text = pre_text.replace('<pre>', '').replace('</pre>', '').replace('<code>', '').replace('</code>', '')
        self._text_buffer.append(pre_text.strip(' \t\n\r'))
        self._write_block(sep=LF*2)
        self._indentation_stack.pop()
        self._inside_block = False

    def _tag_sup(self, tag):
        sup_txt = tag.getText()
        if _FOOTNOTE_REF_re.match(sup_txt):
            self._footnote_ref += 1
            self._text_buffer.append(u'[^%s]' % self._footnote_ref)
        else:
            self._write(unicode(tag))


    # CriticMarkup support
    def _tag_ins(self, tag):
        pass

    def _tag_del(self, tag):
        self._text_buffer.append(u"~~")
        self._process(tag)
        self._text_buffer.append(u"~~")


    def _write_block(self, sep=u''):
        if not self._attributes_stack and not self._text_buffer:
            return
        indentation = u''
        extra_indentation = u''
        for idx in range(len(self._indentation_stack)):
            indent_type = self._indentation_stack[idx]
            if indent_type == 'bq':
                indentation += u'> '
                extra_indentation += u'> '
            elif indent_type == 'pre':
                indentation += u' ' * 4
                extra_indentation += u' ' * 4
            elif indent_type == 'ol':
                indentation += u'1.  '
                extra_indentation += u' ' * 4
                self._indentation_stack[idx] = 'col'
            elif indent_type == 'ul':
                indentation += u'*   '
                extra_indentation += (u' ' * 4)
                self._indentation_stack[idx] = 'cul'
            elif indent_type == 'cul':
                indentation += (u' ' * 4)
                extra_indentation += (u' ' * 4)
            elif indent_type == 'col':
                indentation += (u' ' * 4)
                extra_indentation += (u' ' * 4)

        attributes = []
        if self._options['attrs']:
            for tagname, attrs in self._attributes_stack:
                attributes.append(self.elemAttrs(tagname, attrs, '..'))
        self._attributes_stack = []

        txt = indentation
        txt += ''.join(self._text_buffer)
        txt = txt.replace(u'\r\n', LF)
        if sep and txt.endswith(LF):
            txt = txt.rstrip(LF)
        # SHOULD I: textwrap.wrap()
        if attributes:
            txt += u' ' + u' '.join(attributes)
        txt = txt.replace(u'\n', LF + extra_indentation)

        self._write(txt, sep)
        self._text_buffer = []

    def _write(self, value, sep=u''):
        if value and value[0] == LF and self._output and self._output[-1] == LF:
            value = value[len(LF):]
        self._output += _entity2ascii(value) + sep

    def simpleAttrs(self, attrs):
        if not attrs:
            return u""

        attr_arr = []
        lattrs = attrs.copy()
        if 'id' in lattrs:
            attr_arr.append("#%s" % lattrs['id'])
            del lattrs['id']
        if 'class' in lattrs:
            [attr_arr.append(sv) for sv in lattrs['class'].split()]
            del lattrs['class']

        for k, v in lattrs.items():
            use_sep = False
            for c in (' ', ':', '-', ';'):
                if v.find(c) > -1:
                    use_sep = True
                    break
            if use_sep:
                attr_arr.append("%s='%s'" % (k, v))
            else:
                attr_arr.append("%s=%s" % (k, v))
        return u"{{%s}}" % " ".join(attr_arr)

    def elemAttrs(self, tag_name, attrs, sep):
        if not attrs:
            return u""
        attr_arr = []
        lattrs = attrs.copy()
        if 'id' in lattrs:
            attr_arr.append("#%s" % lattrs['id'])
            del lattrs['id']
        if 'class' in lattrs:
            [attr_arr.append(sv) for sv in lattrs['class'].split()]
            del lattrs['class']
        for k, v in lattrs.items():
            use_sep = False
            for c in (' ', ':', '-', ';'):
                if v.find(c) > -1:
                    use_sep = True
                    break
            if use_sep:
                attr_arr.append("%s='%s'" % (k, v))
            else:
                attr_arr.append("%s=%s" % (k, v))
        return u"[%s](\"{{%s:%s}}\")" % (sep, tag_name, " ".join(attr_arr))

    def removeAttrs(self, attrs, *keys):
        if not attrs:
            return
        for k in keys:
            try:
                del attrs[k]
            except KeyError:
                pass

    def _known_div(self, div_tag):
        for t in div_tag.contents:
            if isinstance(t, (NavigableString, Comment)):
                continue
            if isinstance(t, Tag) and t.name in _KNOWN_ELEMENTS:
                continue
            return False
        return True

    def _is_empty(self, value):
        if not value:
            return True
        svalue = value.strip(' \t\n\r')
        if not svalue:
            return True
        return False

    def _flush_buffer(self):
        if self._text_buffer:
            self._write(''.join(self._text_buffer))

    def _push_attributes(self, tag=None, tagname=None, attrs=None):
        attr_dict = None
        if tag:
            tagname = tag.name
            if tag.attrs:
                attr_dict = dict(tag.attrs)
            elif attrs:
                attr_dict = attrs
            else:
                attr_dict = {}
        if tagname and attrs:
            attr_dict = attrs
        if attr_dict:
            self._attributes_stack.append((tagname, attr_dict))

    def _process_footnotes(self, tag):
        self._write('', sep=LF * 2)
        index = 0
        for li in tag.findAll('li'):
            buffer = []
            index += 1
            links = li.findAll('a')

            if links:
                links[-1].extract()

            buffer.append("[^%s]: " % index)

            children = []
            for c in li.contents:
                if isinstance(c, NavigableString):
                    if not self._is_empty(c):
                        children.append(c)
                elif isinstance(c, Tag):
                    children.append(c)
            if len(children) == 1 and isinstance(children[0], Tag) and children[0].name == 'p':
                children = children[0].contents
            for c in children:
                if isinstance(c, NavigableString):
                    buffer.append(c)
                elif isinstance(c, Tag):
                    if c.name in ('a', 'b', 'strong', 'code', 'del', 'em', 'i', 'img', 'tt'):
                        self._process_tag(c)
                        buffer.extend(self._text_buffer)
                        self._text_buffer = []
                    else:
                        buffer.append(unicode(c))

            footnote = u''.join(buffer).strip(' \n\r')
            if footnote.endswith('()'):
                footnote = footnote[:-2]
            self._write(footnote, sep=os.linesep)


def _is_inline(element):
    if isinstance(element, (NavigableString, Declaration, ProcessingInstruction, Comment)):
        return False
    if isinstance(element, Tag) and \
            (element.name in ('blockquote', 'center', 'dl', 'dt', 'dd', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol', 'ul', 'p')):  # nopep8
        return False
    return True

_FOOTNOTE_REF_re = re.compile('\[?[a-zA-Z0-9]\]?')



def _entity2ascii(val):
    for ent, asc in _ENTITY_DICT.items():
        val = val.replace(ent, asc)
    return val


_ENTITY_DICT = {
    '&#8212;': '--',
    '&#8216;': "'",
    '&#8217;': "'",
    '&#8220;': '"',
    '&#8221;': '"',
    '&#8230;': '...',
    u'…': '...',
}


def main(instream):
    markup = html2md(instream.read())

    return markup
    #parser = argparse.ArgumentParser(description='Transform HTML file to Markdown')
    #parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin, help='Input file or stream')
    #options = parser.parse_args(sys.argv)
    #text = options.input.read()


if __name__ == '__main__':
    input = sys.argv[1]
    if not os.path.exists(input):
        print "Input must be either a directory or a file"
        sys.exit(1)

    if os.path.isfile(input):
        result = main(open(input))
    else:
        result = main(sys.stdin)

    print result.encode('utf8')
