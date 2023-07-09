import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.models import Experience, SacredWord


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"


def _connect_spreadsheet(sheet_name: str) -> gspread.Worksheet:
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(os.getcwd(), "app", CLIENT_KEY_FILENAME),
        scope,
    )
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_FILENAME).worksheet(sheet_name)


def get_experience_by_date(date: str) -> Experience:
    sheet = _connect_spreadsheet("experience")
    row = sheet.find(date, in_column=0).row
    latest_experience = sheet.get_values(f"A{row}:G{row}")[0]
    return Experience(
        _id=latest_experience[0],
        date=latest_experience[1],
        person_name=latest_experience[2],
        church=latest_experience[3],
        content=latest_experience[4],
        audio_url=latest_experience[5],
        url=latest_experience[6],
    )


def get_sacred_word_by_date(date: str) -> SacredWord:
    sheet = _connect_spreadsheet("sacred_word")
    row = sheet.find(date, in_column=0).row
    latest_sacred_word = sheet.get_values(f"A{row}:F{row}")[0]
    return SacredWord(
        _id=latest_sacred_word[0],
        date=latest_sacred_word[1],
        title=latest_sacred_word[2],
        content=latest_sacred_word[3],
        audio_url=latest_sacred_word[4],
        url=latest_sacred_word[5],
    )
