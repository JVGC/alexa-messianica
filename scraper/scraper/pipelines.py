"""  Define your item pipelines here """
from datetime import date

from scraper.spreadsheet import create_sacred_word


class InsertPipeline:
    def __init__(self) -> None:
        pass

    def process_item(self, item, _):
        create_sacred_word(
            date=date.today().strftime(format="%d/%m/%Y"),
            title=item["title"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )

        return item
