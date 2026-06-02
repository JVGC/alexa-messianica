import json
import time
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scraper import (
    SacredWordSpider,
    _connect_spreadsheet,
    get_sacred_word_by_date,
    create_sacred_word,
)

START_DATE = date(2026, 1, 1)
END_DATE = date.today()
BASE_URL = "https://www.messianica.org.br"
DELAY = 1  # seconds between requests


def get_all_existing_dates() -> set:
    sheet = _connect_spreadsheet("sacred_word_v2")
    dates = sheet.col_values(2)  # column B = date
    return set(dates[1:])  # skip header


def get_prev_url(soup: BeautifulSoup) -> str | None:
    for a in soup.find_all("a", href=True):
        if "Ir para a página anterior" in a.get_text():
            return BASE_URL + a["href"]
    return None


def scrape_range():
    spider = SacredWordSpider()

    print("Loading existing dates from spreadsheet...")
    existing_dates = get_all_existing_dates()
    print(f"Found {len(existing_dates)} existing entries.")

    # Start from today and walk backwards to START_DATE
    current_url = spider.get_today_url()
    if not current_url:
        print("Could not find today's URL.")
        return

    scraped = 0
    skipped = 0
    visited = set()

    while current_url and current_url not in visited:
        visited.add(current_url)

        response = requests.get(current_url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Check the date of this entry
        time_tag = soup.find("time")
        if not time_tag:
            print(f"No date found on {current_url}, skipping.")
            prev_url = get_prev_url(soup)
            current_url = prev_url
            continue

        entry_date = date.fromisoformat(time_tag["datetime"][:10])
        formatted_date = entry_date.strftime("%d/%m/%Y")

        # Stop if we've gone past the start date
        if entry_date < START_DATE:
            print(f"Reached {formatted_date}, before start date. Stopping.")
            break

        if formatted_date in existing_dates:
            print(f"[SKIP] {formatted_date} already exists.")
            skipped += 1
        else:
            data = spider.scrape_data(response.content, current_url)
            create_sacred_word(
                date_str=formatted_date,
                title=data["title"],
                content=data["content"],
                audio_url=data["audio_url"],
                url=data["url"],
            )
            existing_dates.add(formatted_date)
            scraped += 1
            print(f"[DONE] {formatted_date} — {data['title']}")

        prev_url = get_prev_url(soup)
        current_url = prev_url
        time.sleep(DELAY)

    print(f"\nFinished. Scraped: {scraped}, Skipped: {skipped}")


if __name__ == "__main__":
    scrape_range()
