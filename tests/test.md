# Common elements

## A header 2 with id [..]("{{h2:#h2id cls1 cls2 style='text-align:right'}}")

This could be a paragraph ending with the trick [..]("{{p:pclass}}")

> Now this is a blockquote having the same trick at the end.
>   It is a single paragraph. [..]("{{blockquote:#bqid}}") [..]("{{p:pbqcls}}")

I've forgot to put in a paragraph to separate these.

> This will probably not work. [..]("{{blockquote:#outerbq}}")

> > Inner blockquote not sure it will
> >             actually work. [..]("{{blockquote:#innerbq}}")

> And this is the outer/ending paragraph.

And last but not least a list:

1.  first item . [..]("{{ol:lclass}}")
1.  second item[^1]third item


There's also [a link](http://yahoo.com "{{rel='external nofollow'}}") and then `some code`.
Does it work `[this way](http://yahoo.com "{{rel='external nofollow'}}")`? But I also need
a normal [link](http://yahoo.com "some title").

Image is exactly the same:

![alt text](http://yahoo.com "{{width=500 height=200}}")

And now two advanced examples [..]("{{p:#pid andpclass}}")

The other one would be [..]("{{p:style='text-align:right'}}")

*   simple l 1
*   simple l 2
            
    *   inner 2.1
    *   inner 2.3
*   simple l 3


1.  paragraph l 1

1.  para l 2

1.  para l 3

    continuation paragraph

1.  paragraph 4



# Footnotes



[^1]: 
[1]
a footnote&nbsp;


[^1]: I have some vague ideas, but it’s better to learn than to speculate.&nbsp;
# Code snippets

    project/
        __init__.py
        example1.py
        test/
            __init__.py
            test_example1.py
Find a Pygments code snippet to see how it works

    fromBeautifulSoupimportBeautifulSoupimporturllib2soup=BeautifulSoup(urllib2.urlopen('http://java.sun.com').read())menu=soup.findAll('div',attrs={'class':'pad'})forsubMenuinmenu:links=subMenu.findAll('a')forlinkinlinks:print"%s:%s"%(link.string,link['href']) [..]("{{pre:code python literal-block}}")
# Special elements

<ins>insert</ins>

<q>quote</q>

<abbr>abbr</abbr>

A series of elements , ~~delete~~, , that are not natively supported.

Then is time for definition lists:

<div>
    Also DIVs even if they're wrong, they should still work.
</div>

# Embeds

YouTube:

<iframe width="420" height="315" src="//www.youtube.com/embed/rnujQquKCQY" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

Slideshare:

<iframe src="http://www.slideshare.net/slideshow/embed_code/28512891" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen="allowfullscreen"> </iframe>

<div style="margin-bottom:5px"> <strong> <a href="https://www.slideshare.net/subagini/effective-presentation-skills-28512891" title="Effective presentation skills" target="_blank">Effective presentation skills</a> </strong> from <strong><a href="http://www.slideshare.net/subagini" target="_blank">Subagini Manivannan</a></strong> </div>

Vimeo:

<iframe src="//player.vimeo.com/video/78276911?title=0&amp;byline=0&amp;portrait=0&amp;color=ff0000" width="500" height="281" frameborder="0" webkitallowfullscreen="webkitallowfullscreen" mozallowfullscreen="mozallowfullscreen" allowfullscreen="allowfullscreen"></iframe>

[Why I Ride - Ep1: Passion At Work](http://vimeo.com/78276911) from [ALCHEMYcreative](http://vimeo.com/alchemycreative) on [Vimeo](https://vimeo.com).
