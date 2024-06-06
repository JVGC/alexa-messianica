from datetime import date

from bs4 import BeautifulSoup
import requests

from beautifulSoupScraper.helpers import SCRAPE_FUNCTIONS
from beautifulSoupScraper.spreadsheet import SacredWordSpreadSheet

MONTHS = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12",
}


class NotAvailableError(Exception):
    pass


class SacredWordScraper:
    start_url = "https://www.messianica.org.br/escrito-divino?id={id}"
    skip_n_days = 0

    def _get_content(self):
        data = SacredWordSpreadSheet.get_last_scraped_sacred_word()
        _id = data._id + 1 + self.skip_n_days
        response = requests.get(self.start_url.format(id=_id), timeout=5)
        return _id, response.content, data

    def scrape_data(self):
        _id, content, data = self._get_content()
        soup = BeautifulSoup(content, "html.parser")

        url = self.start_url.format(id=_id)
        try:
            title = SCRAPE_FUNCTIONS["title"](soup)
            period = SCRAPE_FUNCTIONS["period"](soup)
            date_str = SCRAPE_FUNCTIONS["date"](soup)
            audio_url = SCRAPE_FUNCTIONS["audio_url"](soup)
            content = SCRAPE_FUNCTIONS["content"](soup)
        except Exception as e:
            d, m, y = data.date.split("/")
            last_scraped_date = date(int(y), int(m), int(d))
            today_date = date.today()
            if last_scraped_date < today_date:
                # means that for some reason the id does not exist
                self.skip_n_days += 1
                return True
            print("Soup:", soup)
            print("Error:", e)
            raise NotAvailableError("Sacred Word is not available yet")

        if not content:
            raise NotAvailableError("Sacred Word is not available yet")
        return {
            "_id": _id,
            "title": title,
            "period": period,
            "date": date_str,
            "url": url,
            "audio_url": audio_url,
            "content": content,
        }

    def _process_date(self, date_str):
        date_str = date_str.split(" ")
        date_str[1] = MONTHS[date_str[1].lower()]
        return f"{date_str[0]}/{date_str[1]}/{date_str[2]}"

    def process_item(self, item):
        if not item:
            return None

        item["date"] = self._process_date(item["date"])

        print("Scrapping today's sacred word")
        SacredWordSpreadSheet.create_sacred_word(
            _id=item["_id"],
            period=item["period"],
            date_str=item["date"],
            title=item["title"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )

        return item
