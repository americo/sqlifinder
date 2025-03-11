from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        """Process HTML start tags to find anchor tags and extract href URLs.
        
        Args:
            tag (str): HTML tag name
            attrs (list): List of (attribute, value) tuples

        """

        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        """Fetch webpage and extract all links found.
        
        Args:
            url (str): URL to fetch and parse
            
        Returns:
            tuple: (html_content, links_found)
                - html_content (str): Page HTML content
                - links_found (list): List of absolute URLs found
        """

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
    """Web crawler that visits pages and collects links.
    
    Args:
        url (str): Starting URL to begin crawl
        maxPages (int): Maximum number of pages to visit
        
    Returns:
        list: All unique links discovered during crawl
    """

    links = [] 
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
        except:
            pass
        return links

print(spider("http://vulnweb.com", 10))