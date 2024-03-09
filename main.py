import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()
        self.max=50 # max limit for urls is 50
        self.count=0 # counting the no of urls

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()
            self.count =self.count +1 # after everyone insertion of url into dict inserting the current count of the value 
            if self.count ==self.max: # checking current count is equal to max return 
                return
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    #changed two if conditions to nested if condition 
                    # so that if url locates valid location and starts with base url then only function crawls
                    if urlparse(href).netloc:
                        if  href.startswith(base_url or url):   #fixed if condition
                            href = urljoin(base_url or url, href)
                            self.crawl(href, base_url=base_url or url)
            # extact and follow links on the current page
            for link in self.extract_links(soup,base_url or url):
                self.crawl(link,base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def extract_links(self, soup, base_url):
        # Extract links from the current page
        links = []
        tcount=0    #keep track of link count

        for anchor_tag in soup.find_all('a', href=True):
            href = anchor_tag['href']
            absolute_link = urljoin(base_url, href)

            # Check if the absolute link is within the same domain
            if urlparse(absolute_link).netloc == urlparse(base_url).netloc:
                links.append(absolute_link)
                tcount+=1
                if tcount>50:     #limiting url count to 50
                    return links
                

        return links           

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower():        #fixed search condition
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}") #fixed the print statement from undefined_variable to result
        else:
            print("No results found.")
def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)    #fixed method name craw to crawl

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)


if __name__ == "__main__":
    main()
