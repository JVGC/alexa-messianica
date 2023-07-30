from uuid import uuid4
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from scraper.scraper.models import Experience, SacredWord


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"


def _connect_spreadsheet(sheet_name: str) -> gspread.Worksheet:
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(os.getcwd(), "scraper", "scraper", CLIENT_KEY_FILENAME),
        scope,
    )
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_FILENAME).worksheet(sheet_name)


def create_experience(
    date: str,
    person_name: str,
    church: str,
    content: str,
    audio_url: str,
    url: str,
) -> Experience:
    experience = Experience(
        _id=str(uuid4()),
        date=date,
        person_name=person_name,
        church=church,
        content=content,
        audio_url=audio_url,
        url=url,
    )

    sheet = _connect_spreadsheet("experience")
    sheet.append_row(experience.__list__())

    return experience


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
