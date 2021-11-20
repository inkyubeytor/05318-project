import requests
from bs4 import BeautifulSoup
import time
import os


class RRIndexScraper:
    def __init__(self, out_dir, delay=5):
        self.base = "https://www.royalroad.com"
        self.index_base = f"{self.base}/fictions/best-rated"
        self.out = out_dir
        self.delay = delay

    def scrape_index(self, pages):
        try:
            with open(f"{self.out}/index.txt", "r") as f:
                contents = set(f.read().split("\n"))
        except FileNotFoundError:
            contents = set()

        for page in pages:
            links = self.scrape_index_page(page)

            with open(f"{self.out}/index.txt", "a") as f:
                for link in links:
                    if link not in contents:
                        f.write(f"{self.base}{link}\n")

            contents |= links

    def make_page_url(self, page):
        return f"{self.index_base}?page={page}"

    def scrape_index_page(self, page):
        print(f"Scraping page {page}")
        time.sleep(self.delay)
        data = requests.get(self.make_page_url(page))
        soup = BeautifulSoup(data.content, "lxml")
        links = [d.a["href"] for d in soup.find_all(class_="fiction-title")]
        return {link for link in links if link.startswith("/fiction")}


if __name__ == "__main__":
    from itertools import count
    scraper = RRIndexScraper("../data")
    # finished 1-1104
    scraper.scrape_index(count(1105))
