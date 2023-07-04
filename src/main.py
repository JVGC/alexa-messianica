from datetime import date
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spreadsheet.experience_repository import ExperienceSheetRepository
from scraper.scraper import settings as scraper_settings
from scraper.scraper.spiders.experiencespider import (
    ExperienceSpider,
)

from scraper.scraper.spiders.sacredwordspider import SacredWordSpider


def call_spider():
    crawler_settings = Settings()
    crawler_settings.setmodule(scraper_settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(ExperienceSpider)
    process.start()


def main():
    # experience_repository = ExperienceSheetRepository()

    # experience = experience_repository.getByDate(
    # date.today().strftime(format="%d/%m/%Y")
    # )

    # print(experience)
    call_spider()


if __name__ == "__main__":
    load_dotenv()
    main()
