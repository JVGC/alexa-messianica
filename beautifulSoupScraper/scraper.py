from dataclasses import dataclass, asdict
from uuid import uuid4
from datetime import date
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"


@dataclass
class SacredWord:
    _id: str
    date: date
    title: str
    content: str
    audio_url: str
    url: str

    def __list__(self):
        return [str(v) for _, v in asdict(self).items()]


def _connect_spreadsheet(sheet_name: str) -> gspread.Worksheet:
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(client_key, scope)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_FILENAME).worksheet(sheet_name)


def get_sacred_word_by_date(date_str: str) -> SacredWord:
    sheet = _connect_spreadsheet("sacred_word_v2")
    cell = sheet.find(date_str, in_column=0)

    if not cell:
        return None

    row = cell.row
    latest_sacred_word = sheet.get_values(f"A{row}:F{row}")[0]
    return SacredWord(
        _id=latest_sacred_word[0],
        date=latest_sacred_word[1],
        title=latest_sacred_word[2],
        content=latest_sacred_word[3],
        audio_url=latest_sacred_word[4],
        url=latest_sacred_word[5],
    )


def create_sacred_word(
    date_str: str,
    title: str,
    content: str,
    audio_url: str,
    url: str,
) -> SacredWord:
    sacred_word = SacredWord(
        _id=str(uuid4()),
        date=date_str,
        title=title,
        content=content,
        audio_url=audio_url,
        url=url,
    )

    sheet = _connect_spreadsheet("sacred_word_v2")
    sheet.append_row(sacred_word.__list__())

    return sacred_word


class SacredWordSpider:
    name = "sacred_word"
    start_url = f"https://www.messianica.org.br/escrito-divino?d={date.today().strftime(format='%d/%m/%Y')}"

    def scrape_data(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        title = soup.select_one("section h2.calendar-card__content-title").get_text(
            strip=True
        )
        date_str = soup.select_one("h1").get_text(strip=True)
        url = self.start_url
        audio_url = f"https://www.messianica.org.br{soup.select_one('audio#player source')['src']}"
        content = (
            soup.select_one("section#wa-conteudo")
            .get_text(strip=True)
            .replace("\r\r", " ")
        )

        return {
            "title": title,
            "date": date_str,
            "url": url,
            "audio_url": audio_url,
            "content": content,
        }

    def process_item(self, item):
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
            date_str=date.today().strftime(format="%d/%m/%Y"),
            title=item["title"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )

        return item


response = requests.get(SacredWordSpider.start_url, timeout=5)
if response.status_code == 200:
    spider = SacredWordSpider()
    data = spider.scrape_data(response.content)
    spider.process_item(data)
    print(data)
