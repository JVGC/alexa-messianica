from dataclasses import dataclass

from datetime import date


@dataclass
class Experience:
    _id: str
    date: date
    person_name: str
    church: str
    content: str
    audio_url: str
    url: str
