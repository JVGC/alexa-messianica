import gspread
import os
from uuid import uuid4
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
            str(uuid4()),
            date,
            person_name,
            church,
            content,
            audio_url,
            url,
        ]

        sheet.append_row(experience_obj)

    def getByDate(self, date) -> Experience:
        sheet = self.client.open(SPREADSHEET_FILENAME).sheet1

        all_values = sheet.get_all_values()
        latest_experience = all_values[-1]
        return Experience(
            _id=latest_experience[0],
            date=latest_experience[1],
            person_name=latest_experience[2],
            church=latest_experience[3],
            content=latest_experience[4],
            audio_url=latest_experience[5],
            url=latest_experience[6],
        )
