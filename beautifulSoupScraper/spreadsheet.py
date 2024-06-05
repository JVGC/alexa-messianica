from dataclasses import asdict, dataclass
from typing import Literal
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import date

CLIENT_KEY = {
    "type": "service_account",
    "project_id": "ensinamento-de-meishu-sama",
    "private_key_id": "d4e8e9e747796ab277678c0498b0a9931f6f3752",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDaOO1GT9Mk0uqT\ndLiJpBB0J8+eWoAqFkxyt0G6H5r0k4MVn/pqL9Rn44kYZ5BU85kHU9XM71dAkzx4\nDgbbmHhx9RCU/g0IxCu4TWYgEEPSmOxHDccjmvEpOoHh7OIevWUTz6CttQFsF5TB\n2s4i6e00rCdI8/uPZaecSDEjQx0oJAqUrCftTkO3HXPYPQQ4zOBRs64QIrZp+F0c\nWUJGAmDFUt429Zys3YHermVGoXGyyMcRnyjQpY+W39UfUEn3fWAjo/Msao3wTxko\nrkBuVyqLL6GRPAPf84w7Zskz+4EzAjvBf8dkQuim78tsNcgiBrR+5aVutNoE6G9j\nWbIWDDTjAgMBAAECggEACek4+Y8Jj2wW5FCSSwoNB0GBn/cLSB4QJcul7A6gaohC\nlVpZNLZsZrWCVf3qI7mWkysfFDowk8m8HtXAQPv5SG+xa5roO6QxOiMlxsIGWovA\ne2+oQjk4x78VBA5OrMe8TfyJlyoX4PFnO7C02QgX0mMZO6p9G+Opi6MJvEjBi7+V\n0nM07HVBw85L4idYJ/QTR2FTpocPKRtwKIgeIog6pKuV3VmaUPaJgZR66cT9T7U6\nKAbPiPa12r5wVDuYE+kCwWd6pRY62IvA4Z5/ghRxVo1a93qEb9ECzl6fqMKFsNhR\nMU3LpL/824DY9M0qozXq+Jx83+c7wCfs/qYXMoiNGQKBgQDz86EtLCCJdmZ/bv//\nm90mjdyseRmMCRlKKGbc/zM7Zv+DVLC11MifD+Q57VAn1g8YKHM+7Pr8cggtTR3B\neK3zfwFPUwM85kUBKkJBP40Dxy2CYqmCjdz3X5vZMRvGPZlqg6bltsKAqvSyYkLc\nl7nLR1Ai/uzp8v3NFvFKlVY8uwKBgQDk//4A2NCmFChhuvftfplaxicpgoFNHGa6\nMjw35R3p0TYcD68FJ+ijUxHbV0MBIFLUmmRUNqRa2zH06WIGfs15mC/nA9vcpeAr\n6ll+jXHUSQtosHG+ZmPvLR5Ro6YGGOL8tS7ZodYaXRuyrXsTEi/TMmJWJwJ+zubh\nNMqjOVi5+QKBgQDoCVPFI7PPDE9x5qKY/ifcBBNh+c3S5NSpNMSicBrK5a0jvepX\nCY3JvdPXRWJ4gaLZ15/GuqIAfHZKoI8s9xx9/s/AI7Vwt5XrBcb/SPNYJJuk6TNS\nep0yrj4O2CcS6ISES7TzymI3AGS/R7dRGwAd2jbfEptF61p9ONVJm8HrAQKBgQCQ\neoJC/ogFgEpJ/rBVgr42azZiFhiGEhkt+GvNyBwrXPeKlMqTsi4wfUSS4mc/2qjn\nwdDy4NapDApkvqo99tqkkMQIOIMKnwzkKCL2mT7r9HniPxBEVE1QpWKvl1Q0HJd5\nYMaCQHzYfU3wWUuBKMRLt0obmNkWMGuyQqBmgtPb4QKBgQDkTtWQMiptTJMebJdM\nCNNtkIc6mISRsYT4obZjNc+nWGynw7AiUiX3vNJpd7bLvtFXxO1FNREdHV1v1vDO\nzC3+DiG3PPsyuU/ZLAhAE3iS+fm9leuY5DiUSxxxqcdPJb9yU9yX4YHI+Xoj4Rwu\nbiF/MAmFW0ayRne8LlL4gtp06A==\n-----END PRIVATE KEY-----\n",
    "client_email": "ensinamentosheets@ensinamento-de-meishu-sama.iam.gserviceaccount.com",
    "client_id": "104566814956533700620",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ensinamentosheets%40ensinamento-de-meishu-sama.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}


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
