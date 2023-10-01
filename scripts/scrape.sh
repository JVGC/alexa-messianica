#!/bin/bash
export PATH="/home/ubuntu/.local/bin:$PATH"
cd scraper
poetry run scrapy crawl sacred_word