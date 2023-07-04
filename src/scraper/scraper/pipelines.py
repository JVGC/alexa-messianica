# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date

from spreadsheet.spreadsheet_repository import SpreadSheetRepository


class ExperiencePipeline:
    def __init__(self) -> None:
        self.experience_repository = SpreadSheetRepository()

    def process_item(self, item, spider):
        print(item.keys())
        self.experience_repository.create(
            date=date.today().strftime(format="%d/%m/%Y"),
            person_name=item["person_name"],
            church=item["church"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )
        return item
