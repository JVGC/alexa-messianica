""" Scraper Settings """
BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.scraper.spiders"]
NEWSPIDER_MODULE = "scraper.scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# update the pipelines to this
ITEM_PIPELINES = {"scraper.scraper.pipelines.ExperiencePipeline": 300}
