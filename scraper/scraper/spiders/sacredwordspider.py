from datetime import date
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse


class SacredWordSpider(Spider):
    name = "sacred_word"
    start_urls = [
        f"https://www.messianica.org.br/escrito-divino?d={date.today().strftime(format='%d/%m/%Y')}"
    ]

    def parse(self, response: HtmlResponse):
        yield {
            "title": response.css("section")
            .css("h2.calendar-card__content-title::text")
            .get()
            .strip(),
            "date": response.css("h1::text").get().strip(),
            "url": self.start_urls[0],
            "audio_url": f"https://www.messianica.org.br{response.css('audio#player').css('source').xpath('@src').get()}",
            "content": "".join(response.css("section#wa-conteudo::text").getall())
            .strip()
            .replace("\r\r", " "),
        }
