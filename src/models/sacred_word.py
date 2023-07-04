from dataclasses import dataclass

from datetime import date


@dataclass
class SacredWord:
    _id: str
    date: date
    title: str
    content: str
    audio_url: str
    url: str
