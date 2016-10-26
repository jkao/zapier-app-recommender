import bs4
import urllib2

class ZapbookScraper():

    def __init__(self, url='https://zapier.com/zapbook/'):
        self.req = urllib2.Request(url)

    def run(self):
        print(self.req)
        response = urllib2.urlopen(self.req)
        html = response.read()
        print(html)

    def fetch_zapbook_links(self):
        pass

