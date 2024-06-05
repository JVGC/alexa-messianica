from dataclasses import asdict, dataclass
from typing import Literal
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import date

CLIENT_KEY = {}


@dataclass
class SacredWord:
    _id: int
    date: date
    period: Literal["MATINAL", "VESPERAL"]
    title: str
    content: str
    audio_url: str
    url: str

    def __list__(self):
        return [str(v) for _, v in asdict(self).items()]

    def __dict__(self):
        return {k: str(v) for k, v in asdict(self).items()}


class SacredWordSpreadSheet:

    CLIENT_KEY_FILENAME = "client_key.json"
    SPREADSHEET_FILENAME = "Ensinamento do Dia"

    @staticmethod
    def connect_spreadsheet(sheet_name: str) -> gspread.Worksheet:
        scope = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(CLIENT_KEY, scope)
        client = gspread.authorize(creds)
        return client.open(SacredWordSpreadSheet.SPREADSHEET_FILENAME).worksheet(
            sheet_name
        )

    @staticmethod
    def create_sacred_word(
        _id: int,
        period: Literal["MATINAL", "VESPERAL"],
        date_str: str,
        title: str,
        content: str,
        audio_url: str,
        url: str,
    ) -> SacredWord:
        sacred_word = SacredWord(
            _id=_id,
            date=date_str,
            period=period,
            title=title,
            content=content,
            audio_url=audio_url,
            url=url,
        )

        sheet = SacredWordSpreadSheet.connect_spreadsheet("sacred_word_v2")
        sheet.append_row(sacred_word.__list__())

        return sacred_word

    @staticmethod
    def get_last_scraped_sacred_word() -> SacredWord:
        sheet = SacredWordSpreadSheet.connect_spreadsheet("sacred_word_v2")
        latest_sacred_word = sheet.get_all_records()[-1]
        return SacredWord(
            _id=latest_sacred_word["_id"],
            date=latest_sacred_word["date"],
            period=latest_sacred_word["period"],
            title=latest_sacred_word["title"],
            content=latest_sacred_word["content"],
            audio_url=latest_sacred_word["audio_url"],
            url=latest_sacred_word["url"],
        )

    @staticmethod
    def get_sacred_word_by_date(date_str: str) -> SacredWord:
        sheet = SacredWordSpreadSheet.connect_spreadsheet("sacred_word_v2")
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
