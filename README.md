# html2md

html2md is a Python script that converts HTML (complete or fragments) into [Markdown][markdown].

html2md was inspired by Aaron Swartz's [html2text][html2text]
and is adding support for missing elements that are common in HTML pages
without compromising the Markdown format.

## Usage

```bash
html2md.py [-h] [-a] [-f] [--fenced_code {github,php}] [-e ENCODING]
                  [infile]

Transform HTML file to Markdown

positional arguments:
  infile

optional arguments:
  -h, --help            show this help message and exit
  -a, --attrs           Enable element attributes in the output (custom
                        Markdown extension)
  -f, --footnotes       Enabled footnote processing (custom Markdown
                        extension)
  --fenced_code {github,php}, --fencedcode {github,php}, --fenced {github,php}
                        Enabled fenced code output
  -e ENCODING, --encoding ENCODING
                        Provide an encoding for reading the input
```

Using it from your code:

```python
import html2md
print html2md.html2md("<p>Getting rid of HTML with html2md. Yey!</p>")
```

You can pass in different options

*   `footnotes`: `True|False` (default `False`) convert footnotes
*   `fenced_code`: `default|github|php` (default: `default`) convert code snippets into fenced code
*   `attrs`: convert HTML attributes. _This is a custom extension and should not be used_.



## License

Short version: **OK** for open source projects. **OK** for commercial projects with my [signed agreement](mailto:html2md@mypopescu.com) **only**.

Long version: see the [License](LICENSE.md) file in the project.

[markdown]: http://daringfireball.net/projects/markdown/
[html2text]: http://www.aaronsw.com/2002/html2text/
