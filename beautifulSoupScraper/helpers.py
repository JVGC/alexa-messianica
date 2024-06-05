from bs4 import BeautifulSoup


def get_period(soup: BeautifulSoup) -> str:
    period = soup.select_one("span.calendar-card__title-text").get_text().split("- ")
    if len(period) > 1:
        return period[1].upper()
    return "MATINAL"


def get_audio_url(soup: BeautifulSoup) -> str:
    base_url = "https://www.messianica.org.br{element}"
    audio_url = soup.select_one("audio#player source")
    if not audio_url:
        return ""
    return base_url.format(element=audio_url.get("src"))


SCRAPE_FUNCTIONS = {
    "title": lambda soup: soup.select_one(
        "section h2.calendar-card__content-title"
    ).get_text(strip=True),
    "date": lambda soup: soup.select_one("h1").get_text(strip=True),
    "period": lambda soup: get_period(soup),
    "audio_url": lambda soup: get_audio_url(soup),
    "content": lambda soup: soup.select_one("section#wa-conteudo")
    .get_text(strip=True)
    .replace("\r\r", " "),
}
