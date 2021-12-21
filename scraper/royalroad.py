import requests
from bs4 import BeautifulSoup
import time
import os
import RoyalRoadLAPI.royalroadlapi as rr


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


class RRScraper:
    def __init__(self, out_dir, delay=15):
        self.out = out_dir
        self.delay = delay
        self.base = "https://www.royalroad.com"

    def load_index(self):
        with open(f"{self.out}/index.txt", "r") as f:
            lines = f.read().splitlines()
        line_splits = [line.split("/")[-2:] for line in lines]
        return {line[0]: line[1] for line in line_splits}

    def get_fics(self):
        existing = set(os.listdir(f"{self.out}/fics"))
        for fic_id, fic_name in self.load_index().items():
            if fic_name not in existing:
                self.get_fic(fic_id, fic_name)

    def get_fic(self, fic_id, fic_name):
        try:
            chapter_links = rr.get_chapter_link_list(fic_id, end_chapter="10")
        except AttributeError:
            return
        print(f"Getting {fic_name}")
        fic_dir = f"{self.out}/fics/{fic_name}"
        os.mkdir(fic_dir)
        for i, link in enumerate(chapter_links):

            data = requests.get(f"{self.base}{link}")
            soup = BeautifulSoup(data.content, "lxml")
            content = soup.find(class_="chapter-inner chapter-content").text
            with open(f"{fic_dir}/{i+1}.txt", "w+", encoding="utf-8") as f:
                f.write(content)
            time.sleep(self.delay)


if __name__ == "__main__":
    # from itertools import count
    # scraper = RRIndexScraper("../data")
    # # finished 1-1104
    # scraper.scrape_index(count(1105))

    fic_scraper = RRScraper("../data")
    fic_scraper.get_fics()
