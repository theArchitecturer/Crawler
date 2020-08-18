import re
import csv
import urllib.parse
import requests
import enum
from lxml import etree
from lxml import html
from .parse_content import ParseContent


class CodeforceUrl():
    url = 'https://codeforces.com/contests' 
    """ base url for every type of crawl """ 

    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, opt):
        if opt == 'latest':
            self.files = ParseContent(CodeforceUrl.get_latest())
        elif opt.isdigit():
            self.files = CodeforceUrl.contest_handle(CodeforceUrl.get_id(int(opt)))
        # elif opt == 'all':
            # self.url = self.get_all_contest()
        elif re.match(regex, opt) is not None:
            self.files = self.get_url(opt)


    @staticmethod
    def get_latest():
        response = requests.get(CodeforceUrl.url)
        content = html.fromstring(response.content)
        for link in content.xpath('/html/body[1]//div[contains(text(), "Past contests")]/following::table/descendant::tr/td[1]'):
            href = link.xpath('./a[1]/@href')[0]
            return urllib.parse.urljoin(CodeforceUrl.url, href)


    @staticmethod
    def get_id(id_contest):
        return urllib.parse.urljoin(CodeforceUrl.url, f"/contest/{id_contest}")


    @staticmethod
    def contest_handle(url):
        page_start = session.get(url).html
        files = []
        for link_to_next_page in page_start.xpath('//div[@style="float: left;"]/a/@href'):
            next_page_url = urllib.parse.urljoin(url, link_to_next_page)
            files.append(ParseContent(next_page_url).content())
        return files

    @staticmethod # Get all contests at the first page 
    def get_all_contest():
        response = requests.get(CodeforceUrl.url)
        content = html.fromstring(response.content)
        with open('all_contest.csv', 'a+') as outFile:
            dataFile = csv.writer(outFile)
            xpath_opt = '/html/body[1]//div[contains(text(), "Past contests")]/following::table/descendant::tr/td[1]'
            data = content.xpath(xpath_opt)
            for link in reversed(data):
                try:
                    href = link.xpath('./a[1]/@href')[0]
                except IndexError:
                    href = ' '

                try:
                    contest_name = link.xpath('./text()')[0].replace('\r\n', '').rstrip()
                except IndexError:
                    contest_name = ' '
                dataFile.writerow([contest_name, href])
