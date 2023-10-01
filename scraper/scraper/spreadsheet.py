from uuid import uuid4
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scraper.models import SacredWord


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"


def _connect_spreadsheet(sheet_name: str) -> gspread.Worksheet:
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(os.getcwd(), "scraper", CLIENT_KEY_FILENAME),
        scope,
    )
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_FILENAME).worksheet(sheet_name)


def get_sacred_word_by_date(date: str) -> SacredWord:
    sheet = _connect_spreadsheet("sacred_word")
    cell = sheet.find(date, in_column=0)

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
    date: str,
    title: str,
    content: str,
    audio_url: str,
    url: str,
) -> SacredWord:
    sacred_word = SacredWord(
        _id=str(uuid4()),
        date=date,
        title=title,
        content=content,
        audio_url=audio_url,
        url=url,
    )

    sheet = _connect_spreadsheet("sacred_word")
    sheet.append_row(sacred_word.__list__())

    return sacred_word
