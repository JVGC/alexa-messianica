import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

from models.experience import Experience


CLIENT_KEY_FILENAME = "client_key.json"
SPREADSHEET_FILENAME = "Ensinamento do Dia"


class SpreadSheetRepository:
    def __init__(self) -> None:
        scope = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.getcwd(), "spreadsheet", CLIENT_KEY_FILENAME), scope
        )
        self.client = gspread.authorize(creds)

    def create(
        self,
        date: str,
        person_name: str,
        church: str,
        content: str,
        audio_url: str,
        url: str,
    ) -> Experience:
        sheet = self.client.open(SPREADSHEET_FILENAME).sheet1
        experience_obj = [
            date,
            person_name,
            church,
            content,
            audio_url,
            url,
        ]

        sheet.append_row(experience_obj)
