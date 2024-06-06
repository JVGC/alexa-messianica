from time import sleep
from beautifulSoupScraper.sacred_word_scraper import SacredWordScraper


spider = SacredWordScraper()
data = spider.scrape_data()
spider.process_item(data)

while data:
    data = spider.scrape_data()
    spider.process_item(data)
    sleep(2)
