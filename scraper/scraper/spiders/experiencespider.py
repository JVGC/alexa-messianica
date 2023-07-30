from datetime import date
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse


class ExperienceSpider(Spider):
    name = "experience"
    start_urls = ["https://www.messianica.org.br/experiencia-de-fe"]

    def parse(self, response: HtmlResponse):
        name_and_local = response.css("aside").css("p::text").getall()
        yield {
            "person_name": name_and_local[0].strip(),
            "church": name_and_local[1].strip(),
            "url": f"{self.start_urls[0]}?d={date.today().strftime(format='%d/%m/%Y')}",
            "audio_url": f"https://www.messianica.org.br{response.css('audio#player').css('source').xpath('@src').get()}",
            "content": "".join(response.css("section#wa-conteudo::text").getall())
            .strip()
            .replace("\r\r", " "),
        }
