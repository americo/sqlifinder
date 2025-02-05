from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links.append(newUrl)

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

def spider(url, maxPages):
    links = [] 
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit:
        numberVisited += 1
        url = pagesToVisit.pop()
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
        except:
            pass
        return links

print(spider("http://vulnweb.com", 10))