from datetime import date
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from mongo.experience_repository import ExperienceMongoRepository

from scraper.scraper import settings as scraper_settings
from scraper.scraper.spiders.experiencespider import (
    ExperienceSpider,
)


def call_spider():
    crawler_settings = Settings()
    crawler_settings.setmodule(scraper_settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(ExperienceSpider)
    process.start()


def main():
    call_spider()


if __name__ == "__main__":
    load_dotenv()
    main()
