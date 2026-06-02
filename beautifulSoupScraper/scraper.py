from dataclasses import dataclass, asdict
from uuid import uuid4
from datetime import date
import json
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
    with open(CLIENT_KEY_FILENAME) as f:
        client_key = json.load(f)
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
    base_url = "https://www.messianica.org.br"
    listing_url = "https://www.messianica.org.br/escritos-divinos"

    def get_today_url(self) -> str | None:
        today = date.today().strftime("%Y-%m-%d")
        response = requests.get(self.listing_url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        for a in soup.find_all("a", href=True):
            if today in a["href"] and "/escritos-divinos/" in a["href"]:
                return self.base_url + a["href"]
        return None

    def scrape_data(self, html_content, url: str) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")

        article = soup.find("article")
        title = article.find("header").find("h1").get_text(strip=True)

        time_tag = soup.find("time")
        date_obj = date.fromisoformat(time_tag["datetime"][:10])
        formatted_date = date_obj.strftime("%d/%m/%Y")

        audio_tag = soup.select_one("audio[src]")
        audio_url = audio_tag["src"] if audio_tag else ""

        content_div = article.find("div", class_=lambda c: c and "mt-8" in c)
        content = (
            content_div.get_text(strip=True).replace("\r\r", " ")
            if content_div
            else ""
        )

        return {
            "title": title,
            "date": formatted_date,
            "url": url,
            "audio_url": audio_url,
            "content": content,
        }

    def process_item(self, item: dict) -> dict:
        today_str = date.today().strftime("%d/%m/%Y")
        if item["date"] != today_str:
            print("Today's sacred word is not available yet")
            return item

        already_exists = get_sacred_word_by_date(today_str)
        if already_exists:
            print("Today's sacred word already scrapped. Skipping...")
            return item

        print("Scrapping today's sacred word")
        create_sacred_word(
            date_str=today_str,
            title=item["title"],
            content=item["content"],
            audio_url=item["audio_url"],
            url=item["url"],
        )

        return item


spider = SacredWordSpider()
today_url = spider.get_today_url()
if today_url:
    response = requests.get(today_url, timeout=5)
    if response.status_code == 200:
        data = spider.scrape_data(response.content, today_url)
        spider.process_item(data)
        print(data)
    else:
        print(f"Failed to fetch {today_url}: {response.status_code}")
else:
    print("Today's sacred word URL not found on listing page")
