from dataclasses import dataclass, asdict

from datetime import date


@dataclass
class SacredWord:
    _id: str
    date: date
    title: str
    content: str
    audio_url: str
    url: str

    def __list__(self):
        return [str(v) for _, v in asdict(self).items()]
