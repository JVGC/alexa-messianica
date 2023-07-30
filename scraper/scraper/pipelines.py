"""  Define your item pipelines here """
from datetime import date

from scraper.scraper.spreadsheet import create_experience, create_sacred_word


class ExperiencePipeline:
    def __init__(self) -> None:
        pass

    def process_item(self, item, spider):
        if spider.__class__.__name__ == "ExperienceSpider":
            create_experience(
                date=date.today().strftime(format="%d/%m/%Y"),
                person_name=item["person_name"],
                church=item["church"],
                content=item["content"],
                audio_url=item["audio_url"],
                url=item["url"],
            )
        else:
            create_sacred_word(
                date=date.today().strftime(format="%d/%m/%Y"),
                title=item["title"],
                content=item["content"],
                audio_url=item["audio_url"],
                url=item["url"],
            )

        return item
