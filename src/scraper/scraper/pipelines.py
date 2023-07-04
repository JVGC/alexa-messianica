# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date

from spreadsheet.experience_repository import ExperienceSheetRepository
from spreadsheet.sacred_word_repository import SacredWordSheetRepository


class ExperiencePipeline:
    def __init__(self) -> None:
        self.experience_repository = ExperienceSheetRepository()
        self.sacred_word_repository = SacredWordSheetRepository()

    def process_item(self, item, spider):
        if spider.__class__.__name__ == "ExperienceSpider":
            self.experience_repository.create(
                date=date.today().strftime(format="%d/%m/%Y"),
                person_name=item["person_name"],
                church=item["church"],
                content=item["content"],
                audio_url=item["audio_url"],
                url=item["url"],
            )
        else:
            self.sacred_word_repository.create(
                date=date.today().strftime(format="%d/%m/%Y"),
                title=item["title"],
                content=item["content"],
                audio_url=item["audio_url"],
                url=item["url"],
            )

        return item
