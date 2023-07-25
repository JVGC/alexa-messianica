from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper import settings as scraper_settings
from scraper.scraper.spiders import ExperienceSpider, SacredWordSpider


def call_sacred_word_spider():
    crawler_settings = Settings()
    crawler_settings.setmodule(scraper_settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(SacredWordSpider)
    process.start()


def call_experience_spider():
    crawler_settings = Settings()
    crawler_settings.setmodule(scraper_settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(ExperienceSpider)
    process.start()


def main():
    call_experience_spider()
    call_sacred_word_spider()


if __name__ == "__main__":
    load_dotenv()
    main()
