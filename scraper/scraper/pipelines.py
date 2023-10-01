"""  Define your item pipelines here """
from datetime import date

from scraper.spreadsheet import create_sacred_word, get_sacred_word_by_date


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


class InsertPipeline:
    def __init__(self) -> None:
        pass

    def process_item(self, item, _):
        item["date"] = item["date"].split(" ")

        item["date"][1] = MONTHS[item["date"][1].lower()]

        if (
            item["date"][0].lstrip("0") != str(date.today().day)
            and item["date"][1].lstrip("0") != str(date.today().month)
            and item["date"][2] != str(date.today().year)
        ):
            print("Today's sacred word is not available yet")
            return item

        already_exists = get_sacred_word_by_date(
            date.today().strftime(format="%d/%m/%Y")
        )
        if already_exists:
            print("Today's sacred word already scrapped. Skipping...")
            return item

        print("Scrapping today's sacred word")
        create_sacred_word(
            date=date.today().strftime(format="%d/%m/%Y"),
            title=item["title"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )

        return item
