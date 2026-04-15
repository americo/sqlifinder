from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib import parse
from typing import Optional


class LinkParser(HTMLParser):

    def __init__(self, baseUrl: str) -> None:
        super().__init__()
        self.baseUrl = baseUrl
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        """Process HTML start tags to find anchor tags and extract href URLs.

        Args:
            tag (str): HTML tag name
            attrs (list): List of (attribute, value) tuples

        """
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href' and value is not None:
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links.append(newUrl)

    def getLinks(self, url: str) -> tuple[str, list[str]]:
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
        try:
            response = urlopen(url)
        except (URLError, HTTPError) as exc:
            return "", []

        content_type = response.getheader("Content-Type", "")
        if not content_type.startswith("text/html"):
            return "", []

        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8", errors="replace")
        self.feed(htmlString)
        return htmlString, self.links


def spider(url: str, maxPages: int) -> list[str]:
    """Web crawler that visits pages up to maxPages.

    Args:
        url (str): Starting URL
        maxPages (int): Maximum number of pages to crawl

    Returns:
        list[str]: All unique URLs discovered across all crawled pages
    """
    pagesToVisit: list[str] = [url]
    visited: set[str] = set()
    all_links: list[str] = []
    numberVisited = 0

    while numberVisited < maxPages and pagesToVisit:
        numberVisited += 1
        url = pagesToVisit.pop(0)

        if url in visited:
            continue
        visited.add(url)

        try:
            _, links = LinkParser(url).getLinks(url)
        except (URLError, HTTPError, ValueError):
            continue

        for link in links:
            if link not in visited:
                pagesToVisit.append(link)
                all_links.append(link)

    return all_links
