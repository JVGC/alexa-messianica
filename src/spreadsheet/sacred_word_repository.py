import gspread
import os
from uuid import uuid4
from oauth2client.service_account import ServiceAccountCredentials

from models.sacred_word import SacredWord


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"
SHEET_NAME = "sacred_word"


class SacredWordSheetRepository:
    def __init__(self) -> None:
        scope = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.getcwd(), "spreadsheet", CLIENT_KEY_FILENAME), scope
        )
        client = gspread.authorize(creds)
        self.sheet = client.open(SPREADSHEET_FILENAME).worksheet(SHEET_NAME)

    def create(
        self,
        date: str,
        title: str,
        content: str,
        audio_url: str,
        url: str,
    ) -> SacredWord:
        sacred_word_obj = [
            str(uuid4()),
            date,
            title,
            content,
            audio_url,
            url,
        ]

        self.sheet.append_row(sacred_word_obj)

    def getByDate(self, date) -> SacredWord:
        row = self.sheet.find(date, in_column=0).row
        latest_sacred_word = self.sheet.get_values(f"A{row}:F{row}")[0]
        return SacredWord(
            _id=latest_sacred_word[0],
            date=latest_sacred_word[1],
            title=latest_sacred_word[2],
            content=latest_sacred_word[3],
            audio_url=latest_sacred_word[4],
            url=latest_sacred_word[5],
        )
