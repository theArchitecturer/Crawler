import re
import requests
from lxml import html

BEGIN_HTML = """ <!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>MathJax example</title>
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script id="MathJax-script" async
          src="https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js">
  </script>
</head>
<body>
"""

END_HTML = """</body>
</html>"""


class ParseContent():

    def __init__(self, url):
        raw_data = requests.get(url)
        self.raw_content = html.fromstring(raw_data.content)

    """
    In case there're many title just take first one
    """
    def name(self):
        return self.raw_content.xpath('//div[@class="title"]/text()')[0]

    def time_limit(self):
        return self.raw_content.xpath('//div[@class="time-limit"]/text()')

    def memory_limit(self):
        return self.raw_content.xpath('//div[@class="memory-limit"]/text()')

    def input(self):
        return self.raw_content.xpath('//div[@class="input-file"]/text()')

    def output(self):
        return self.raw_content.xpath('//div[@class="output-file"]/text()')

    def content(self):
        problem_name = self.raw_content.xpath('//div[@class="title"]/text()')[0]
        problem, name = problem_name.split('. ')
        outFile = f"{problem}_{name}.html"
        with open(outFile, 'w'):
            outFile.write(BEGIN_HTML)
            for hello in self.raw_content.xpath('//div/p/text()'):
                outFile.write("<p>\n{}\n</p>".format(re.sub('\$+', '$$', hello)))
            outFile.write(END_HTML)
        return outFile
