from datetime import date
from scrapy import Spider
from scrapy.http.response.html import HtmlResponse


class SacredWordSpider(Spider):
    name = "sacred_word"
    start_urls = ["https://www.messianica.org.br/escrito-divino"]

    def parse(self, response: HtmlResponse):
        yield {
            "title": response.css("section")
            .css("h2.calendar-card__content-title::text")
            .get()
            .strip(),
            "url": f"{self.start_urls[0]}?d={date.today().strftime(format='%d/%m/%Y')}",
            "audio_url": f"https://www.messianica.org.br{response.css('audio#player').css('source').xpath('@src').get()}",
            "content": "".join(response.css("section#wa-conteudo::text").getall())
            .strip()
            .replace("\r\r", " "),
        }
